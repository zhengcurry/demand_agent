"""
Code Reviewer Agent
Reviews generated code for quality, security, and best practices.
"""
import json
from typing import Dict, Any, List
from anthropic import Anthropic
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils import parse_json_response


class CodeReviewer:
    """Agent for reviewing code"""

    def __init__(self, api_key: str, model: str = "claude-opus-4-5-20251101"):
        """
        Initialize Code Reviewer

        Args:
            api_key: Anthropic API key
            model: Claude model to use (Opus for thorough review)
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.2

    def review(self, code: Dict[str, Any], requirement: Dict[str, Any]) -> Dict[str, Any]:
        """
        Review generated code

        Args:
            code: Generated code
            requirement: Original requirement

        Returns:
            Review report
        """
        prompt = f"""You are a code reviewer. Review the following code for quality, security, and best practices.

Code:
{json.dumps(code, indent=2)}

Requirement:
{json.dumps(requirement, indent=2)}

Please provide a comprehensive review in the following JSON format:
{{
    "overall_score": 85,
    "summary": "Brief summary of the review",
    "strengths": [
        "List of code strengths"
    ],
    "issues": [
        {{
            "severity": "critical|high|medium|low",
            "category": "security|performance|maintainability|style|correctness",
            "file": "path/to/file.py",
            "line": 42,
            "description": "Issue description",
            "suggestion": "How to fix it"
        }}
    ],
    "security_concerns": [
        "List of security concerns"
    ],
    "performance_concerns": [
        "List of performance concerns"
    ],
    "best_practices": [
        "List of best practice recommendations"
    ],
    "test_coverage": {{
        "score": 80,
        "missing_tests": [
            "List of scenarios that need tests"
        ]
    }},
    "recommendations": [
        "List of general recommendations"
    ],
    "approved": true
}}

Review criteria:
- Code quality and readability
- Security vulnerabilities (SQL injection, XSS, etc.)
- Error handling
- Performance considerations
- Test coverage
- Documentation
- Best practices for the language/framework

Respond with ONLY the JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8000,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            result = parse_json_response(content)
            return {"success": True, "review": result}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse JSON: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def quick_review(self, file_content: str, file_path: str) -> Dict[str, Any]:
        """
        Quick review of a single file

        Args:
            file_content: File content
            file_path: File path

        Returns:
            Quick review result
        """
        prompt = f"""Quickly review this file for critical issues:

File: {file_path}
Content:
{file_content}

Provide a brief review focusing on critical issues only. Respond in JSON format:
{{
    "has_critical_issues": false,
    "issues": ["List of critical issues if any"]
}}"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            result = parse_json_response(content)
            return {"success": True, "review": result}
        except Exception as e:
            return {"success": False, "error": str(e)}
