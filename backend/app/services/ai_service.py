import os
import json
from typing import List, Dict
from openai import OpenAI
from app.models.schemas import TaskAnalysisResponse, TaskBreakdown, TaskStep, NextAction


class AIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Default to gpt-4o-mini, can use gpt-4o or gpt-3.5-turbo
    
    def analyze_tasks(self, tasks: List[str]) -> TaskAnalysisResponse:
        """
        Analyze tasks and return prioritized breakdown with next action.
        
        Args:
            tasks: List of task strings
            
        Returns:
            TaskAnalysisResponse with priorities, breakdowns, and next action
        """
        if not tasks:
            raise ValueError("Tasks list cannot be empty")
        
        # Create the prompt
        prompt = self._create_analysis_prompt(tasks)
        
        # Call OpenAI
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert task prioritization and productivity coach. Your goal is to help people overcome procrastination by breaking down overwhelming tasks into tiny, actionable micro-steps.

Key principles:
1. The first step should be so easy it's impossible to say no
2. Each step should be 2-20 minutes and feel achievable
3. Prioritize based on urgency, impact, dependencies, and effort
4. Always provide the smallest possible next action to reduce friction

Provide structured JSON responses that are practical and actionable."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.5,  # Lower temperature for more consistent results
            max_tokens=3000  # Increased for detailed breakdowns
        )
        
        # Parse response
        content = response.choices[0].message.content
        result = json.loads(content)
        
        # Validate and structure the response
        return self._parse_ai_response(result, tasks)
    
    def _create_analysis_prompt(self, tasks: List[str]) -> str:
        """Create the prompt for task analysis."""
        tasks_text = "\n".join([f"{i+1}. {task}" for i, task in enumerate(tasks)])
        
        prompt = f"""Analyze the following tasks and provide a comprehensive JSON response with prioritization, breakdowns, and next action.

TASKS TO ANALYZE:
{tasks_text}

=== PRIORITIZATION CRITERIA ===

Evaluate each task using these factors (in order of importance):
1. URGENCY: Deadlines, time-sensitive commitments
2. IMPACT: Consequences of doing/not doing, value created
3. DEPENDENCIES: Blocks other tasks or people waiting on this
4. EFFORT: Time and energy required (lower effort = easier to start)

Categorize as:
- MUST: High urgency OR high impact OR blocking others OR has deadline
- SHOULD: Important but not urgent, medium impact, no immediate deadline
- OPTIONAL: Low priority, nice-to-have, can be deferred

=== BREAKDOWN RULES ===

For EACH task, create micro-steps that follow these rules:

1. STEP SIZE: Each step must be 2-20 minutes. Prefer smaller steps (2-5 min) for the first few steps.

2. ACTION FORMAT: 
   - Start with action verbs: "Open", "Write", "Call", "Find", "Create", "Send", etc.
   - Be specific and concrete: "Open email client" not "Check email"
   - One clear action per step

3. FIRST STEP RULE (Critical!):
   - The FIRST step must be extremely easy - so easy it's impossible to say no
   - Examples: "Open the document", "Find the phone number", "Open the app"
   - Should take 2-5 minutes maximum
   - Should require minimal mental energy

4. PROGRESSION:
   - Steps should build logically on each other
   - Each step should feel achievable
   - Break complex tasks into 3-8 steps typically

5. TIME ESTIMATES:
   - Be realistic: 2-5 min for simple actions, 10-15 min for moderate, 15-20 min for complex
   - First step should always be 2-5 minutes

=== NEXT ACTION SELECTION ===

Choose the NEXT ACTION that:
1. Comes from the highest priority task (Must > Should > Optional)
2. Is the FIRST step of that task's breakdown
3. Takes 2-5 minutes (prefer shorter)
4. Requires minimal context or preparation
5. Is the absolute smallest viable action to get started

The next action should eliminate all friction - it should be so easy that starting feels effortless.

=== OUTPUT FORMAT ===

Return JSON in this exact structure:
{{
  "priorities": {{
    "must": ["exact task name 1", "exact task name 2"],
    "should": ["exact task name 3"],
    "optional": ["exact task name 4"]
  }},
  "breakdown": {{
    "exact task name 1": {{
      "steps": [
        {{"step": "Open the document or file needed", "minutes": 2}},
        {{"step": "Review the key sections", "minutes": 5}},
        {{"step": "Write the introduction paragraph", "minutes": 10}},
        {{"step": "Complete the main content", "minutes": 15}}
      ]
    }},
    "exact task name 2": {{
      "steps": [
        {{"step": "Find the contact information", "minutes": 3}},
        {{"step": "Draft the message or talking points", "minutes": 5}},
        {{"step": "Make the call or send the message", "minutes": 10}}
      ]
    }}
  }},
  "next_action": {{
    "task": "exact task name 1",
    "step": "Open the document or file needed",
    "minutes": 2
  }}
}}

=== CRITICAL REQUIREMENTS ===

1. Use EXACT task names as provided (match them precisely)
2. Every task must appear in exactly ONE priority category
3. Every task must have a breakdown with at least 2 steps
4. First step of each task must be 2-5 minutes and extremely easy
5. Next action must be the first step of the highest priority task
6. All step descriptions must start with action verbs
7. Time estimates must be between 2-20 minutes per step

Now analyze the tasks and provide your response:"""
        
        return prompt
    
    def _parse_ai_response(self, result: Dict, original_tasks: List[str]) -> TaskAnalysisResponse:
        """Parse and validate AI response."""
        # Extract priorities
        priorities = result.get("priorities", {})
        must = priorities.get("must", [])
        should = priorities.get("should", [])
        optional = priorities.get("optional", [])
        
        # Validate that all tasks are categorized
        all_categorized = set(must + should + optional)
        original_set = set(original_tasks)
        
        # If some tasks are missing, add them to optional
        missing_tasks = original_set - all_categorized
        if missing_tasks:
            optional.extend(list(missing_tasks))
        
        # Extract breakdowns
        breakdown_dict = result.get("breakdown", {})
        breakdown = {}
        for task_name, task_data in breakdown_dict.items():
            steps_data = task_data.get("steps", [])
            if not steps_data:
                # If no steps provided, create a default breakdown
                steps_data = [
                    {"step": f"Start working on {task_name}", "minutes": 5},
                    {"step": f"Complete {task_name}", "minutes": 15}
                ]
            
            # Validate and fix step times
            validated_steps = []
            for s in steps_data:
                step_text = s.get("step", "")
                minutes = s.get("minutes", 5)
                # Ensure minutes are within valid range
                minutes = max(2, min(20, int(minutes)))
                validated_steps.append(TaskStep(step=step_text, minutes=minutes))
            
            breakdown[task_name] = TaskBreakdown(steps=validated_steps)
        
        # Create breakdowns for tasks that don't have one
        for task in original_tasks:
            if task not in breakdown:
                breakdown[task] = TaskBreakdown(steps=[
                    TaskStep(step=f"Start working on {task}", minutes=5),
                    TaskStep(step=f"Complete {task}", minutes=15)
                ])
        
        # Extract next action
        next_action_data = result.get("next_action", {})
        next_task = next_action_data.get("task", "")
        next_step = next_action_data.get("step", "")
        next_minutes = next_action_data.get("minutes", 5)
        
        # If next action is missing or invalid, use first step of highest priority task
        if not next_task or not next_step:
            # Find first task in priority order
            priority_task = None
            if must:
                priority_task = must[0]
            elif should:
                priority_task = should[0]
            elif optional:
                priority_task = optional[0]
            
            if priority_task and priority_task in breakdown:
                first_step = breakdown[priority_task].steps[0]
                next_task = priority_task
                next_step = first_step.step
                next_minutes = first_step.minutes
        
        # Validate next action minutes
        next_minutes = max(2, min(20, int(next_minutes)))
        
        next_action = NextAction(
            task=next_task,
            step=next_step,
            minutes=next_minutes
        )
        
        return TaskAnalysisResponse(
            priorities={
                "must": must,
                "should": should,
                "optional": optional
            },
            breakdown=breakdown,
            next_action=next_action
        )

