# Testing Phase 2: Backend Core Implementation

## ✅ Server Status

The backend server is now running on **http://localhost:8000**

## Testing Methods

### Method 1: Interactive API Documentation (Recommended)

1. Open your browser and visit: **http://localhost:8000/docs**
2. You'll see the Swagger UI with all available endpoints
3. Click on `/api/analyze` endpoint
4. Click "Try it out"
5. Enter test tasks in the request body:
   ```json
   {
     "tasks": "Write quarterly report\nCall client about project\nBuy groceries\nReview code changes"
   }
   ```
6. Click "Execute"
7. **Note**: You'll need to set `OPENAI_API_KEY` in your environment for the analyze endpoint to work

### Method 2: Using curl

#### Test Health Endpoint
```bash
curl http://localhost:8000/health
```
Expected response: `{"status":"healthy"}`

#### Test Root Endpoint
```bash
curl http://localhost:8000/
```
Expected response: `{"message":"ToDo Prioritizer API"}`

#### Test Analyze Endpoint (requires OpenAI API key)
```bash
curl -X POST "http://localhost:8000/api/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "tasks": "Write quarterly report\nCall client about project\nBuy groceries"
     }'
```

### Method 3: Using the Test Script

Run the provided test script:
```bash
./test_backend.sh
```

## Setting Up OpenAI API Key

To test the `/api/analyze` endpoint, you need an OpenAI API key:

1. Create a `.env` file in the project root:
   ```bash
   cd /Users/ramazkapanadze/ToDo_Prioritizer
   echo "OPENAI_API_KEY=your_api_key_here" > .env
   echo "FRONTEND_URL=http://localhost:3000" >> .env
   ```

2. Or export it in your terminal:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

3. Restart the backend server for the .env file to be loaded

## Expected API Response Format

When you call `/api/analyze`, you should receive:

```json
{
  "priorities": {
    "must": ["task1", "task2"],
    "should": ["task3"],
    "optional": ["task4"]
  },
  "breakdown": {
    "task1": {
      "steps": [
        {"step": "Open document editor", "minutes": 2},
        {"step": "Write introduction section", "minutes": 10}
      ]
    }
  },
  "next_action": {
    "task": "task1",
    "step": "Open document editor",
    "minutes": 2
  }
}
```

## Troubleshooting

### Server not running?
```bash
cd backend
source ../venv/bin/activate
uvicorn app.main:app --reload
```

### Port 8000 already in use?
```bash
lsof -ti:8000 | xargs kill -9
```

### Import errors?
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
cd backend
pip install -r requirements.txt
```

### OpenAI API errors?
- Check that your API key is set correctly
- Verify the key is valid and has credits
- Check the server logs for detailed error messages

## Next Steps

Once Phase 2 testing is complete, we'll proceed to **Phase 3: Frontend Implementation** to build the UI that connects to this backend.

