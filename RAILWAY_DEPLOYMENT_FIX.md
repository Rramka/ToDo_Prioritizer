# Railway Deployment Fix

## Problem
Railway is trying to use Railpack (auto-detection) but can't detect the build method. Our project uses Docker Compose.

## Solution: Deploy Services Separately

Railway works best when you deploy backend and frontend as **separate services** rather than using docker-compose.

### Option 1: Deploy Backend Service (Recommended)

1. **In Railway Dashboard:**
   - Go to your project
   - Click "New" → "Service"
   - Select "GitHub Repo" → Choose your repo

2. **Configure Backend Service:**
   - **Root Directory:** `backend`
   - **Build Command:** Leave empty (Railway will use Dockerfile)
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **OR** if using Dockerfile: Leave start command empty

3. **Environment Variables:**
   - `OPENAI_API_KEY` = your OpenAI key
   - `FRONTEND_URL` = (will be your frontend URL later)
   - `PORT` = (Railway sets this automatically)

4. **Deploy Settings:**
   - Railway should detect `backend/Dockerfile`
   - If not, set **Builder** to "Dockerfile"
   - **Dockerfile Path:** `backend/Dockerfile`

### Option 2: Deploy Frontend Service

1. **Create New Service:**
   - Click "New" → "Service"
   - Select same GitHub repo

2. **Configure Frontend Service:**
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Start Command:** `npm start` or leave empty if using Dockerfile
   - **OR** use Dockerfile: Set **Builder** to "Dockerfile"

3. **Environment Variables:**
   - `NEXT_PUBLIC_BACKEND_URL` = your backend service URL
   - `PORT` = (Railway sets automatically)

4. **Get Backend URL:**
   - Go to backend service → Settings → Domains
   - Copy the Railway-provided URL
   - Use this in `NEXT_PUBLIC_BACKEND_URL`

### Option 3: Use Nixpacks (Alternative)

If Docker doesn't work, Railway can auto-detect:

**For Backend:**
- Root Directory: `backend`
- Railway will detect Python/FastAPI
- Add `requirements.txt` in root or backend folder

**For Frontend:**
- Root Directory: `frontend`
- Railway will detect Next.js
- Should work automatically

## Quick Fix Steps

1. **Delete the failed service** (if any)

2. **Create Backend Service:**
   ```
   New Service → GitHub Repo
   Root Directory: backend
   Builder: Dockerfile
   Dockerfile Path: backend/Dockerfile
   ```

3. **Create Frontend Service:**
   ```
   New Service → GitHub Repo  
   Root Directory: frontend
   Builder: Dockerfile
   Dockerfile Path: frontend/Dockerfile
   ```

4. **Set Environment Variables:**
   - Backend: `OPENAI_API_KEY`, `FRONTEND_URL`
   - Frontend: `NEXT_PUBLIC_BACKEND_URL`

5. **Deploy!**

## Alternative: Use Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize
railway init

# Link to project
railway link

# Deploy backend
cd backend
railway up

# Deploy frontend (new terminal)
cd frontend
railway up
```

## Troubleshooting

**If Dockerfile not detected:**
- Go to Service → Settings → Build
- Set Builder to "Dockerfile"
- Set Dockerfile Path manually

**If build fails:**
- Check build logs
- Verify Dockerfile syntax
- Check environment variables are set

**If services can't connect:**
- Use Railway's internal service URLs
- Backend URL format: `https://backend-production-xxxx.up.railway.app`
- Frontend URL format: `https://frontend-production-xxxx.up.railway.app`

