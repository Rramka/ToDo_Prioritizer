from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from app.api import routes

load_dotenv()

app = FastAPI(title="ToDo Prioritizer API", version="1.0.0")

# CORS configuration
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(routes.router, prefix="/api", tags=["analysis"])

@app.get("/")
async def root():
    return {"message": "ToDo Prioritizer API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

