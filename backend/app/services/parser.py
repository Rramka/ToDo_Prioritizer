import re
from typing import List


def parse_tasks(input_text: str) -> List[str]:
    """
    Parse input text into discrete tasks.
    Handles bullets, commas, numbered lists, and natural language.
    
    Args:
        input_text: Raw text input from user
        
    Returns:
        List of parsed task strings
    """
    if not input_text or not input_text.strip():
        return []
    
    # Normalize whitespace
    text = input_text.strip()
    
    # Split by common delimiters: newlines, bullets, commas
    # First, try splitting by newlines (most common for task lists)
    lines = text.split('\n')
    
    tasks = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Remove common bullet points and numbering
        # Matches: -, *, •, 1., 1), etc.
        line = re.sub(r'^[\s]*[-*•]\s+', '', line)
        line = re.sub(r'^[\s]*\d+[.)]\s+', '', line)
        line = re.sub(r'^[\s]*\([a-zA-Z0-9]+\)\s+', '', line)
        
        # Remove leading/trailing whitespace again
        line = line.strip()
        
        if line:
            tasks.append(line)
    
    # If we only got one task, try splitting by commas as well
    if len(tasks) == 1 and ',' in tasks[0]:
        comma_tasks = [t.strip() for t in tasks[0].split(',') if t.strip()]
        if len(comma_tasks) > 1:
            tasks = comma_tasks
    
    # Remove duplicates while preserving order
    seen = set()
    unique_tasks = []
    for task in tasks:
        task_lower = task.lower()
        if task_lower not in seen:
            seen.add(task_lower)
            unique_tasks.append(task)
    
    return unique_tasks


def validate_task_count(tasks: List[str], max_tasks: int = 50) -> None:
    """
    Validate that we don't have too many tasks.
    
    Args:
        tasks: List of tasks
        max_tasks: Maximum allowed number of tasks
        
    Raises:
        ValueError: If too many tasks
    """
    if len(tasks) > max_tasks:
        raise ValueError(f"Too many tasks. Maximum {max_tasks} tasks allowed.")

