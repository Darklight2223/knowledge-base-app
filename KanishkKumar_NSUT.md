# Technical and Product Decision Document

**Project:** AI Knowledge Base with RAG (Retrieval-Augmented Generation)  
**Author:** Kanishk Kumar  
**Institution:** NSUT (Netaji Subhas University of Technology)  
**Date:** February 6, 2026  

---

## Executive Summary

This document outlines the technical and product decisions made during the development of an AI-powered Knowledge Base system using Retrieval-Augmented Generation (RAG). The system allows users to upload PDF documents, which are then indexed and made queryable through natural language interactions powered by Google's Gemini AI.

---

## How to Use This Application

### Getting Started

1. **Access the Application**
   - Open the frontend in your browser (default: `http://localhost:3000`)
   - Ensure both backend (port 8000) and frontend servers are running

2. **Upload Documents**
   - Click the **"📄 Documents"** button in the top right corner
   - Click **"Upload PDF"** or drag and drop a PDF file
   - Wait for the upload confirmation message

3. **Ask Questions**
   - Type your question in the chat input box at the bottom
   - Press **Enter** or click the send button
   - Wait for the AI to process and respond with sourced answers

### Important Usage Guidelines

#### File Upload Restrictions
- ✅ **Supported Format:** PDF files only
- ⚠️ **Maximum Size:** 10 MB per file
- ⏱️ **Processing Time:** 
  - Small files (< 1 MB): ~5-10 seconds
  - Medium files (1-5 MB): ~15-30 seconds
  - Large files (5-10 MB): ~30-60 seconds (may take longer)
- 📄 **Page Count:** Files with 100+ pages may take several minutes to process

#### Query Best Practices
- **Be specific:** Ask clear, focused questions about your documents
- **Use natural language:** Write questions as you would ask a person
- **Wait for responses:** Large document searches may take 5-10 seconds
- **Check sources:** Review the source citations provided with each answer
- **Free tier limit:** If using Gemini free tier, you have 20 requests per day

#### Example Queries
```
✅ Good: "What are the company's vacation policies?"
✅ Good: "Explain the troubleshooting steps for error code 404"
✅ Good: "What products are mentioned in the documentation?"

❌ Avoid: Single word queries like "policies" (too vague)
❌ Avoid: Questions about content not in uploaded documents
```

#### Managing Documents
- **View documents:** Click the Documents button to see all uploaded files
- **Delete documents:** Click the trash icon next to any document to remove it
- **Re-upload:** If a document seems outdated, delete and re-upload it
- **Multiple documents:** The system searches across all uploaded documents

#### Troubleshooting
- **No results found:** Ensure relevant documents are uploaded
- **API rate limit error:** Wait 24 hours or upgrade to paid Gemini API tier
- **Upload fails:** Check file size (< 10 MB) and format (PDF only)
- **Slow responses:** Large documents or many documents increase processing time

---

## 1. Architecture Decisions

### 1.1 RAG (Retrieval-Augmented Generation) Architecture

**Decision:** Implement a RAG-based system rather than fine-tuning or pure LLM approach.

**Rationale:**
- **Cost-effectiveness:** RAG doesn't require expensive model fine-tuning
- **Dynamic knowledge:** Documents can be added/removed without retraining
- **Source attribution:** Provides transparent citations for generated answers
- **Accuracy:** Grounds responses in actual document content, reducing hallucinations

**Implementation:**
- Document chunking with overlap (1000 chars, 200 overlap)
- Vector embeddings for semantic search
- Context injection into LLM prompts
- Relevance scoring and filtering (50% minimum threshold)

### 1.2 Database Choice: MongoDB with Vector Search

**Decision:** Use MongoDB Atlas with vector embeddings stored as arrays.

**Rationale:**
- **Flexibility:** Schema-less design accommodates varying document metadata
- **Vector storage:** Native support for storing embedding vectors
- **Scalability:** Cloud-native with automatic scaling
- **Integration:** Easy integration with Python ecosystem

**Alternative Considered:**
- ChromaDB (initially used) - Less scalable for production
- Pinecone - Additional cost for specialized vector DB
- PostgreSQL with pgvector - More complex setup

