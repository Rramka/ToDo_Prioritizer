import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from app.services.ai_service import AIService
from app.models.schemas import TaskAnalysisResponse


class TestAIService:
    """Test suite for AI service."""
    
    @pytest.fixture
    def ai_service(self):
        """Create AI service instance with mocked OpenAI client."""
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}):
            service = AIService()
            service.client = Mock()
            return service
    
    def test_init_missing_api_key(self):
        """Test that missing API key raises error."""
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(ValueError, match="OPENAI_API_KEY"):
                AIService()
    
    def test_analyze_tasks_empty_list(self, ai_service):
        """Test that empty task list raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            ai_service.analyze_tasks([])
    
    def test_analyze_tasks_success(self, ai_service):
        """Test successful task analysis."""
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = json.dumps({
            "priorities": {
                "must": ["Task 1"],
                "should": ["Task 2"],
                "optional": []
            },
            "breakdown": {
                "Task 1": {
                    "steps": [
                        {"step": "Open document", "minutes": 2},
                        {"step": "Write content", "minutes": 10}
                    ]
                },
                "Task 2": {
                    "steps": [
                        {"step": "Find contact", "minutes": 3},
                        {"step": "Make call", "minutes": 15}
                    ]
                }
            },
            "next_action": {
                "task": "Task 1",
                "step": "Open document",
                "minutes": 2
            }
        })
        
        ai_service.client.chat.completions.create.return_value = mock_response
        
        result = ai_service.analyze_tasks(["Task 1", "Task 2"])
        
        assert isinstance(result, TaskAnalysisResponse)
        assert len(result.priorities["must"]) == 1
        assert len(result.breakdown) == 2
        assert result.next_action.task == "Task 1"
        assert result.next_action.step == "Open document"
        assert result.next_action.minutes == 2
    
    def test_parse_ai_response_missing_tasks(self, ai_service):
        """Test parsing response with missing tasks."""
        result_dict = {
            "priorities": {
                "must": ["Task 1"],
                "should": [],
                "optional": []
            },
            "breakdown": {
                "Task 1": {
                    "steps": [
                        {"step": "Do something", "minutes": 5}
                    ]
                }
            },
            "next_action": {
                "task": "Task 1",
                "step": "Do something",
                "minutes": 5
            }
        }
        
        # Task 2 is missing from response
        original_tasks = ["Task 1", "Task 2"]
        response = ai_service._parse_ai_response(result_dict, original_tasks)
        
        # Task 2 should be added to optional
        assert "Task 2" in response.priorities["optional"]
        # Task 2 should have a default breakdown
        assert "Task 2" in response.breakdown
    
    def test_parse_ai_response_invalid_times(self, ai_service):
        """Test parsing response with invalid time estimates."""
        result_dict = {
            "priorities": {
                "must": ["Task 1"],
                "should": [],
                "optional": []
            },
            "breakdown": {
                "Task 1": {
                    "steps": [
                        {"step": "Step 1", "minutes": 1},  # Too low
                        {"step": "Step 2", "minutes": 25}  # Too high
                    ]
                }
            },
            "next_action": {
                "task": "Task 1",
                "step": "Step 1",
                "minutes": 1
            }
        }
        
        response = ai_service._parse_ai_response(result_dict, ["Task 1"])
        
        # Times should be clamped to 2-20
        steps = response.breakdown["Task 1"].steps
        assert steps[0].minutes == 2  # Clamped from 1
        assert steps[1].minutes == 20  # Clamped from 25

