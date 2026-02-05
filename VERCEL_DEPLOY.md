# Vercel Deployment Guide

Complete guide for deploying the AI Knowledge Base to Vercel.

## 🎯 Deployment Architecture

- **Frontend (Next.js)**: Vercel ✅
- **Backend (FastAPI)**: Google Cloud Run / Railway / Render

## 📋 Prerequisites

1. [Vercel Account](https://vercel.com/signup) (free tier works)
2. [Google Cloud Account](https://cloud.google.com) or [Railway](https://railway.app) for backend
3. GitHub repository with your code
4. Gemini API Key

---

## 🚀 Step 1: Deploy Backend

### Option A: Google Cloud Run (Recommended)

```powershell
# Install Google Cloud SDK first

# Login
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Deploy backend
cd backend
gcloud run deploy kb-backend `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "GEMINI_API_KEY=YOUR_KEY" `
  --memory 2Gi

# Get your backend URL
gcloud run services describe kb-backend --region us-central1 --format "value(status.url)"
```

Copy the URL - you'll need it for the frontend!

### Option B: Railway (Easiest)

1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Set root directory to `backend`
5. Add environment variables:
   ```
   GEMINI_API_KEY=your_key
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
6. Railway will auto-deploy and give you a URL

### Option C: Render

1. Go to [Render](https://render.com)
2. New Web Service → Connect repository
3. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variable: `GEMINI_API_KEY`
5. Deploy and copy the URL

---

## 🎨 Step 2: Deploy Frontend to Vercel

### Method 1: Vercel Dashboard (Easiest)

1. **Push to GitHub**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Import to Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Click "Import Git Repository"
   - Select your repository
   - Configure:
     - **Framework Preset**: Next.js
     - **Root Directory**: `myapp`
     - **Build Command**: `npm run build`
     - **Output Directory**: `.next`

3. **Add Environment Variable**
   - Click "Environment Variables"
   - Add: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.run.app`
   - Click "Deploy"

4. **Done!** 🎉
   - Your site will be at `https://your-project.vercel.app`

### Method 2: Vercel CLI

```powershell
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Navigate to frontend
cd myapp

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: kb-frontend
  - In which directory is your code? ./
# - Override settings? No

# Add environment variable
vercel env add NEXT_PUBLIC_API_URL

# Paste your backend URL when prompted

# Deploy to production
vercel --prod
```

---

## 🔧 Step 3: Configure CORS

Update your backend environment variables to allow your Vercel frontend:

**Google Cloud Run:**
```powershell
gcloud run services update kb-backend `
  --update-env-vars "CORS_ORIGINS=https://your-project.vercel.app"
```

**Railway/Render:**
- Go to environment variables
- Update `CORS_ORIGINS` to `https://your-project.vercel.app`

---

## ✅ Step 4: Verify Deployment

1. Visit your Vercel URL: `https://your-project.vercel.app`
2. Check the status indicator (should be green 🟢)
3. Try uploading a document
4. Ask a question

---

## 🔄 Continuous Deployment

Both Vercel and Cloud Run/Railway will auto-deploy on git push!

```powershell
# Make changes
git add .
git commit -m "Update feature"
git push

# Vercel automatically deploys frontend
# Railway/Render automatically deploys backend
```

---

## 💾 Environment Variables Summary

### Frontend (Vercel)
```
NEXT_PUBLIC_API_URL=https://your-backend-url
```

### Backend (Cloud Run/Railway/Render)
```
GEMINI_API_KEY=your_gemini_api_key
CORS_ORIGINS=https://your-project.vercel.app
```

---

## 🎯 Custom Domain (Optional)

### Vercel Frontend

1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as shown
4. SSL is automatic!

### Backend Domain

**Cloud Run:**
```powershell
gcloud run domain-mappings create `
  --service kb-backend `
  --domain api.yourdomain.com
```

Then update DNS with the provided records.

---

## 📊 Monitoring & Logs

### Vercel
- **Logs**: Project → Deployments → Click deployment → Logs
- **Analytics**: Built-in analytics dashboard

### Cloud Run
```powershell
gcloud run services logs read kb-backend --limit 50
```

### Railway/Render
- View logs directly in the dashboard

---

## 💰 Pricing Estimates

### Free Tier Generous Limits

**Vercel:**
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless functions

**Google Cloud Run:**
- ✅ 2 million requests/month free
- ✅ 180,000 vCPU-seconds/month
- ✅ 360,000 GiB-seconds/month

**Railway:**
- ✅ $5 free credit/month
- ⚠️ Credit-based after that

**Render:**
- ✅ Free tier for web services
- ⚠️ Spins down after inactivity

---

## 🐛 Troubleshooting

### "API Connection Failed"

1. Check backend is deployed and running
2. Verify `NEXT_PUBLIC_API_URL` in Vercel
3. Check CORS settings on backend
4. Open browser console for errors

### "CORS Error"

Update backend `CORS_ORIGINS`:
```
CORS_ORIGINS=https://your-project.vercel.app,https://your-project-git-main-username.vercel.app
```

### "Build Failed on Vercel"

1. Check build logs in Vercel dashboard
2. Verify `package.json` scripts
3. Ensure all dependencies are listed
4. Try building locally: `npm run build`

### Backend Cold Starts

Free tier services may "sleep":
- **Cloud Run**: Always on (in limits)
- **Railway**: Always on with credit
- **Render**: Spins down after 15min inactivity

Upgrade to paid tier for always-on.

---

## 🎓 Project URLs

After deployment:

- **Frontend**: `https://your-project.vercel.app`
- **Backend**: `https://kb-backend-xxxxx.run.app` (Cloud Run)
- **API Docs**: `https://kb-backend-xxxxx.run.app/docs`

---

## 🚀 Quick Deploy Commands

### Full Deployment (All in one)

```powershell
# 1. Deploy Backend to Cloud Run
cd backend
gcloud run deploy kb-backend --source . --allow-unauthenticated --set-env-vars "GEMINI_API_KEY=YOUR_KEY"

# 2. Get backend URL
$BACKEND_URL = gcloud run services describe kb-backend --format "value(status.url)"

# 3. Deploy Frontend to Vercel
cd ../myapp
vercel --prod -e NEXT_PUBLIC_API_URL=$BACKEND_URL

# 4. Update CORS
gcloud run services update kb-backend --update-env-vars "CORS_ORIGINS=https://your-project.vercel.app"
```

---

## 📞 Support

- **Vercel Docs**: https://vercel.com/docs
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **Railway Docs**: https://docs.railway.app
- **Render Docs**: https://render.com/docs

---

**You're ready to deploy!** 🎉

Choose your backend platform and follow the steps above.
