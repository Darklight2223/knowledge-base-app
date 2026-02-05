from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from app.config import settings
from app.models import (
    QueryRequest, QueryResponse, DocumentInfo, 
    HealthResponse, DocumentUpload
)
from app.services.document_service import document_service
from app.services.rag_service import rag_service

app = FastAPI(
    title="AI Knowledge Base API",
    description="RAG-powered knowledge base with Gemini AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    gemini_configured = bool(settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != "your_gemini_api_key_here")
    
    return HealthResponse(
        status="healthy" if gemini_configured else "warning",
        message="AI Knowledge Base API is running" if gemini_configured else "Gemini API key not configured",
        gemini_configured=gemini_configured
    )

@app.post("/api/documents/upload", response_model=dict)
async def upload_document(file: UploadFile = File(...)):
    """Upload and index a PDF document"""
    try:
        # Read file content
        content = await file.read()
        
        # Determine file type and extract text
        filename = file.filename
        file_extension = os.path.splitext(filename)[1].lower()
        
        # Only allow PDF files
        if file_extension != '.pdf':
            raise HTTPException(status_code=400, detail="Only PDF files are allowed. Please upload a PDF document.")
        
        # Use PDF-specific method with page tracking
        doc_id = document_service.add_pdf_document(
            filename=filename,
            pdf_content=content
        )
        
        return {
            "message": "Document uploaded and indexed successfully",
            "document_id": doc_id,
            "filename": filename,
            "doc_type": "pdf"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/documents/text", response_model=dict)
async def upload_text_document(doc: DocumentUpload):
    """Upload a text document directly"""
    try:
        doc_id = document_service.add_document(
            filename=doc.filename,
            content=doc.content,
            doc_type=doc.doc_type,
            metadata=doc.metadata
        )
        
        return {
            "message": "Document uploaded and indexed successfully",
            "document_id": doc_id,
            "filename": doc.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query", response_model=QueryResponse)
async def query_knowledge_base(request: QueryRequest):
    """Query the knowledge base"""
    try:
        response = rag_service.generate_answer(request.query, request.top_k)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents", response_model=List[DocumentInfo])
async def get_documents():
    """Get all documents in the knowledge base"""
    try:
        documents = document_service.get_all_documents()
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/api/documents/{document_id}", response_model=dict)
async def delete_document(document_id: str):
    """Delete a document from the knowledge base"""
    try:
        success = document_service.delete_document(document_id)
        if success:
            return {"message": "Document deleted successfully", "document_id": document_id}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
