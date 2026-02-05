from pymongo import MongoClient
from typing import List, Dict, Any
import uuid
from datetime import datetime
import PyPDF2
import io
import base64
import numpy as np
from app.config import settings
from app.services.embedding_service import embedding_service

class DocumentService:
    """Service for managing documents and vector store with MongoDB"""
    
    def __init__(self):
        # Use timeout to avoid hanging
        self.client = MongoClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=30000,
            connectTimeoutMS=30000,
            socketTimeoutMS=60000
        )
        self.db = self.client[settings.DATABASE_NAME]
        self.collection = self.db[settings.COLLECTION_NAME]
        # Test connection
        try:
            self.client.admin.command('ping')
            print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
        except Exception as e:
            print(f"⚠️ MongoDB connection warning: {e}")
    
    def chunk_text_with_lines(self, text: str, chunk_size: int = None, overlap: int = None) -> List[Dict[str, Any]]:
        """Split text into overlapping chunks with line number tracking"""
        chunk_size = chunk_size or settings.CHUNK_SIZE
        overlap = overlap or settings.CHUNK_OVERLAP
        
        # Split into lines and track positions
        lines = text.split('\n')
        line_positions = []  # (start_char, end_char, line_number)
        current_pos = 0
        for i, line in enumerate(lines):
            line_positions.append((current_pos, current_pos + len(line), i + 1))
            current_pos += len(line) + 1  # +1 for newline
        
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < text_length:
                last_period = chunk.rfind('.')
                last_newline = chunk.rfind('\n')
                break_point = max(last_period, last_newline)
                
                if break_point > chunk_size * 0.5:
                    chunk = chunk[:break_point + 1]
                    end = start + break_point + 1
            
            # Find line numbers for this chunk
            start_line = 1
            end_line = 1
            for pos_start, pos_end, line_num in line_positions:
                if pos_start <= start < pos_end or (pos_start <= start and pos_end >= start):
                    start_line = line_num
                if pos_start < end <= pos_end or (pos_start < end and pos_end >= end):
                    end_line = line_num
                    break
                if pos_start >= end:
                    break
                end_line = line_num
            
            if chunk.strip():
                chunks.append({
                    "text": chunk.strip(),
                    "start_line": start_line,
                    "end_line": end_line
                })
            
            start = end - overlap
        
        return chunks
    
    def extract_text_from_pdf(self, pdf_content: bytes) -> List[Dict[str, Any]]:
        """Extract text from PDF bytes with page tracking"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pages_data = []
            for page_num, page in enumerate(pdf_reader.pages, 1):
                page_text = page.extract_text()
                if page_text.strip():
                    pages_data.append({
                        "text": page_text,
                        "page_number": page_num
                    })
            return pages_data
        except Exception as e:
            raise Exception(f"Error extracting PDF text: {str(e)}")
    
    def add_pdf_document(self, filename: str, pdf_content: bytes, metadata: Dict[str, Any] = None) -> str:
        """Add a PDF document with page number tracking"""
        doc_id = str(uuid.uuid4())
        
        # Extract pages from PDF
        pages_data = self.extract_text_from_pdf(pdf_content)
        
        all_chunks = []
        
        # Process each page
        for page_info in pages_data:
            page_text = page_info["text"]
            page_num = page_info["page_number"]
            
            # Chunk this page with line numbers
            page_chunks = self.chunk_text_with_lines(page_text)
            
            # Add page number to each chunk
            for chunk in page_chunks:
                chunk["page_number"] = page_num
                all_chunks.append(chunk)
        
        if not all_chunks:
            raise Exception("No text content found in PDF")
        
        # Extract just the text for embeddings
        chunk_texts = [c["text"] for c in all_chunks]
        
        # Generate embeddings
        embeddings = embedding_service.generate_embeddings(chunk_texts)
        
        # Prepare chunks with embeddings
        chunks_with_embeddings = [
            {
                "text": all_chunks[i]["text"],
                "embedding": embeddings[i],
                "start_line": all_chunks[i]["start_line"],
                "end_line": all_chunks[i]["end_line"],
                "page_number": all_chunks[i].get("page_number"),
                "chunk_index": i
            }
            for i in range(len(all_chunks))
        ]
        
        # Store in MongoDB
        document = {
            "_id": doc_id,
            "filename": filename,
            "doc_type": "pdf",
            "pdf_binary": base64.b64encode(pdf_content).decode('utf-8'),
            "chunks": chunks_with_embeddings,
            "total_chunks": len(chunks_with_embeddings),
            "upload_date": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        
        self.collection.insert_one(document)
        print(f"✅ Stored document {filename} with {len(chunks_with_embeddings)} chunks")
        
        return doc_id
    
    def search_similar(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        """Search for similar chunks using cosine similarity"""
        top_k = top_k or settings.TOP_K_RESULTS
        
        # Generate query embedding
        query_embedding = embedding_service.generate_query_embedding(query)
        
        # Get all documents with chunks
        all_docs = list(self.collection.find({}, {"filename": 1, "chunks": 1, "doc_type": 1}))
        
        if not all_docs:
            return []
        
        # Calculate similarity for all chunks
        results = []
        for doc in all_docs:
            for chunk in doc.get("chunks", []):
                chunk_embedding = chunk.get("embedding", [])
                if not chunk_embedding:
                    continue
                
                # Cosine similarity
                similarity = self._cosine_similarity(query_embedding, chunk_embedding)
                # Convert to distance (0 = identical, 2 = opposite)
                distance = 1 - similarity
                
                results.append({
                    "document": chunk["text"],
                    "metadata": {
                        "filename": doc["filename"],
                        "doc_type": doc["doc_type"],
                        "start_line": chunk.get("start_line", 1),
                        "end_line": chunk.get("end_line", 1),
                        "page_number": chunk.get("page_number"),
                        "chunk_index": chunk.get("chunk_index", 0)
                    },
                    "distance": distance,
                    "relevance_score": similarity
                })
        
        # Sort by distance (ascending) and return top k
        results.sort(key=lambda x: x["distance"])
        return results[:top_k]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        v1 = np.array(vec1)
        v2 = np.array(vec2)
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    
    def get_all_documents(self) -> List[Dict[str, Any]]:
        """Get all unique documents in the knowledge base"""
        documents = list(self.collection.find(
            {},
            {"_id": 1, "filename": 1, "upload_date": 1, "doc_type": 1, "total_chunks": 1}
        ))
        
        return [
            {
                "id": str(doc["_id"]),
                "filename": doc.get("filename", "Unknown"),
                "upload_date": doc.get("upload_date", ""),
                "doc_type": doc.get("doc_type", "pdf"),
                "chunk_count": doc.get("total_chunks", 0)
            }
            for doc in documents
        ]
    
    def delete_document(self, doc_id: str) -> bool:
        """Delete a document and all its chunks"""
        try:
            result = self.collection.delete_one({"_id": doc_id})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting document: {e}")
            return False

document_service = DocumentService()