**Trade-offs:**
- MongoDB's cosine similarity search is implemented in application layer
- Requires custom distance calculations vs. specialized vector DBs

---

## 2. Technology Stack Decisions

### 2.1 Backend Framework: FastAPI

**Decision:** Use FastAPI for the backend REST API.

**Rationale:**
- **Performance:** Async support for handling concurrent requests
- **Type safety:** Pydantic models for request/response validation
- **Auto documentation:** Built-in Swagger/OpenAPI generation
- **Modern Python:** Native async/await support

**Key Features Used:**
- File upload handling with `UploadFile`
- CORS middleware for cross-origin requests
- Pydantic settings management with environment variables
- Automatic JSON serialization

### 2.2 Frontend Framework: Next.js 14

**Decision:** Use Next.js with App Router and React.

**Rationale:**
- **Server Components:** Improved performance with React Server Components
- **Developer Experience:** Hot reload, TypeScript support
- **Deployment:** Easy deployment to Vercel
- **Modern UI:** Integration with Tailwind CSS and Framer Motion

**Libraries Integrated:**
- **Tailwind CSS:** Utility-first styling
- **Framer Motion:** Smooth animations and transitions
- **Axios:** HTTP client for API calls
- **Heroicons:** Consistent icon set

### 2.3 AI Model: Google Gemini

**Decision:** Use Google Gemini API for both embeddings and text generation.

**Rationale:**
- **Cost:** Free tier available for development/testing
- **Performance:** Fast response times
- **Quality:** High-quality embeddings and generation
- **Single Provider:** Unified API for both embeddings and generation

**Model Choices:**

| Purpose | Model | Dimensions | Rationale |
|---------|-------|------------|-----------|
| Embeddings | `embedding-001` | 3072 | Higher dimensionality for better semantic capture |
| Text Generation | `gemini-2.0-flash` | N/A | Fast, cost-effective for conversational AI |

**Alternative Considered:**
- OpenAI (GPT-4 + text-embedding-ada-002) - Higher cost
- Anthropic Claude - No native embedding model

---

## 3. Critical Technical Decisions & Solutions

### 3.1 Embedding Model Migration Issue

**Problem Encountered:**
- Initial implementation used `text-embedding-004` (768 dimensions)
- Database contained documents embedded with `embedding-001` (3072 dimensions)
- Dimension mismatch caused vector comparison errors

**Decision:** Standardize on `embedding-001` to match existing database.

**Rationale:**
- Re-embedding entire database would be time-consuming
- `embedding-001` provides higher dimensional representations
- Maintains backward compatibility with existing documents

**Code Configuration:**
```python
EMBEDDING_MODEL: str = "embedding-001"  # 3072 dimensions
GEMINI_MODEL: str = "gemini-2.0-flash"
```

**Lesson Learned:** Maintain version consistency between embeddings in database and query-time embeddings.

### 3.2 API Error Handling Strategy

**Decision:** Implement granular error detection with user-friendly messages.

**Implementation:**
```python
# Distinguish between different error types
if any(keyword in error_msg for keyword in ['exhausted', 'quota', 'rate limit', '429']):
    return "⚠️ API Rate Limit Exhausted..."
if 'not found' in error_msg or 'invalid' in error_msg:
    return "⚠️ Model Configuration Error..."
```

**Rationale:**
- **User clarity:** Generic "API error" messages are unhelpful
- **Debugging:** Specific errors help identify configuration issues
- **Recovery:** Users know whether to wait, reconfigure, or contact support

**Evolution:**
- Initially caught generic errors including "resource"
- Refined to distinguish between rate limits and model configuration errors
- Added debug logging for development troubleshooting

### 3.3 Casual Query Detection

**Decision:** Detect and handle casual queries differently from knowledge queries.

**Implementation:**
- Short queries (≤3 words) without question keywords treated as casual
- Casual queries get conversational responses without RAG overhead
- Reduces unnecessary embedding generation and database searches

**Rationale:**
- **Performance:** Avoids expensive RAG pipeline for "hello", "hey", etc.
- **User Experience:** More natural conversational flow
- **Cost:** Reduces API calls for non-informational queries

