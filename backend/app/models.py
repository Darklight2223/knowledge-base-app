from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DocumentUpload(BaseModel):
    """Model for document metadata"""
    filename: str
    content: str
    doc_type: str = "text"
    metadata: Optional[dict] = None

class QueryRequest(BaseModel):
    """Model for query requests"""
    query: str = Field(..., min_length=1, max_length=1000)
    top_k: Optional[int] = Field(default=None, ge=1, le=20)  # None = use config default

class Source(BaseModel):
    """Model for source citations"""
    document_name: str
    chunk_text: str
    relevance_score: float
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    page_number: Optional[int] = None

class QueryResponse(BaseModel):
    """Model for query responses"""
    answer: str
    sources: List[Source]
    query: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class DocumentInfo(BaseModel):
    """Model for document information"""
    id: str
    filename: str
    upload_date: str
    doc_type: str
    chunk_count: int
    
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    gemini_configured: bool
