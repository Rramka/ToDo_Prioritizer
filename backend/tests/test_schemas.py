import pytest
from pydantic import ValidationError
from app.models.schemas import (
    TaskAnalysisRequest,
    TaskStep,
    TaskBreakdown,
    NextAction,
    TaskAnalysisResponse
)


class TestTaskAnalysisRequest:
    """Test suite for TaskAnalysisRequest model."""
    
    def test_valid_request(self):
        """Test valid request."""
        request = TaskAnalysisRequest(tasks="Write report\nCall client")
        assert request.tasks == "Write report\nCall client"
    
    def test_empty_tasks(self):
        """Test that empty tasks raises error."""
        with pytest.raises(ValidationError):
            TaskAnalysisRequest(tasks="")
    
    def test_whitespace_only_tasks(self):
        """Test that whitespace-only tasks raises error."""
        with pytest.raises(ValidationError):
            TaskAnalysisRequest(tasks="   ")
    
    def test_tasks_too_long(self):
        """Test that tasks exceeding max length raises error."""
        long_text = "a" * 2001
        with pytest.raises(ValidationError):
            TaskAnalysisRequest(tasks=long_text)
    
    def test_tasks_stripped(self):
        """Test that tasks are stripped of leading/trailing whitespace."""
        request = TaskAnalysisRequest(tasks="  Write report  ")
        assert request.tasks == "Write report"


class TestTaskStep:
    """Test suite for TaskStep model."""
    
    def test_valid_step(self):
        """Test valid step."""
        step = TaskStep(step="Open document", minutes=5)
        assert step.step == "Open document"
        assert step.minutes == 5
    
    def test_minutes_too_low(self):
        """Test that minutes below 2 raises error."""
        with pytest.raises(ValidationError):
            TaskStep(step="Test", minutes=1)
    
    def test_minutes_too_high(self):
        """Test that minutes above 20 raises error."""
        with pytest.raises(ValidationError):
            TaskStep(step="Test", minutes=21)
    
    def test_minutes_boundary_values(self):
        """Test boundary values for minutes."""
        step_min = TaskStep(step="Test", minutes=2)
        step_max = TaskStep(step="Test", minutes=20)
        assert step_min.minutes == 2
        assert step_max.minutes == 20


class TestTaskBreakdown:
    """Test suite for TaskBreakdown model."""
    
    def test_valid_breakdown(self):
        """Test valid breakdown."""
        breakdown = TaskBreakdown(
            steps=[
                TaskStep(step="Step 1", minutes=5),
                TaskStep(step="Step 2", minutes=10)
            ]
        )
        assert len(breakdown.steps) == 2


class TestNextAction:
    """Test suite for NextAction model."""
    
    def test_valid_next_action(self):
        """Test valid next action."""
        action = NextAction(
            task="Write report",
            step="Open document",
            minutes=5
        )
        assert action.task == "Write report"
        assert action.step == "Open document"
        assert action.minutes == 5


class TestTaskAnalysisResponse:
    """Test suite for TaskAnalysisResponse model."""
    
    def test_valid_response(self):
        """Test valid response."""
        response = TaskAnalysisResponse(
            priorities={
                "must": ["Task 1"],
                "should": ["Task 2"],
                "optional": []
            },
            breakdown={
                "Task 1": TaskBreakdown(
                    steps=[TaskStep(step="Do something", minutes=5)]
                )
            },
            next_action=NextAction(
                task="Task 1",
                step="Do something",
                minutes=5
            )
        )
        assert len(response.priorities["must"]) == 1
        assert "Task 1" in response.breakdown

