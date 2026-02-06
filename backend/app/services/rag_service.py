import google.generativeai as genai
from typing import List, Dict, Any
from app.config import settings
from app.services.document_service import document_service
from app.models import QueryResponse, Source

class RAGService:
    """RAG service using Gemini for generation"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def is_casual_query(self, query: str) -> bool:
        """Check if query is casual/conversational (not a knowledge base question)"""
        query_lower = query.lower().strip()
        # Short queries (less than 4 words) that don't look like questions
        words = query_lower.split()
        if len(words) <= 3 and not any(q in query_lower for q in ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'explain', 'describe', 'tell me']):
            return True
        return False
    
    def generate_casual_response(self, query: str) -> QueryResponse:
        """Generate a casual conversational response without RAG"""
        try:
            prompt = f"""You are a friendly AI assistant for a knowledge base system. 
The user sent a casual message. Respond naturally and briefly.
If they seem to want help, let them know they can ask questions about the uploaded documents.

User: {query}

Respond briefly and friendly:"""
            
            response = self.model.generate_content(
                prompt,
                generation_config={"temperature": 0.9, "max_output_tokens": 256}
            )
            return QueryResponse(answer=response.text, sources=[], query=query)
        except Exception as e:
            print(f"🔴 CASUAL RESPONSE ERROR: {type(e).__name__}: {e}")
            error_msg = str(e).lower()
            if any(keyword in error_msg for keyword in ['exhausted', 'quota', 'rate limit', '429']):
                return QueryResponse(
                    answer="⚠️ **API Rate Limit Exhausted**\n\nPlease wait for **1 minute** before trying again.",
                    sources=[], query=query
                )
            if 'not found' in error_msg or 'invalid' in error_msg:
                return QueryResponse(
                    answer=f"⚠️ **Model Configuration Error**: {str(e)}\n\nPlease check the GEMINI_MODEL setting.",
                    sources=[], query=query
                )
            return QueryResponse(answer=f"⚠️ Error: {str(e)}", sources=[], query=query)
    
    def generate_answer(self, query: str, top_k: int = None) -> QueryResponse:
        """Generate an answer using RAG"""
        # Handle casual/conversational queries without RAG
        if self.is_casual_query(query):
            print(f"💬 Casual query detected: '{query}'")
            return self.generate_casual_response(query)
        
        top_k = top_k or settings.TOP_K_RESULTS
        print(f"🔍 RAG: Using top_k={top_k}")
        
        # Retrieve relevant documents
        search_results = document_service.search_similar(query, top_k)
        print(f"🔍 RAG: Got {len(search_results)} results from search")
        
        if not search_results:
            return QueryResponse(
                answer="I don't have enough information in my knowledge base to answer this question. Please upload relevant documents first.",
                sources=[],
                query=query
            )
        
        # Build context from search results
        context_parts = []
        sources = []
        
        for idx, result in enumerate(search_results):
            doc_text = result['document']
            metadata = result['metadata']
            # Fix relevance score: convert cosine distance to percentage
            distance = result.get('distance', 1)
            # Cosine distance ranges 0-2, convert to 0-100% (0 distance = 100% match)
            relevance = max(0, min(100, (1 - distance / 2) * 100))
            
            # Skip sources below minimum relevance threshold
            if relevance < settings.MIN_RELEVANCE_SCORE:
                continue
            
            # Get line numbers and page number from metadata
            start_line = metadata.get('start_line', 1)
            end_line = metadata.get('end_line', 1)
            page_number = metadata.get('page_number')
            
            # Build location string
            location = f"Lines {start_line}-{end_line}"
            if page_number:
                location = f"Page {page_number}, {location}"
            
            context_parts.append(f"[Source {idx + 1}: {metadata.get('filename', 'Unknown')} ({location})]\n{doc_text}\n")
            
            sources.append(Source(
                document_name=metadata.get('filename', 'Unknown'),
                chunk_text=doc_text[:300] + "..." if len(doc_text) > 300 else doc_text,
                relevance_score=round(relevance, 1),
                start_line=start_line,
                end_line=end_line,
                page_number=page_number
            ))
        
        print(f"🔍 RAG: Returning {len(sources)} sources after filtering (min relevance: {settings.MIN_RELEVANCE_SCORE}%)")
        context = "\n".join(context_parts)
        
        # Create prompt for Gemini
        prompt = f"""You are a helpful AI assistant for a knowledge base system. Answer the user's question based ONLY on the provided context. 

IMPORTANT RULES:
1. Only use information from the provided sources
2. If the sources don't contain enough information, say so clearly
3. Cite your sources by mentioning the document name
4. Be concise but comprehensive
5. If you're uncertain, express that uncertainty
6. Format your answer in a clear, readable way using markdown

CONTEXT FROM KNOWLEDGE BASE:
{context}

USER QUESTION: {query}

Please provide a well-structured answer with proper citations:"""
        
        try:
            # Generate response using Gemini
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 2048,
                }
            )
            
            answer = response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            # Check for rate limit / quota exhausted errors
            if any(keyword in error_msg for keyword in ['exhausted', 'quota', 'rate limit', '429']):
                print(f"⚠️ API limit exhausted: {e}")
                return QueryResponse(
                    answer="⚠️ **API Rate Limit Exhausted**\n\nPlease wait for **1 minute** before trying again.",
                    sources=[],  # Don't show sources on rate limit
                    query=query
                )
            if 'not found' in error_msg or 'invalid' in error_msg:
                print(f"❌ Model error: {e}")
                return QueryResponse(
                    answer=f"⚠️ **Model Configuration Error**: {str(e)}\n\nPlease check the GEMINI_MODEL setting.",
                    sources=[],
                    query=query
                )
            answer = f"Error generating response: {str(e)}\n\nHowever, I found {len(sources)} relevant sources that might help answer your question."
        
        return QueryResponse(
            answer=answer,
            sources=sources,
            query=query
        )

rag_service = RAGService()
