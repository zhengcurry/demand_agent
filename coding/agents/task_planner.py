"""
Task Planner Agent
Breaks down architecture and requirements into executable tasks.
"""
import json
from typing import Dict, Any, List
from anthropic import Anthropic


class TaskPlanner:
    """Agent for planning and breaking down tasks"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize Task Planner

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.5

    def plan(self, requirement: Dict[str, Any], architecture: Dict[str, Any],
             api_spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create task breakdown

        Args:
            requirement: Structured requirement
            architecture: Architecture design
            api_spec: API specification

        Returns:
            Task queue with ordered tasks
        """
        prompt = f"""You are a task planner. Break down the following project into executable development tasks.

Requirement:
{json.dumps(requirement, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

API Specification:
{json.dumps(api_spec, indent=2)}

Please provide a detailed task breakdown in the following JSON format:
{{
    "tasks": [
        {{
            "id": "task_001",
            "title": "Task title",
            "description": "Detailed task description",
            "type": "setup|backend|frontend|database|testing|documentation",
            "priority": 1,
            "dependencies": ["task_id_that_must_complete_first"],
            "estimated_complexity": "low|medium|high",
            "files_to_create": [
                {{
                    "path": "relative/path/to/file.py",
                    "description": "What this file should contain"
                }}
            ],
            "acceptance_criteria": [
                "List of criteria to consider task complete"
            ]
        }}
    ]
}}

Order tasks by dependencies and priority. Respond with ONLY the JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            result = json.loads(content)
            return {"success": True, "task_plan": result}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse JSON: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_next_task(self, task_plan: Dict[str, Any], completed_tasks: List[str]) -> Dict[str, Any]:
        """
        Get next executable task

        Args:
            task_plan: Task plan
            completed_tasks: List of completed task IDs

        Returns:
            Next task to execute or None
        """
        for task in task_plan.get("tasks", []):
            task_id = task.get("id")
            if task_id in completed_tasks:
                continue

            dependencies = task.get("dependencies", [])
            if all(dep in completed_tasks for dep in dependencies):
                return {"success": True, "task": task}

        return {"success": False, "message": "No more tasks available"}
