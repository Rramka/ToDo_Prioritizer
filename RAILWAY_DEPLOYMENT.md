# Railway Deployment Guide

## Quick Start

Railway requires **separate services** for backend and frontend. Follow these steps:

### Step 1: Create Backend Service

1. Go to your Railway project dashboard
2. Click **"New"** → **"Empty Service"**
3. Name it: `backend`
4. Go to **Settings** → **Source**:
   - **Root Directory:** `backend`
5. Go to **Settings** → **Docker**:
   - Enable **"Use Dockerfile"**
   - **Dockerfile Path:** `Dockerfile` (relative to root directory)
6. Go to **Settings** → **Deploy**:
   - **Start Command:** (leave empty - Dockerfile CMD handles it)
7. Go to **Variables** and add:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o-mini
   FRONTEND_URL=https://your-frontend-service.railway.app
   PORT=8000
   ```
8. Go to **Settings** → **Networking**:
   - Generate a domain (e.g., `backend-production.up.railway.app`)
   - Copy this URL - you'll need it for the frontend

### Step 2: Create Frontend Service

1. In the same Railway project, click **"New"** → **"Empty Service"**
2. Name it: `frontend`
3. Go to **Settings** → **Source**:
   - **Root Directory:** `frontend`
4. Go to **Settings** → **Docker**:
   - Enable **"Use Dockerfile"**
   - **Dockerfile Path:** `Dockerfile` (relative to root directory)
5. Go to **Settings** → **Deploy**:
   - **Start Command:** (leave empty - Dockerfile CMD handles it)
6. Go to **Variables** and add:
   ```
   NEXT_PUBLIC_BACKEND_URL=https://your-backend-service.railway.app
   PORT=3000
   NODE_ENV=production
   ```
   **Important:** Replace `your-backend-service.railway.app` with the actual backend URL from Step 1
7. Go to **Settings** → **Networking**:
   - Generate a domain (e.g., `frontend-production.up.railway.app`)

### Step 3: Update Backend CORS

After getting the frontend URL, update the backend service:
1. Go to **backend** service → **Variables**
2. Update `FRONTEND_URL` to match your frontend Railway URL

### Step 4: Deploy

Both services will automatically deploy when you push to your connected GitHub branch.

## Environment Variables Summary

### Backend Service
- `OPENAI_API_KEY` (required) - Your OpenAI API key
- `OPENAI_MODEL` (optional) - Default: `gpt-4o-mini`
- `FRONTEND_URL` (required) - Frontend Railway URL for CORS
- `PORT` (optional) - Railway automatically provides this

### Frontend Service
- `NEXT_PUBLIC_BACKEND_URL` (required) - Backend Railway URL
- `PORT` (optional) - Railway automatically provides this
- `NODE_ENV` (optional) - Set to `production`

## Troubleshooting

### Issue: "Railpack could not determine how to build the app"
**Solution:** Make sure:
- Docker is enabled in service settings
- Root directory is set correctly (`backend` or `frontend`)
- Dockerfile exists in the root directory

### Issue: "Script start.sh not found"
**Solution:** This is normal - Railway will use the Dockerfile CMD instead. Make sure Docker is enabled.

### Issue: Build fails
**Solution:**
1. Check build logs in Railway dashboard
2. Verify all environment variables are set
3. Ensure Dockerfiles are correct
4. Check that `requirements.txt` and `package.json` are in the correct directories

### Issue: Services can't communicate
**Solution:**
1. Use the Railway-generated URLs (not localhost)
2. Update `NEXT_PUBLIC_BACKEND_URL` in frontend with backend URL
3. Update `FRONTEND_URL` in backend with frontend URL
4. Ensure CORS is configured correctly in backend

## Manual Deployment via Railway CLI

If you prefer using CLI:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy backend
railway service --service backend
railway up

# Deploy frontend
railway service --service frontend
railway up
```

## Notes

- Railway automatically provides a `PORT` environment variable
- Both Dockerfiles are configured to use this PORT
- Services are deployed separately but can communicate via Railway's internal network
- Use Railway-generated URLs for service-to-service communication
- CORS must be configured with the actual frontend URL

