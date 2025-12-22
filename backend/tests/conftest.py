import pytest
import os
import json
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from app.main import app

# Set test environment variables
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["FRONTEND_URL"] = "http://localhost:3000"

@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)

@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response."""
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "priorities": {
                        "must": ["Write quarterly report"],
                        "should": ["Call client"],
                        "optional": ["Buy groceries"]
                    },
                    "breakdown": {
                        "Write quarterly report": {
                            "steps": [
                                {"step": "Open the document", "minutes": 2},
                                {"step": "Write introduction", "minutes": 10}
                            ]
                        },
                        "Call client": {
                            "steps": [
                                {"step": "Find phone number", "minutes": 3},
                                {"step": "Make the call", "minutes": 15}
                            ]
                        },
                        "Buy groceries": {
                            "steps": [
                                {"step": "Make shopping list", "minutes": 5},
                                {"step": "Go to store", "minutes": 20}
                            ]
                        }
                    },
                    "next_action": {
                        "task": "Write quarterly report",
                        "step": "Open the document",
                        "minutes": 2
                    }
                })
            }
        }]
    }

