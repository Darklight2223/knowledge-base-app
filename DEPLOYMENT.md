# Deployment Guide

Complete guide for deploying the AI Knowledge Base platform to production.

## 🎯 Deployment Options

1. **Docker Compose** (Easiest - Recommended)
2. **Cloud Platforms** (Scalable)
   - Vercel + Google Cloud Run
   - AWS (ECS + Amplify)
   - Azure (Container Apps)
3. **Manual VPS** (Full control)

---

## 1️⃣ Docker Compose Deployment

### Prerequisites
- Docker and Docker Compose installed
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

### Steps

```bash
# 1. Clone the repository
git clone your-repo-url
cd crud

# 2. Set environment variables
cp .env.example .env
# Edit .env and add GEMINI_API_KEY

# 3. Build and run
docker-compose up -d --build

# 4. Check logs
docker-compose logs -f

# 5. Access
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Production Configuration

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
    restart: always
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - CORS_ORIGINS=https://yourdomain.com
    volumes:
      - backend-data:/app/chroma_db
    labels:
      - "traefik.enable=true"
      # Add Traefik labels for SSL

  frontend:
    build:
      context: ./myapp
    restart: always
    environment:
      - NEXT_PUBLIC_API_URL=https://api.yourdomain.com
    labels:
      - "traefik.enable=true"

volumes:
  backend-data:
```

Run with:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 2️⃣ Vercel + Google Cloud Run

### Frontend to Vercel

```bash
cd myapp

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Add environment variable in Vercel dashboard
# NEXT_PUBLIC_API_URL=https://your-backend-url.run.app
```

### Backend to Google Cloud Run

```bash
cd backend

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/kb-backend

# Deploy
gcloud run deploy kb-backend \
  --image gcr.io/YOUR_PROJECT_ID/kb-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,CORS_ORIGINS=https://your-frontend.vercel.app \
  --memory 2Gi \
  --cpu 2

# Get the URL
gcloud run services describe kb-backend --region us-central1 --format 'value(status.url)'
```

Update Vercel environment variable with the Cloud Run URL.

---

## 3️⃣ AWS Deployment

### Frontend to AWS Amplify

1. Push code to GitHub
2. Go to AWS Amplify Console
3. Connect repository
4. Configure build:
   ```yaml
   version: 1
   frontend:
     phases:
       preBuild:
         commands:
           - cd myapp
           - npm ci
       build:
         commands:
           - npm run build
     artifacts:
       baseDirectory: myapp/.next
       files:
         - '**/*'
     cache:
       paths:
         - myapp/node_modules/**/*
   ```
5. Add environment variable: `NEXT_PUBLIC_API_URL`

### Backend to AWS ECS

```bash
# 1. Create ECR repository
aws ecr create-repository --repository-name kb-backend

# 2. Build and push
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker build -t kb-backend ./backend
docker tag kb-backend:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/kb-backend:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/kb-backend:latest

# 3. Create ECS task definition and service (via AWS Console or CloudFormation)
```

---

## 4️⃣ Azure Deployment

### Frontend to Azure Static Web Apps

```bash
cd myapp

# Install Azure Static Web Apps CLI
npm install -g @azure/static-web-apps-cli

# Deploy
swa deploy --app-location . --output-location .next
```

### Backend to Azure Container Apps

```bash
# Create resource group
az group create --name kb-rg --location eastus

# Create container registry
az acr create --resource-group kb-rg --name kbregistry --sku Basic

# Build and push
az acr build --registry kbregistry --image kb-backend ./backend

# Create container app
az containerapp create \
  --name kb-backend \
  --resource-group kb-rg \
  --image kbregistry.azurecr.io/kb-backend:latest \
  --target-port 8000 \
  --ingress external \
  --env-vars GEMINI_API_KEY=your_key
```

---

## 5️⃣ Manual VPS Deployment

### Prerequisites
- Ubuntu 22.04 VPS
- Domain name pointing to VPS IP
- SSH access

### Setup

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install dependencies
sudo apt update
sudo apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx

# 3. Clone repository
git clone your-repo-url /opt/kb-platform
cd /opt/kb-platform

# 4. Set environment variables
cp .env.example .env
nano .env  # Add your GEMINI_API_KEY

# 5. Run with Docker Compose
docker-compose up -d

# 6. Configure Nginx
sudo nano /etc/nginx/sites-available/kb-platform
```

Nginx configuration:

```nginx
# Frontend
server {
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Backend
server {
    server_name api.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kb-platform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

## 🔒 Security Checklist

### Before Going Live

- [ ] Change all default passwords
- [ ] Set strong `SECRET_KEY` for backend
- [ ] Enable HTTPS/SSL everywhere
- [ ] Configure CORS properly (no wildcards)
- [ ] Set up rate limiting
- [ ] Enable firewall (UFW/Security Groups)
- [ ] Regular backups of vector database
- [ ] Monitor API usage and costs
- [ ] Set up logging and monitoring
- [ ] Review Gemini API quotas

### Environment Variables Security

**Never commit:**
- `.env` files
- API keys
- Secrets

**Use secret management:**
- AWS Secrets Manager
- Google Secret Manager
- Azure Key Vault
- HashiCorp Vault

---

## 📊 Monitoring

### Application Monitoring

Add to backend `requirements.txt`:
```
prometheus-client==0.19.0
```

Add monitoring endpoint in `app/main.py`:
```python
from prometheus_client import Counter, Histogram, generate_latest

query_counter = Counter('queries_total', 'Total queries')
query_duration = Histogram('query_duration_seconds', 'Query duration')

@app.get("/metrics")
def metrics():
    return Response(generate_latest())
```

### Log Aggregation

Use:
- **Datadog**
- **New Relic**
- **ELK Stack**
- **Grafana + Loki**

---

## 💾 Backup Strategy

### Vector Database

```bash
# Backup
tar -czf chroma_db_backup_$(date +%Y%m%d).tar.gz backend/chroma_db/

# Restore
tar -xzf chroma_db_backup_20260205.tar.gz
```

### Automated Backups

Cron job:
```bash
0 2 * * * cd /opt/kb-platform && tar -czf /backups/chroma_db_$(date +\%Y\%m\%d).tar.gz backend/chroma_db/
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

`.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Cloud Run
        uses: google-github-actions/deploy-cloudrun@v1
        with:
          service: kb-backend
          image: gcr.io/${{ secrets.GCP_PROJECT }}/kb-backend
          credentials: ${{ secrets.GCP_SA_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## 📈 Scaling Considerations

### Horizontal Scaling

- **Backend**: Multiple instances behind load balancer
- **Frontend**: CDN + edge functions
- **Database**: Consider dedicated vector DB (Pinecone, Weaviate)

### Performance Optimization

1. **Caching**: Redis for frequent queries
2. **Queue**: Bull/Celery for async document processing
3. **CDN**: CloudFront/Cloudflare for static assets
4. **Database**: Connection pooling

---

## 🆘 Troubleshooting Deployment

### Container won't start
```bash
docker-compose logs backend
docker-compose logs frontend
```

### CORS errors in production
Update `backend/.env`:
```
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### High memory usage
Increase Docker memory limits or upgrade instance.

### Slow responses
- Check Gemini API quotas
- Add caching layer
- Optimize chunk size/overlap

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Review main README
3. Check cloud provider documentation
4. Open an issue with deployment details

---

**Ready to deploy!** Choose your platform and follow the guide above. 🚀
