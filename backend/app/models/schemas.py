from pydantic import BaseModel, Field, field_validator
from typing import Dict, List, Optional


class TaskAnalysisRequest(BaseModel):
    tasks: str = Field(..., min_length=1, max_length=2000, description="Raw task input text")

    @field_validator('tasks')
    @classmethod
    def validate_tasks(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Tasks cannot be empty")
        return v.strip()


class TaskStep(BaseModel):
    step: str = Field(..., description="Actionable step description")
    minutes: int = Field(..., ge=2, le=20, description="Estimated time in minutes (2-20)")


class TaskBreakdown(BaseModel):
    steps: List[TaskStep] = Field(..., description="List of micro-steps for the task")


class NextAction(BaseModel):
    task: str = Field(..., description="Task name")
    step: str = Field(..., description="The next actionable step")
    minutes: int = Field(..., ge=2, le=20, description="Estimated time in minutes")


class TaskAnalysisResponse(BaseModel):
    priorities: Dict[str, List[str]] = Field(
        ...,
        description="Tasks grouped by priority: must, should, optional"
    )
    breakdown: Dict[str, TaskBreakdown] = Field(
        ...,
        description="Task breakdowns mapped by task name"
    )
    next_action: NextAction = Field(..., description="The next action to take")


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")