---

## 4. Document Processing Decisions

### 4.1 PDF-Only Restriction

**Decision:** Restrict uploads to PDF files only.

**Rationale:**
- **Consistency:** PDFs maintain formatting across platforms
- **Metadata:** PDFs support page numbers and structured content
- **Security:** Less variance in parsing libraries reduces attack surface
- **User Expectation:** Professional documents typically in PDF format

**Implementation:**
```python
if file_extension != '.pdf':
    raise HTTPException(status_code=400, detail="Only PDF files are allowed")
```

### 4.2 Chunking Strategy

**Decision:** 1000-character chunks with 200-character overlap.

**Rationale:**
- **Context preservation:** Overlap ensures sentences aren't split awkwardly
- **Embedding quality:** 1000 chars fits well within model context windows
- **Retrieval precision:** Smaller chunks allow more precise source attribution

**Trade-offs:**
- More chunks = more storage and processing
- Smaller chunks might lose broader context

### 4.3 Page Number Tracking

**Decision:** Store page numbers with each chunk for source attribution.

**Implementation:**
```python
page_number=metadata.get('page_number')
location = f"Page {page_number}, Lines {start_line}-{end_line}"
```

**Rationale:**
- **User trust:** Users can verify information in original documents
- **Citation quality:** Academic-style source attribution
- **Debugging:** Easier to identify problematic document sections

---

## 5. API Design Decisions

### 5.1 Endpoint Structure

**Decision:** RESTful API with clear resource separation.

**Endpoints:**
```
GET  /                          # Health check
POST /api/documents/upload      # Upload PDF
POST /api/documents/text        # Upload text
GET  /api/documents             # List documents
DELETE /api/documents/{id}      # Delete document
POST /api/query                 # Query knowledge base
```

**Rationale:**
- **Clarity:** Resource-based URLs are intuitive
- **Scalability:** Easy to extend with new endpoints
- **REST compliance:** Standard HTTP methods for operations

### 5.2 Response Format with Sources

**Decision:** Include source attribution in query responses.

**Response Structure:**
```json
{
  "answer": "The main answer text...",
  "sources": [
    {
      "document_name": "file.pdf",
      "chunk_text": "Relevant excerpt...",
      "relevance_score": 87.5,
      "page_number": 3,
      "start_line": 45,
      "end_line": 60
    }
  ],
  "query": "original user query",
  "timestamp": "2026-02-06T..."
}
```

**Rationale:**
- **Transparency:** Users see where information comes from
- **Trust:** Verifiable sources increase confidence
- **Relevance filtering:** Only show sources above 50% relevance

---

## 6. Configuration Management

### 6.1 Environment-Based Configuration

**Decision:** Use Pydantic Settings with `.env` files.

**Implementation:**
```python
class Settings(BaseSettings):
    GEMINI_API_KEY: str
    MONGODB_URI: str
    CORS_ORIGINS: str = "http://localhost:3000"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )
```

**Rationale:**
- **Security:** Secrets never committed to version control
- **Flexibility:** Easy environment switching (dev/staging/prod)
- **Type Safety:** Pydantic validates configuration at startup
- **Defaults:** Sensible defaults for optional settings

### 6.2 Configurable RAG Parameters

**Decision:** Make RAG pipeline tunable via configuration.

**Parameters:**
```python
CHUNK_SIZE: int = 1000
CHUNK_OVERLAP: int = 200
TOP_K_RESULTS: int = 3
MIN_RELEVANCE_SCORE: float = 50.0
```

**Rationale:**
- **Experimentation:** Tune for specific use cases without code changes
- **Performance:** Adjust trade-offs between quality and speed
- **Domain adaptation:** Different document types may need different settings

---

## 7. Error Recovery and Resilience

### 7.1 Graceful Degradation

**Decision:** Return partial results when possible rather than complete failure.

**Examples:**
- Embedding failures return zero vectors (allows processing to continue)
- Rate limit errors return friendly messages with retry guidance
- Missing sources still return generated answers

**Trade-off:** Potential for degraded quality vs. preventing total failure.

