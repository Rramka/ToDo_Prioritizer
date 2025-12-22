import pytest
from app.services.parser import parse_tasks, validate_task_count


class TestTaskParser:
    """Test suite for task parser."""
    
    def test_parse_bullet_points(self):
        """Test parsing tasks with bullet points."""
        input_text = "- Task 1\n- Task 2\n- Task 3"
        result = parse_tasks(input_text)
        assert len(result) == 3
        assert "Task 1" in result
        assert "Task 2" in result
        assert "Task 3" in result
    
    def test_parse_numbered_list(self):
        """Test parsing numbered lists."""
        input_text = "1. First task\n2. Second task\n3. Third task"
        result = parse_tasks(input_text)
        assert len(result) == 3
        assert "First task" in result
        assert "Second task" in result
    
    def test_parse_comma_separated(self):
        """Test parsing comma-separated tasks."""
        input_text = "Task 1, Task 2, Task 3"
        result = parse_tasks(input_text)
        assert len(result) == 3
    
    def test_parse_mixed_format(self):
        """Test parsing mixed formats."""
        input_text = "- Task 1\nTask 2\n3. Task 3"
        result = parse_tasks(input_text)
        assert len(result) == 3
    
    def test_parse_empty_input(self):
        """Test parsing empty input."""
        result = parse_tasks("")
        assert result == []
        
        result = parse_tasks("   ")
        assert result == []
    
    def test_parse_single_task(self):
        """Test parsing single task."""
        result = parse_tasks("Single task")
        assert len(result) == 1
        assert result[0] == "Single task"
    
    def test_remove_duplicates(self):
        """Test that duplicates are removed."""
        input_text = "Task 1\nTask 1\nTask 2"
        result = parse_tasks(input_text)
        assert len(result) == 2
        assert result.count("Task 1") == 1
    
    def test_remove_whitespace(self):
        """Test that leading/trailing whitespace is removed."""
        input_text = "  Task 1  \n  Task 2  "
        result = parse_tasks(input_text)
        assert all(not task.startswith(" ") and not task.endswith(" ") for task in result)
    
    def test_validate_task_count_success(self):
        """Test task count validation with valid count."""
        tasks = ["Task 1", "Task 2", "Task 3"]
        # Should not raise
        validate_task_count(tasks)
    
    def test_validate_task_count_too_many(self):
        """Test task count validation with too many tasks."""
        tasks = [f"Task {i}" for i in range(51)]
        with pytest.raises(ValueError, match="Too many tasks"):
            validate_task_count(tasks, max_tasks=50)
    
    def test_parse_natural_language(self):
        """Test parsing natural language task descriptions."""
        input_text = """
        I need to:
        - Write a report
        - Call my client
        - Buy groceries
        """
        result = parse_tasks(input_text)
        assert len(result) >= 3

