from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    GEMINI_API_KEY: str
    MONGODB_URI: str
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # Database settings
    DATABASE_NAME: str = "knowledge_base"
    COLLECTION_NAME: str = "documents"

    # Gemini embedding model
    EMBEDDING_MODEL: str = "models/text-embedding-004"
    GEMINI_MODEL: str = "models/gemini-2.5-flash-lite"
    
    # RAG settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    TOP_K_RESULTS: int = 3
    MIN_RELEVANCE_SCORE: float = 50.0  # Minimum relevance % to include in sources
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()
