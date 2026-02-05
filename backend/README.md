# AI Knowledge Base - Backend API

FastAPI backend with RAG (Retrieval Augmented Generation) powered by Google Gemini AI.

## Features

- 📄 **Document Ingestion**: Upload PDF and text documents
- 🔍 **Vector Search**: Efficient similarity search using ChromaDB
- 🤖 **RAG Pipeline**: Context-aware answers with Gemini AI
- 📚 **Source Citations**: All responses include source references
- 🔄 **Document Management**: Add, list, and delete documents

## Tech Stack

- **FastAPI**: Modern Python web framework
- **ChromaDB**: Vector database for embeddings
- **Google Gemini**: LLM for embeddings and generation
- **PyPDF2**: PDF text extraction
- **Pydantic**: Data validation

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 3. Run the Server

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /
```

### Upload Document (File)
```
POST /api/documents/upload
Content-Type: multipart/form-data
Body: file (PDF or TXT)
```

### Upload Document (Text)
```
POST /api/documents/text
Content-Type: application/json
Body: {
  "filename": "doc.txt",
  "content": "...",
  "doc_type": "text"
}
```

### Query Knowledge Base
```
POST /api/query
Content-Type: application/json
Body: {
  "query": "Your question here",
  "top_k": 5
}
```

### List Documents
```
GET /api/documents
```

### Delete Document
```
DELETE /api/documents/{document_id}
```

## Configuration

Key settings in `app/config.py`:

- `CHUNK_SIZE`: Document chunk size (default: 1000)
- `CHUNK_OVERLAP`: Overlap between chunks (default: 200)
- `TOP_K_RESULTS`: Number of source chunks to retrieve (default: 5)
- `GEMINI_MODEL`: Gemini model to use (default: gemini-1.5-pro-latest)

## RAG Pipeline

1. **Document Upload**: Documents are split into chunks with overlap
2. **Embedding**: Each chunk is embedded using Gemini embeddings
3. **Storage**: Embeddings stored in ChromaDB vector database
4. **Query**: User query is embedded and similar chunks retrieved
5. **Generation**: Gemini generates answer based on retrieved context
6. **Citation**: Sources are returned with relevance scores

## Deployment

### Docker (Recommended)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t kb-backend .
docker run -p 8000:8000 --env-file .env kb-backend
```

### Cloud Deployment Options

- **Google Cloud Run**: Containerized deployment
- **AWS Lambda**: With Mangum adapter
- **Heroku**: With Procfile
- **Azure App Service**: Container deployment

## Monitoring

The API includes:
- Request/response logging
- Error handling with detailed messages
- Health check endpoint for uptime monitoring

## Security Notes

- Never commit `.env` file
- Use environment variables for secrets
- Enable CORS only for trusted origins
- Implement rate limiting for production
- Add authentication/authorization as needed

## Troubleshooting

### ChromaDB Permission Issues
```bash
chmod -R 755 chroma_db/
```

### Gemini API Errors
- Verify API key is valid
- Check API quotas
- Ensure network connectivity

### PDF Extraction Issues
- Install system dependencies if needed
- Some PDFs may have encoding issues
- Try converting to text first

## Development

Run with auto-reload:
```bash
uvicorn app.main:app --reload
```

Run tests (if implemented):
```bash
pytest
```

## License

MIT
