# Railway Deployment Guide - ToDo Prioritizer

This guide will walk you through deploying your ToDo Prioritizer application on Railway with separate services for backend and frontend.

## Prerequisites

1. **Railway Account**: Sign up at [railway.app](https://railway.app) if you don't have one
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **OpenAI API Key**: You'll need an OpenAI API key for the backend service

## Architecture Overview

Your application will be deployed as **two separate Railway services**:
- **Backend Service**: FastAPI application (Python)
- **Frontend Service**: Next.js application (Node.js)

Each service will get its own Railway URL (e.g., `backend-production.up.railway.app` and `frontend-production.up.railway.app`).

---

## Step 1: Prepare Your Repository

Your repository is already configured with:
- ✅ `backend/Dockerfile` - Backend Docker configuration
- ✅ `frontend/Dockerfile` - Frontend Docker configuration
- ✅ `backend/railway.json` - Railway configuration for backend
- ✅ `frontend/railway.json` - Railway configuration for frontend
- ✅ `.railwayignore` - Files to exclude from deployment

**No changes needed** - your project is ready!

---

## Step 2: Create Railway Project

1. Go to [railway.app](https://railway.app) and log in
2. Click **"New Project"** button
3. Select **"Deploy from GitHub repo"**
4. Select your `ToDo_Prioritizer` repository
5. Railway will create a project and detect your repository structure

---

## Step 3: Deploy Backend Service

### 3.1 Create Backend Service

1. In your Railway project, click **"+ New"** → **"GitHub Repo"** (if not already added)
2. Select your repository
3. Railway will create a service, but we need to configure it

### 3.2 Configure Backend Service

1. Click on the newly created service (or the service representing your backend)
2. Go to **Settings** tab
3. In the **Source** section (right sidebar):
   - Set **Root Directory** to: `backend`
4. In the **Build** section (right sidebar):
   - **Builder**: Dockerfile (should be detected automatically)
   - **Dockerfile Path**: `Dockerfile` (relative to root directory)
5. **Save** the settings

### 3.3 Set Backend Environment Variables

1. Go to the **Variables** tab in your backend service
2. Click **"+ New Variable"** and add:

```
OPENAI_API_KEY=your_openai_api_key_here
```

3. Optionally, add:
```
OPENAI_MODEL=gpt-4o-mini
FRONTEND_URL=https://your-frontend-service.up.railway.app
```
   *Note: You'll update FRONTEND_URL after deploying the frontend service*

4. Click **Save**

### 3.4 Deploy Backend

1. Railway will automatically start building and deploying
2. Go to **Deployments** tab to watch the build progress
3. Once deployed, Railway will generate a public URL
4. Click on the **Settings** → **Generate Domain** to get a public URL like:
   - `backend-production-xxxx.up.railway.app`
5. **Copy this URL** - you'll need it for the frontend configuration

### 3.5 Verify Backend Deployment

1. Visit `https://your-backend-url.up.railway.app/health`
2. You should see: `{"status": "healthy"}`
3. Visit `https://your-backend-url.up.railway.app/docs` to see the API documentation

---

## Step 4: Deploy Frontend Service

### 4.1 Create Frontend Service

1. In your Railway project, click **"+ New"** → **"GitHub Repo"**
2. Select the **same repository** (`ToDo_Prioritizer`)
3. Railway will create a second service

### 4.2 Configure Frontend Service

1. Click on the frontend service
2. Go to **Settings** tab
3. In the **Source** section (right sidebar):
   - Set **Root Directory** to: `frontend`
4. In the **Build** section (right sidebar):
   - **Builder**: Dockerfile (should be detected automatically)
   - **Dockerfile Path**: `Dockerfile` (relative to root directory)
5. **Save** the settings

### 4.3 Set Frontend Environment Variables

1. Go to the **Variables** tab in your frontend service
2. Click **"+ New Variable"** and add:

```
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.up.railway.app
```

Replace `your-backend-url.up.railway.app` with the actual backend URL from Step 3.4.

3. Click **Save**

### 4.4 Update Backend CORS Configuration

1. Go back to your **Backend Service** → **Variables** tab
2. Update the `FRONTEND_URL` variable to your frontend URL:
   ```
   FRONTEND_URL=https://your-frontend-url.up.railway.app
   ```
   *You'll get the frontend URL after it deploys*

### 4.5 Deploy Frontend

1. Railway will automatically start building and deploying
2. The frontend build may take 3-5 minutes (Next.js build process)
3. Go to **Deployments** tab to watch the build progress
4. Once deployed, Railway will generate a public URL
5. Click on **Settings** → **Generate Domain** to get a public URL

### 4.6 Update Backend FRONTEND_URL

1. After frontend is deployed, copy the frontend URL
2. Go to **Backend Service** → **Variables** tab
3. Update `FRONTEND_URL` to the frontend URL:
   ```
   FRONTEND_URL=https://your-frontend-url.up.railway.app
   ```
4. Railway will automatically redeploy the backend with the updated CORS settings

---

## Step 5: Test Your Deployment

1. Visit your frontend URL (e.g., `https://frontend-production.up.railway.app`)
2. Try submitting some tasks to test the full workflow
3. Check the browser console for any errors
4. Verify API calls are working by checking the Network tab

---

## Environment Variables Reference

### Backend Service Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key | `sk-...` |
| `OPENAI_MODEL` | ❌ No | OpenAI model to use (default: `gpt-4o-mini`) | `gpt-4o-mini` |
| `FRONTEND_URL` | ❌ No | Frontend URL for CORS (set after frontend deploys) | `https://frontend-production.up.railway.app` |
| `PORT` | ❌ No | Port number (Railway sets this automatically) | `8000` |

### Frontend Service Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_BACKEND_URL` | ✅ Yes | Backend API URL | `https://backend-production.up.railway.app` |
| `PORT` | ❌ No | Port number (Railway sets this automatically) | `3000` |

---

## Troubleshooting

### Backend Build Fails

**Problem**: Build fails with "File not found" errors

**Solution**: 
- Check that **Root Directory** is set to `backend` in Settings → Source
- Check that **Dockerfile Path** is set to `Dockerfile` (not `/backend/Dockerfile`)

### Frontend Build Fails

**Problem**: Build fails with "File not found" errors

**Solution**:
- Check that **Root Directory** is set to `frontend` in Settings → Source
- Check that **Dockerfile Path** is set to `Dockerfile` (not `/frontend/Dockerfile`)

### Frontend Can't Connect to Backend

**Problem**: Frontend shows errors when trying to call the API

**Solution**:
1. Verify `NEXT_PUBLIC_BACKEND_URL` is set correctly in frontend variables
2. Verify backend is deployed and healthy (check `/health` endpoint)
3. Check browser console for CORS errors
4. If CORS errors, update `FRONTEND_URL` in backend variables

### Backend Returns CORS Errors

**Problem**: Browser shows CORS errors when frontend calls backend

**Solution**:
1. Verify `FRONTEND_URL` in backend variables matches your frontend Railway URL exactly
2. Make sure there's no trailing slash (use `https://frontend.up.railway.app` not `https://frontend.up.railway.app/`)
3. Redeploy the backend service after updating the variable

### Service Won't Start

**Problem**: Service deploys but shows as "unhealthy" or crashes

**Solution**:
1. Check the **Deployments** tab → Click on the deployment → View logs
2. Look for error messages in the logs
3. Common issues:
   - Missing environment variables (check all required vars are set)
   - Port conflicts (Railway sets PORT automatically, don't override)
   - Build failures (check build logs)

### OpenAI API Key Issues

**Problem**: Backend returns "OpenAI API key is not configured"

**Solution**:
1. Go to Backend Service → Variables
2. Verify `OPENAI_API_KEY` is set correctly
3. Make sure there are no extra spaces or quotes
4. Redeploy the service

---

## Custom Domains (Optional)

Railway provides free `.up.railway.app` domains. If you want to use a custom domain:

1. Go to Service → Settings → Domains
2. Click **"Custom Domain"**
3. Add your domain
4. Follow Railway's DNS instructions
5. Update environment variables with the new domain URLs

---

## Monitoring and Logs

### View Logs
1. Go to your Service → **Deployments** tab
2. Click on a deployment
3. View real-time logs

### Health Checks
- Backend: `https://your-backend-url/health`
- Frontend: `https://your-frontend-url/` (should return 200)

---

## Updating Your Application

Railway automatically deploys when you push to your connected GitHub branch:

1. Make changes to your code
2. Commit and push to GitHub
3. Railway detects the push
4. Automatically builds and deploys the new version
5. Monitor the deployment in the **Deployments** tab

---

## Cost Considerations

Railway offers:
- **Free tier**: $5/month credit (usually enough for small projects)
- **Hobby plan**: $20/month for more resources
- Check Railway pricing for current rates

**Tips to reduce costs**:
- Use `gpt-4o-mini` instead of `gpt-4o` (much cheaper)
- Enable sleep on inactivity for development services
- Monitor usage in Railway dashboard

---

## Next Steps

After successful deployment:
1. ✅ Test all functionality
2. ✅ Set up monitoring (optional)
3. ✅ Configure custom domains (optional)
4. ✅ Set up alerts (optional)
5. ✅ Document your production URLs

---

## Quick Reference Checklist

- [ ] Railway account created
- [ ] GitHub repository connected
- [ ] Backend service created and configured
- [ ] Backend Root Directory set to `backend`
- [ ] Backend Dockerfile Path set to `Dockerfile`
- [ ] `OPENAI_API_KEY` set in backend variables
- [ ] Backend deployed successfully
- [ ] Backend URL copied
- [ ] Frontend service created and configured
- [ ] Frontend Root Directory set to `frontend`
- [ ] Frontend Dockerfile Path set to `Dockerfile`
- [ ] `NEXT_PUBLIC_BACKEND_URL` set in frontend variables
- [ ] Frontend deployed successfully
- [ ] Frontend URL copied
- [ ] `FRONTEND_URL` updated in backend variables
- [ ] Application tested and working

---

## Support

If you encounter issues:
1. Check Railway deployment logs
2. Verify all environment variables are set correctly
3. Test endpoints directly (backend `/health`, `/docs`)
4. Check Railway status page: https://status.railway.app
5. Railway documentation: https://docs.railway.app

---

**Happy Deploying! 🚂**

