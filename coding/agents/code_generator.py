"""
Code Generator Agent
Generates code based on tasks and design documents.
"""
import json
from typing import Dict, Any
from anthropic import Anthropic


class CodeGenerator:
    """Agent for generating code"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize Code Generator

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.3
        self.max_retries = 3

    def generate(self, task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate code for a task

        Args:
            task: Task specification
            context: Context including requirement, architecture, API spec

        Returns:
            Generated code files
        """
        prompt = f"""You are a code generator. Generate production-ready code for the following task.

Task:
{json.dumps(task, indent=2)}

Context:
{json.dumps(context, indent=2)}

Please generate code in the following JSON format:
{{
    "files": [
        {{
            "path": "relative/path/to/file.py",
            "content": "Complete file content with proper imports, documentation, and error handling",
            "language": "python|javascript|typescript|etc"
        }}
    ],
    "tests": [
        {{
            "path": "relative/path/to/test_file.py",
            "content": "Complete test file content",
            "language": "python|javascript|typescript|etc"
        }}
    ],
    "dependencies": [
        "List of new dependencies to add (e.g., 'requests==2.28.0')"
    ],
    "setup_instructions": [
        "List of setup steps if needed"
    ]
}}

Guidelines:
- Write clean, well-documented code
- Include proper error handling
- Follow best practices for the language
- Include comprehensive unit tests
- Add type hints where applicable

Respond with ONLY the JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            result = json.loads(content)
            return {"success": True, "code": result}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse JSON: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fix_code(self, code: Dict[str, Any], error: str, attempt: int) -> Dict[str, Any]:
        """
        Fix code based on error

        Args:
            code: Original code
            error: Error message
            attempt: Attempt number

        Returns:
            Fixed code
        """
        if attempt >= self.max_retries:
            return {"success": False, "error": "Max retries exceeded"}

        prompt = f"""The following code has an error. Please fix it.

Original Code:
{json.dumps(code, indent=2)}

Error:
{error}

Please provide the fixed code in the same JSON format. Respond with ONLY the JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            result = json.loads(content)
            return {"success": True, "code": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
