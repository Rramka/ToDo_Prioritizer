# Railway Fix: Force Docker Instead of Railpack

## The Problem
Railway is trying to use Railpack (auto-detection) instead of Docker, which causes the error:
- "Railpack could not determine how to build the app"
- "Script start.sh not found"

## The Solution

**You MUST configure the service in Railway Dashboard:**

### Step 1: Delete Current Service (if needed)
1. Go to your Railway project
2. Delete the current "ToDo_Prioritizer" service that's failing

### Step 2: Create Backend Service
1. Click **"New"** → **"Empty Service"**
2. Name it: `backend`
3. **CRITICAL STEP:** Go to **Settings** → **Source**
   - Set **Root Directory** to: `backend`
   - This tells Railway to look in the `backend/` folder
4. Go to **Settings** → **Docker**
   - **Enable "Use Dockerfile"** (toggle it ON)
   - **Dockerfile Path:** `Dockerfile` (this is relative to the root directory)
5. Go to **Settings** → **Deploy**
   - **Start Command:** (leave empty - Dockerfile CMD handles it)
6. Add **Variables:**
   ```
   OPENAI_API_KEY=your_key_here
   OPENAI_MODEL=gpt-4o-mini
   FRONTEND_URL=https://your-frontend-url.railway.app
   PORT=8000
   ```
7. Go to **Settings** → **Networking**
   - Generate a domain
   - Copy the URL (you'll need it for frontend)

### Step 3: Create Frontend Service
1. Click **"New"** → **"Empty Service"**
2. Name it: `frontend`
3. **CRITICAL STEP:** Go to **Settings** → **Source**
   - Set **Root Directory** to: `frontend`
   - This tells Railway to look in the `frontend/` folder
4. Go to **Settings** → **Docker**
   - **Enable "Use Dockerfile"** (toggle it ON)
   - **Dockerfile Path:** `Dockerfile`
5. Add **Variables:**
   ```
   NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.railway.app
   PORT=3000
   NODE_ENV=production
   ```
6. Go to **Settings** → **Networking**
   - Generate a domain

### Step 4: Update Backend CORS
After getting the frontend URL, update backend variables:
- Update `FRONTEND_URL` with the actual frontend Railway URL

## Why This Works

When you set the **Root Directory** to `backend` or `frontend`:
- Railway looks for files in that directory
- It finds the `Dockerfile` in that directory
- It finds the `railway.json` in that directory
- It uses Docker instead of Railpack

Without setting the Root Directory:
- Railway looks in the repository root
- It doesn't find a Dockerfile in the root
- It tries Railpack auto-detection
- Railpack fails because it can't determine the build method

## Verification

After setting up, check the build logs:
- You should see "Building Docker image..." instead of "Railpack 0.15.4"
- The build should use your Dockerfile
- No more "Railpack could not determine" errors

## Important Notes

- **Root Directory is REQUIRED** - Without it, Railway won't find your Dockerfiles
- **Docker must be enabled** - Toggle "Use Dockerfile" in Settings → Docker
- **Service-specific railway.json files** are already in `backend/` and `frontend/` directories
- Railway will automatically detect and use these configurations once Root Directory is set

