from fastapi import APIRouter, HTTPException
from app.models.schemas import TaskAnalysisRequest, TaskAnalysisResponse, ErrorResponse
from app.services.parser import parse_tasks, validate_task_count
from app.services.ai_service import AIService

router = APIRouter()

# Initialize AI service (will be created once)
_ai_service = None

def get_ai_service() -> AIService:
    """Get or create AI service instance."""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service


@router.post("/analyze", response_model=TaskAnalysisResponse)
async def analyze_tasks(request: TaskAnalysisRequest) -> TaskAnalysisResponse:
    """
    Analyze tasks and return prioritized breakdown with next action.
    
    Args:
        request: TaskAnalysisRequest with tasks text
        
    Returns:
        TaskAnalysisResponse with priorities, breakdowns, and next action
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Parse tasks from input
        tasks = parse_tasks(request.tasks)
        
        if not tasks:
            raise HTTPException(
                status_code=400,
                detail="No valid tasks found in input. Please provide at least one task."
            )
        
        # Validate task count
        validate_task_count(tasks)
        
        # Get AI service and analyze
        ai_service = get_ai_service()
        result = ai_service.analyze_tasks(tasks)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Log the error (in production, use proper logging)
        error_msg = str(e)
        if "OPENAI_API_KEY" in error_msg:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key is not configured. Please set OPENAI_API_KEY environment variable."
            )
        raise HTTPException(
            status_code=500,
            detail=f"Failed to analyze tasks: {error_msg}"
        )