### 7.2 Service Instantiation Pattern

**Decision:** Singleton service instances initialized at module import.

**Implementation:**
```python
rag_service = RAGService()
document_service = DocumentService()
embedding_service = EmbeddingService()
```

**Implication:** Server restart required for configuration changes affecting service initialization.

**Rationale:**
- **Performance:** Avoid re-initialization on every request
- **Connection pooling:** Database connections persist
- **Simplicity:** No dependency injection framework needed

**Downside:** Less flexible than request-scoped services; requires restart for config changes.

---

## 8. User Experience Decisions

### 8.1 Real-Time Feedback

**Decision:** Immediate visual feedback for all user actions.

**Implementation:**
- Loading states during query processing
- Toast notifications for upload success/failure
- Streaming-like animation during AI responses
- API status indicator in UI

**Rationale:**
- **Perceived performance:** Users tolerate delays better with feedback
- **Error clarity:** Immediate notification of issues
- **Trust:** Visible system state builds confidence

### 8.2 Conversational Interface

**Decision:** Chat-style interface over form-based queries.

**Rationale:**
- **Familiarity:** Users comfortable with chat interfaces (ChatGPT, etc.)
- **Context:** Maintains conversation history visually
- **Natural:** More intuitive than traditional search boxes
- **Engagement:** Encourages exploration and follow-up questions

---

## 9. Deployment Decisions

### 9.1 Deployment Targets

**Backend:**
- **Primary:** Render.com (Python web service)
- **Alternative:** Local development with Uvicorn

**Frontend:**
- **Primary:** Vercel (Next.js optimized)
- **Alternative:** Standalone Docker deployment

**Database:**
- **Production:** MongoDB Atlas (managed cloud)

**Configuration Files:**
```
render.yaml        # Render deployment config
vercel.json        # Vercel deployment config
Procfile          # Process definition
requirements.txt  # Python dependencies
```

### 9.2 CORS Configuration

**Decision:** Explicitly configure allowed origins.

**Implementation:**
```python
CORS_ORIGINS: str = "http://localhost:3000"
# In production: "https://yourdomain.com"
```

**Rationale:**
- **Security:** Prevent unauthorized cross-origin requests
- **Flexibility:** Easy to add multiple allowed origins
- **Development:** Localhost for dev, production domain for prod

---

## 10. Performance Optimizations

### 10.1 Top-K Result Limiting

**Decision:** Default to top 3 most relevant documents, configurable up to 5.

**Rationale:**
- **Context window:** Avoid overwhelming LLM with too much context
- **Cost:** Fewer tokens consumed per request
- **Quality:** Most relevant results usually in top 3
- **Speed:** Faster processing with less context

### 10.2 Relevance Score Filtering

**Decision:** Filter sources below 50% relevance before LLM injection.

**Implementation:**
```python
if relevance < settings.MIN_RELEVANCE_SCORE:
    continue  # Skip this source
```

**Rationale:**
- **Quality:** Low-relevance sources dilute answer quality
- **Token efficiency:** Don't waste tokens on irrelevant context
- **User trust:** Only show meaningful sources

**Calculation:**
```python
# Convert cosine distance (0-2) to percentage (0-100%)
relevance = (1 - distance / 2) * 100
```

---

## 11. Security Considerations

### 11.1 API Key Management

**Decision:** Environment variables with `.env` files, never in code.

**Practice:**
- `.env` added to `.gitignore`
- `.env.example` provided as template
- Validation at startup (fail fast if missing)

### 11.2 File Upload Validation

**Decision:** Multiple layers of validation.

**Checks:**
1. File extension validation
2. MIME type checking
3. File size limits (10MB max)
4. PDF structure validation during parsing

**Rationale:**
- **Security:** Prevent malicious file uploads
- **Resource protection:** Avoid DoS via large files
- **User experience:** Clear error messages for invalid uploads

### 11.3 Input Sanitization

**Decision:** Rely on Pydantic models for request validation.

**Implementation:**
```python
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3
```

**Rationale:**
- **Type safety:** Automatic validation and type coercion
- **Consistency:** All endpoints use validated models
- **Documentation:** Models auto-generate OpenAPI schema

