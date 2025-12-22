# ToDo Prioritizer - StartNow MVP

A smart task prioritization tool that breaks down your to-do list into actionable micro-steps and identifies what to do next.

## Architecture

- **Frontend**: Next.js 14+ with TypeScript and Tailwind CSS
- **Backend**: FastAPI with Python
- **AI**: OpenAI GPT-4 for task analysis

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 18+
- Docker (optional, for containerized deployment)
- OpenAI API Key

### Backend Setup

1. Activate virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

4. Run backend:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Set environment variables:
   ```bash
   cp .env.example .env.local
   # Edit .env.local and set BACKEND_URL
   ```

3. Run frontend:
   ```bash
   npm run dev
   ```

### Docker Setup (Optional)

```bash
docker-compose up
```

## Environment Variables

- `OPENAI_API_KEY`: Required for AI processing
- `BACKEND_URL`: Frontend needs backend URL (default: http://localhost:8000)
- `FRONTEND_URL`: Backend CORS origin (default: http://localhost:3000)

## Project Structure

```
ToDo_Prioritizer/
├── frontend/          # Next.js application
├── backend/           # FastAPI application
├── docker-compose.yml # Docker orchestration
└── README.md
```

