#!/bin/bash

# Test script for Phase 2 Backend
# This script helps test the backend API

echo "=== Testing ToDo Prioritizer Backend ==="
echo ""

# Check if server is running
if ! lsof -ti:8000 > /dev/null 2>&1; then
    echo "❌ Backend server is not running on port 8000"
    echo ""
    echo "To start the server, run:"
    echo "  cd backend"
    echo "  source ../venv/bin/activate"
    echo "  uvicorn app.main:app --reload"
    echo ""
    exit 1
fi

echo "✅ Backend server is running"
echo ""

# Test 1: Health check
echo "Test 1: Health Check"
echo "-------------------"
curl -s http://localhost:8000/health | python3 -m json.tool
echo ""
echo ""

# Test 2: Root endpoint
echo "Test 2: Root Endpoint"
echo "---------------------"
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""
echo ""

# Test 3: API Documentation
echo "Test 3: API Documentation"
echo "-------------------------"
echo "Visit http://localhost:8000/docs in your browser for interactive API docs"
echo ""

# Test 4: Analyze endpoint (if OpenAI API key is set)
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY not set. Skipping analyze endpoint test."
    echo "   Set it in .env file or export it:"
    echo "   export OPENAI_API_KEY=your_key_here"
    echo ""
else
    echo "Test 4: Analyze Endpoint"
    echo "-----------------------"
    echo "Sending test request..."
    curl -s -X POST "http://localhost:8000/api/analyze" \
         -H "Content-Type: application/json" \
         -d '{
           "tasks": "Write quarterly report\nCall client about project\nBuy groceries\nReview code changes"
         }' | python3 -m json.tool
    echo ""
fi

echo ""
echo "=== Testing Complete ==="

