# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

### Step 1: Get a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key

### Step 2: Configure Backend

```bash
cd backend
cp .env.example .env
```

Edit `backend/.env` and add your key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd myapp
npm install
```

### Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd myapp
npm run dev
```

### Step 5: Open Your Browser

Visit: http://localhost:3000

## 🎯 First Steps

### 1. Upload Sample Documents

Three sample documents are included in `backend/sample_docs/`:

- `product_documentation.txt` - Product info and features
- `company_policies.txt` - Policies and guidelines
- `troubleshooting_guide.txt` - Common issues and solutions

**Upload via UI:**
1. Click "Documents" in sidebar
2. Click "Upload Document"
3. Select files from `backend/sample_docs/`

**Or load programmatically:**
```bash
cd backend
python scripts/load_sample_docs.py
```

### 2. Ask Questions

Click "Chat" and try these:

```
What are the pricing plans available?
```

```
How do I troubleshoot API authentication issues?
```

```
What's the company refund policy?
```

```
What are the supported file types for the chat widget?
```

## � Deploy to Production

See **[VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)** for:
- Deploy frontend to Vercel (free)
- Deploy backend to Cloud Run/Railway/Render
- Complete step-by-step guide

## ⚡ Windows PowerShell Quick Start

```powershell
# Backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Add your API key to backend\.env

# Run backend
python -m uvicorn app.main:app --reload

# Frontend (new terminal)
cd myapp
npm install
npm run dev
```

## ✅ Verify Installation

### Check Backend

Visit http://localhost:8000/docs

You should see the API documentation.

### Check Frontend

Visit http://localhost:3000

You should see the chat interface.

### Test API Connection

In the UI, check the status indicator in the sidebar:
- 🟢 Green = API Connected (Ready!)
- 🟡 Yellow = API Key Not Set
- 🔴 Red = API Offline

## 🔥 Common Issues

### "ModuleNotFoundError"
```bash
cd backend
pip install -r requirements.txt
```

### "CORS Error"
Check that `backend/.env` has:
```
CORS_ORIGINS=http://localhost:3000
```

### "API Key Error"
Verify your Gemini API key in `backend/.env`

### Port Already in Use
Change ports in:
- Backend: `--port 8001` instead of 8000
- Frontend: Update `.env.local` to match

## 📚 What's Next?

1. **Explore Features**: Try uploading your own documents
2. **Customize**: Modify the UI in `myapp/src/components/`
3. **Deploy**: Follow the deployment guide in main README
4. **Extend**: Add new features to the RAG pipeline

## 🎓 Learning Resources

- [Main README](README.md) - Complete documentation
- [Backend README](backend/README.md) - API details
- [Frontend README](myapp/README.md) - UI customization
- [Gemini API Docs](https://ai.google.dev/docs) - AI capabilities

---

**Need Help?** Check the troubleshooting section in the main README or open an issue.
