import google.generativeai as genai
from typing import List
from app.config import settings

class EmbeddingService:
    """Service for generating embeddings using Gemini text-embedding-004"""
    
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.EMBEDDING_MODEL
        # embedding-001: 3072 dims, text-embedding-004: 768 dims
        self.dimension = 3072 if 'embedding-001' in self.model_name else 768
        print(f"✅ Using Gemini embedding model: {self.model_name} ({self.dimension} dimensions)")
    
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        try:
            embeddings = []
            for text in texts:
                result = genai.embed_content(
                    model=self.model_name,
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            return embeddings
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return [[0.0] * self.dimension for _ in texts]
    
    def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query"""
        try:
            result = genai.embed_content(
                model=self.model_name,
                content=query,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return [0.0] * self.dimension

embedding_service = EmbeddingService()