---

## 12. Monitoring and Debugging

### 12.1 Logging Strategy

**Decision:** Print-based logging with emoji indicators for development.

**Examples:**
```python
print(f"✅ Using Gemini embedding model: {self.model_name}")
print(f"🔍 RAG: Using top_k={top_k}")
print(f"🔴 CASUAL RESPONSE ERROR: {e}")
```

**Rationale:**
- **Visibility:** Easy to spot in console output
- **Categorization:** Emoji provides quick visual categorization
- **Development focus:** Sufficient for MVP/development phase

**Production Recommendation:** Migrate to structured logging (e.g., Python `logging` module) with log levels and external aggregation.

### 12.2 Error Visibility

**Decision:** Detailed error messages in development, user-friendly in production.

**Current Approach:**
- Full error details in server logs
- Sanitized, actionable messages to UI
- Debug prints for tracing execution flow

---

## 13. Lessons Learned & Future Improvements

### 13.1 Key Lessons

1. **Model Consistency:** Embedding model changes require full database re-indexing
2. **Server Lifecycle:** Module-level instantiation requires server restart for config changes
3. **Error Handling:** Granular error detection is essential for good UX
4. **Quota Management:** Free tier limitations require careful planning
5. **Multiple Servers:** Port conflicts cause requests to hit stale code

### 13.2 Recommended Improvements

#### Technical Debt
- [ ] Replace print statements with proper logging framework
- [ ] Add comprehensive unit and integration tests
- [ ] Implement request/response caching for repeated queries
- [ ] Add database connection pooling and retry logic
- [ ] Implement proper error tracking (e.g., Sentry)

#### Features
- [ ] Support for multiple document formats (DOCX, TXT, etc.)
- [ ] Conversation history and context retention
- [ ] Multi-document comparative queries
- [ ] User authentication and document access control
- [ ] Document versioning and update tracking

#### Performance
- [ ] Implement streaming responses for better perceived performance
- [ ] Add Redis caching layer for frequent queries
- [ ] Batch embedding generation for bulk uploads
- [ ] Optimize vector similarity search with dedicated vector DB

#### UX Enhancements
- [ ] Real-time typing indicators
- [ ] Export conversation history
- [ ] Highlighted source text in document viewer
- [ ] Query suggestions based on document content
- [ ] Dark mode support

---

## 14. Conclusion

This project demonstrates a production-capable RAG system using modern AI technologies. Key success factors include:

- **Clear architecture:** Separation of concerns (embedding, storage, retrieval, generation)
- **Flexible configuration:** Environment-based settings for easy deployment
- **User-centric design:** Chat interface with transparent source attribution
- **Error resilience:** Graceful degradation and helpful error messages
- **Scalable foundation:** MongoDB and cloud-native services enable growth

The technical decisions made prioritize:
1. **Time-to-market:** Leveraging managed services and free tiers
2. **User experience:** Conversational interface with clear feedback
3. **Maintainability:** Clean code structure and configuration management
4. **Extensibility:** Easy to add new features and document types

---

## Appendix: Technology Stack Summary

| Component | Technology | Version/Variant |
|-----------|-----------|------------------|
| **Backend Framework** | FastAPI | Latest |
| **Frontend Framework** | Next.js | 14 (App Router) |
| **AI - Embeddings** | Google Gemini | embedding-001 |
| **AI - Generation** | Google Gemini | gemini-2.0-flash |
| **Database** | MongoDB Atlas | Cloud |
| **Language - Backend** | Python | 3.11 |
| **Language - Frontend** | JavaScript/React | ES6+ |
| **Styling** | Tailwind CSS | Latest |
| **Animation** | Framer Motion | Latest |
| **PDF Processing** | PyPDF2 | Latest |
| **HTTP Client** | Axios | Latest |
| **Server** | Uvicorn | ASGI |
| **Deployment - Backend** | Render.com | - |
| **Deployment - Frontend** | Vercel | - |

---

**Document Version:** 1.0  
**Last Updated:** February 6, 2026  
**Author:** Kanishk Kumar, NSUT
