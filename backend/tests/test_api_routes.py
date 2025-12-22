import pytest
import json
from unittest.mock import patch, Mock
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.schemas import TaskAnalysisResponse, TaskBreakdown, TaskStep, NextAction


@pytest.fixture
async def client():
    """Create async test client."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


class TestAnalyzeEndpoint:
    """Test suite for /api/analyze endpoint."""
    
    @pytest.mark.asyncio
    async def test_analyze_success(self, client):
        """Test successful task analysis."""
        mock_response = TaskAnalysisResponse(
            priorities={
                "must": ["Write report"],
                "should": ["Call client"],
                "optional": []
            },
            breakdown={
                "Write report": TaskBreakdown(
                    steps=[
                        TaskStep(step="Open document", minutes=2),
                        TaskStep(step="Write content", minutes=10)
                    ]
                ),
                "Call client": TaskBreakdown(
                    steps=[
                        TaskStep(step="Find number", minutes=3),
                        TaskStep(step="Make call", minutes=15)
                    ]
                )
            },
            next_action=NextAction(
                task="Write report",
                step="Open document",
                minutes=2
            )
        )
        
        with patch("app.api.routes.get_ai_service") as mock_service:
            mock_ai_service = Mock()
            mock_ai_service.analyze_tasks.return_value = mock_response
            mock_service.return_value = mock_ai_service
            
            response = await client.post(
                "/api/analyze",
                json={"tasks": "Write report\nCall client"}
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "priorities" in data
            assert "breakdown" in data
            assert "next_action" in data
            assert data["priorities"]["must"] == ["Write report"]
    
    @pytest.mark.asyncio
    async def test_analyze_empty_input(self, client):
        """Test analysis with empty input."""
        response = await client.post(
            "/api/analyze",
            json={"tasks": ""}
        )
        
        # Pydantic validation returns 422 for empty string
        assert response.status_code in [400, 422]
    
    @pytest.mark.asyncio
    async def test_analyze_too_long_input(self, client):
        """Test analysis with input exceeding character limit."""
        long_text = "a" * 2001
        response = await client.post(
            "/api/analyze",
            json={"tasks": long_text}
        )
        
        assert response.status_code == 422  # Validation error
    
    @pytest.mark.asyncio
    async def test_analyze_missing_tasks_field(self, client):
        """Test analysis with missing tasks field."""
        response = await client.post(
            "/api/analyze",
            json={}
        )
        
        assert response.status_code == 422
    
    @pytest.mark.asyncio
    async def test_analyze_openai_error(self, client):
        """Test handling of OpenAI API errors."""
        with patch("app.api.routes.get_ai_service") as mock_service:
            mock_ai_service = Mock()
            mock_ai_service.analyze_tasks.side_effect = Exception("OpenAI API error")
            mock_service.return_value = mock_ai_service
            
            response = await client.post(
                "/api/analyze",
                json={"tasks": "Test task"}
            )
            
            assert response.status_code == 500
            data = response.json()
            assert "error" in data or "detail" in data


class TestHealthEndpoints:
    """Test suite for health check endpoints."""
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = await client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    @pytest.mark.asyncio
    async def test_health_endpoint(self, client):
        """Test health endpoint."""
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

