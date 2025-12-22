# Railway Deployment - Quick Fix Guide

## The Problem
Railway is trying to auto-detect your app (Railpack) but can't find how to build it. Your project uses Docker, so we need to configure Railway to use Dockerfiles.

## Solution: Deploy as 2 Separate Services

Railway doesn't support docker-compose directly. Deploy backend and frontend as **separate services**.

---

## Step-by-Step Fix

### Step 1: Delete Failed Service (if any)
- In Railway dashboard, delete the failed service

### Step 2: Create Backend Service

1. **Click "New" → "Service"**
2. **Select "GitHub Repo"** → Choose `Rramka/ToDo_Prioritizer`
3. **Configure:**
   - **Name:** `backend` (or `todo-prioritizer-backend`)
   - **Root Directory:** `backend`
   - **Settings → Build:**
     - **Builder:** Select "Dockerfile"
     - **Dockerfile Path:** `backend/Dockerfile` (or just `Dockerfile` since root is backend)
   - **Settings → Deploy:**
     - **Start Command:** Leave empty (Dockerfile has CMD)
4. **Environment Variables:**
   - Click "Variables" tab
   - Add:
     ```
     OPENAI_API_KEY=your_openai_key_here
     FRONTEND_URL=https://your-frontend-url.railway.app
     ```
   - Note: `PORT` is set automatically by Railway
5. **Deploy:**
   - Railway will build and deploy
   - Wait for it to finish
   - Copy the **Service URL** (e.g., `https://backend-production-xxxx.up.railway.app`)

### Step 3: Create Frontend Service

1. **Click "New" → "Service"** (in same project)
2. **Select "GitHub Repo"** → Choose `Rramka/ToDo_Prioritizer`
3. **Configure:**
   - **Name:** `frontend` (or `todo-prioritizer-frontend`)
   - **Root Directory:** `frontend`
   - **Settings → Build:**
     - **Builder:** Select "Dockerfile"
     - **Dockerfile Path:** `frontend/Dockerfile` (or just `Dockerfile`)
   - **Settings → Deploy:**
     - **Start Command:** Leave empty
4. **Environment Variables:**
   - Add:
     ```
     NEXT_PUBLIC_BACKEND_URL=https://backend-production-xxxx.up.railway.app
     ```
   - Use the backend URL you copied in Step 2
5. **Deploy:**
   - Railway will build and deploy
   - Get the frontend URL

### Step 4: Update Backend CORS

1. Go back to **Backend Service**
2. **Variables** tab
3. Update `FRONTEND_URL` to your frontend Railway URL
4. Railway will auto-redeploy

---

## Alternative: Use Nixpacks (No Docker)

If Docker doesn't work, Railway can auto-detect:

### Backend (Nixpacks):
1. **New Service** → GitHub Repo
2. **Root Directory:** `backend`
3. Railway will detect Python/FastAPI automatically
4. **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

### Frontend (Nixpacks):
1. **New Service** → GitHub Repo
2. **Root Directory:** `frontend`
3. Railway will detect Next.js automatically
4. Add `NEXT_PUBLIC_BACKEND_URL` environment variable

---

## Quick Checklist

- [ ] Backend service created with Dockerfile builder
- [ ] Backend root directory: `backend`
- [ ] Backend environment variables set (OPENAI_API_KEY, FRONTEND_URL)
- [ ] Backend deployed and URL copied
- [ ] Frontend service created with Dockerfile builder
- [ ] Frontend root directory: `frontend`
- [ ] Frontend environment variable set (NEXT_PUBLIC_BACKEND_URL = backend URL)
- [ ] Frontend deployed
- [ ] Both services running

---

## Troubleshooting

**Build fails:**
- Check build logs in Railway
- Verify Dockerfile syntax
- Ensure root directory is correct

**Services can't connect:**
- Verify `NEXT_PUBLIC_BACKEND_URL` matches backend service URL
- Check CORS settings in backend
- Verify `FRONTEND_URL` in backend matches frontend URL

**Port errors:**
- Railway sets `$PORT` automatically
- Dockerfiles updated to use `$PORT` variable
- Don't hardcode ports

**Still getting Railpack error:**
- Make sure Builder is set to "Dockerfile" not "Nixpacks"
- Check Root Directory is correct
- Verify Dockerfile exists in that directory

---

## Your Live URLs

After deployment:
- **Backend:** `https://backend-production-xxxx.up.railway.app`
- **Frontend:** `https://frontend-production-xxxx.up.railway.app`
- **API Docs:** `https://backend-production-xxxx.up.railway.app/docs`

---

## Need Help?

Check Railway logs:
- Click on service → "Deployments" → Click latest deployment → "View Logs"

Common issues:
1. Wrong root directory → Fix in Settings
2. Missing environment variables → Add in Variables tab
3. Dockerfile not found → Check Builder settings
4. Port conflicts → Railway handles this automatically

