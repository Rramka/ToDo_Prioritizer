# Railway Deployment - Quick Start

## TL;DR - 5 Minute Setup

### 1. Backend Service
- Create service from GitHub repo
- **Settings → Source**: Root Directory = `backend`
- **Settings → Build**: Dockerfile Path = `Dockerfile`
- **Variables**: Add `OPENAI_API_KEY=your_key_here`
- Copy backend URL after deployment

### 2. Frontend Service
- Create second service from same GitHub repo
- **Settings → Source**: Root Directory = `frontend`
- **Settings → Build**: Dockerfile Path = `Dockerfile`
- **Variables**: Add `NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.up.railway.app`
- Copy frontend URL after deployment

### 3. Update Backend CORS
- **Backend Variables**: Add `FRONTEND_URL=https://your-frontend-url.up.railway.app`

### 4. Test
- Visit frontend URL
- Submit tasks and verify it works

---

## Required Environment Variables

### Backend
```
OPENAI_API_KEY=sk-your-key-here
FRONTEND_URL=https://your-frontend-url.up.railway.app
```

### Frontend
```
NEXT_PUBLIC_BACKEND_URL=https://your-backend-url.up.railway.app
```

---

## Important Settings

Both services need:
- **Root Directory** set correctly (`backend` or `frontend`)
- **Dockerfile Path** = `Dockerfile` (not absolute path)

---

📖 **Full Guide**: See `RAILWAY_DEPLOYMENT_GUIDE.md` for detailed instructions

