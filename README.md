# AI Knowledge Base & Customer Service Copilot

A full-stack AI-powered knowledge base platform with RAG (Retrieval Augmented Generation) capabilities, built with Next.js and FastAPI, powered by Google Gemini.

## 🌐 Live Demo

- **Frontend:** https://knowledge-base-app-2k5o.vercel.app/
- **Backend API:** https://knowledge-base-app-1.onrender.com/
- **API Docs:** https://knowledge-base-app-1.onrender.com/docs

![Knowledge Base Screenshot](https://via.placeholder.com/800x400/4F46E5/FFFFFF?text=AI+Knowledge+Base+Platform)

## 🚀 Features

### Core Capabilities
- 📚 **Document Ingestion**: Upload and index PDF, TXT, and Markdown files
- 🤖 **AI-Powered Q&A**: Get intelligent answers grounded in your documents
- 📖 **Source Citations**: Every answer includes clear source references with relevance scores
- 🔍 **Vector Search**: Efficient similarity search using ChromaDB
- 💬 **Interactive Chat**: Modern chat interface with real-time responses
- 📊 **Document Management**: Easy upload, view, and delete operations

### Technical Features
- ⚡ **RAG Pipeline**: Advanced retrieval-augmented generation
- 🎨 **Modern UI**: Beautiful, responsive design with dark mode
- 🔄 **Real-time Updates**: Live status indicators and notifications
- 📱 **Mobile Responsive**: Works perfectly on all devices
- 🎭 **Smooth Animations**: Framer Motion for delightful UX
- 🔐 **Ready to Deploy**: Docker support with production configs

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│   Next.js UI    │──────│  FastAPI Server │──────│  Gemini API     │
│   (Frontend)    │ REST │    (Backend)    │ RAG  │  (LLM + Embed)  │
└─────────────────┘      └─────────────────┘      └─────────────────┘
                                │
                                │
                         ┌──────┴──────┐
                         │  ChromaDB   │
                         │  (Vectors)  │
                         └─────────────┘
```

### Tech Stack

**Frontend:**
- Next.js 16 (React 19)
- Tailwind CSS 4
- Framer Motion
- React Markdown
- Axios

**Backend:**
- FastAPI (Python 3.11+)
- Google Gemini AI
- ChromaDB (Vector Database)
- PyPDF2 (PDF Processing)
- Pydantic (Validation)

## 📋 Prerequisites

- **Node.js** 20+ and npm
- **Python** 3.11+
- **Google Gemini API Key** ([Get one here](https://makersuite.google.com/app/apikey))
- **Docker** (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Backend Setup

```powershell
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
# Edit .env.example and add your GEMINI_API_KEY
```

### 2. Frontend Setup

```powershell
cd myapp

# Install dependencies
npm install

# Environment is already configured in .env.local
```

### 3. Run Locally (Development)

**Terminal 1 - Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```powershell
cd myapp
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 5. Deploy to Production

See **[VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)** for complete deployment guide:
- Frontend → Vercel (1-click deploy)
- Backend → Google Cloud Run / Railway / Render

## 📖 Usage Guide

### Upload Documents

1. Click **"Documents"** in the sidebar
2. Click **"Upload Document"** button
3. Select a PDF, TXT, or MD file (max 10MB)
4. Document is automatically:
   - Split into chunks
   - Embedded using Gemini
   - Indexed in vector database

### Ask Questions

1. Click **"Chat"** in the sidebar
2. Type your question
3. Get an AI-generated answer with:
   - Relevant information from your documents
   - Source citations with relevance scores
   - Clear, well-formatted responses

### Sample Questions to Try

After uploading the sample documents:

- "What are the pricing plans available?"
- "How do I integrate the API?"
- "What's the refund policy?"
- "How to troubleshoot authentication issues?"
- "What are the response time standards?"

## 🎨 Customization

### Update API URL

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

**Backend (.env):**
```env
CORS_ORIGINS=https://your-frontend-url.com
```

### Modify RAG Settings

Edit `backend/app/config.py`:

```python
CHUNK_SIZE = 1000          # Document chunk size
CHUNK_OVERLAP = 200        # Overlap between chunks
TOP_K_RESULTS = 5          # Number of sources to retrieve
GEMINI_MODEL = "gemini-1.5-pro-latest"
```

### Customize UI Theme

Edit `myapp/src/app/globals.css` for colors and styles.

## 🚢 Deployment

### Quick Deploy to Production

**Frontend (Vercel):**
1. Push code to GitHub
2. Import to [Vercel](https://vercel.com/new)
3. Set root directory: `myapp`
4. Add env: `NEXT_PUBLIC_API_URL`
5. Deploy! ✅

**Backend (Cloud Run):**
```powershell
cd backend
gcloud run deploy kb-backend `
  --source . `
  --allow-unauthenticated `
  --set-env-vars "GEMINI_API_KEY=your_key"
```

**Or use Railway/Render** - See [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) for details.

### Complete Deployment Guide

📖 **[VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)** - Step-by-step deployment guide

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
GEMINI_API_KEY=your_gemini_api_key
CHROMA_PERSIST_DIRECTORY=./chroma_db
UPLOAD_DIR=./uploads
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/documents/upload` - Upload a file
- `POST /api/documents/text` - Upload text directly
- `POST /api/query` - Ask a question
- `GET /api/documents` - List all documents
- `DELETE /api/documents/{id}` - Delete a document

## 🧪 Testing

### Test the Backend

```bash
cd backend

# Query the API
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the pricing plans?"}'
```

### Test Document Upload

```bash
curl -X POST http://localhost:8000/api/documents/upload \
  -F "file=@sample_docs/product_documentation.txt"
```

## 📊 Project Structure

```
crud/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configuration
│   │   ├── models.py          # Pydantic models
│   │   └── services/
│   │       ├── embedding_service.py   # Gemini embeddings
│   │       ├── document_service.py    # Document management
│   │       └── rag_service.py         # RAG pipeline
│   ├── sample_docs/           # Sample documents
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── myapp/                     # Next.js Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.js        # Main page
│   │   │   ├── layout.js      # Root layout
│   │   │   └── globals.css    # Global styles
│   │   └── components/
│   │       ├── KnowledgeBaseChat.jsx    # Main chat
│   │       ├── ChatMessage.jsx          # Message display
│   │       └── DocumentManager.jsx      # Doc management
│   ├── package.json
│   ├── Dockerfile
│   └── README.md
└── docker-compose.yml         # Docker orchestration
```

## 🤝 Contributing

This is an assignment project, but suggestions are welcome!

## 📝 License

MIT License - feel free to use this for learning and projects.

## 🆘 Support & Troubleshooting

### Common Issues

**Q: "API Connection Failed"**
- Ensure backend is running on port 8000
- Check CORS settings in backend config
- Verify NEXT_PUBLIC_API_URL is set correctly

**Q: "Gemini API Key Error"**
- Get your API key from https://makersuite.google.com/app/apikey
- Add it to backend/.env (local) or environment variables (production)
- Restart the backend server

**Q: "No documents found"**
- Upload at least one document first
- Check backend/chroma_db directory exists
- Verify file upload completed successfully

**Q: "Slow responses"**
- Gemini API has rate limits on free tier
- Consider upgrading to paid tier
- Reduce TOP_K_RESULTS in config

### Documentation Links

- **Deployment**: [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md) - Production deployment guide
- **Quick Start**: [QUICKSTART.md](QUICKSTART.md) - Get started in 5 minutes
- **Backend**: [backend/README.md](backend/README.md) - API documentation
- **Frontend**: [myapp/README.md](myapp/README.md) - UI customization
- **Gemini API**: https://ai.google.dev/docs
- **Vercel**: https://vercel.com/docs

## 🎯 Future Enhancements

- [ ] Multi-user support with authentication
- [ ] Conversation history persistence
- [ ] Advanced file types (DOCX, Excel, etc.)
- [ ] Real-time collaboration
- [ ] Custom model fine-tuning
- [ ] Analytics dashboard
- [ ] Export conversations
- [ ] API rate limiting
- [ ] Caching layer

## � Deploy Now

Ready to go live? Follow the deployment guide:

**👉 [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)**

- Frontend on Vercel (free, auto-SSL, CDN)
- Backend on Cloud Run/Railway/Render
- Production-ready in minutes

## 🙏 Acknowledgments

- **Google Gemini** for powerful AI capabilities
- **ChromaDB** for efficient vector storage
- **Vercel** for seamless frontend hosting
- **Next.js** and **FastAPI** teams for excellent frameworks

---

**Built with ❤️ for Assignment 2: AI Platform – Knowledge Base & Customer Service Copilot**

*Vercel-Ready • Ultra-modern • Production-ready*
