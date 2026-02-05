# 🚀 MongoDB Deployment Guide

## ✅ Setup Complete!

Your backend is now configured with MongoDB Atlas. Here's what was updated:

### Code Changes:
- ✅ Replaced ChromaDB with MongoDB
- ✅ PDFs stored as base64 in MongoDB
- ✅ Embeddings stored with chunks
- ✅ Vector search using cosine similarity
- ✅ Updated requirements.txt

---

## 📦 Next Steps: Deploy

### 1️⃣ Install MongoDB Package Locally
```powershell
cd c:\crud\backend
pip install pymongo numpy
```

### 2️⃣ Test Locally
```powershell
# Kill old backend
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force

# Start new backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3️⃣ Test Upload
- Go to http://localhost:3000
- Upload a PDF
- Ask a question
- Verify it works!

---

## 🚀 Deploy to Render

### Create GitHub Repository
```powershell
cd c:\crud\backend
git init
git add .
git commit -m "MongoDB integration complete"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### Deploy on Render.com
1. Go to render.com → New Web Service
2. Connect GitHub repo
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Environment Variables:
   ```
   GEMINI_API_KEY=AIzaSyA2ugeGf1DZHgNcwPD5lJtxOvou68cSunM
   MONGODB_URI=mongodb+srv://klk:Kanishk-05@knowledge-base.lpisiio.mongodb.net/?appName=knowledge-base
   CORS_ORIGINS=https://your-app.vercel.app
   ```
5. Click **Create Web Service**
6. Copy backend URL: `https://your-backend.onrender.com`

---

## 🎨 Deploy Frontend to Vercel

### Update API URL
```powershell
cd c:\crud\myapp
# Create .env.local if not exists
echo NEXT_PUBLIC_API_URL=https://your-backend.onrender.com > .env.local
```

### Deploy
```powershell
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_FRONTEND_REPO_URL
git push -u origin main
```

Then on Vercel:
1. Import repository
2. Add environment variable:
   - `NEXT_PUBLIC_API_URL` = `https://your-backend.onrender.com`
3. Deploy!

---

## ✅ Done!

Your AI Knowledge Base is live with:
- ✅ MongoDB Atlas (persistent storage)
- ✅ Render (backend API)
- ✅ Vercel (frontend)
- ✅ PDFs + vectors stored in cloud
