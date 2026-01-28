"""
Requirement Analyst Agent
Analyzes user requirements and converts them to structured format.
"""
import json
from typing import Dict, Any, Optional
from anthropic import Anthropic


class RequirementAnalyst:
    """Agent for analyzing and structuring requirements"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize Requirement Analyst

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.3

    def analyze(self, requirement: str, source_type: str = "text") -> Dict[str, Any]:
        """
        Analyze requirement and convert to structured format

        Args:
            requirement: Requirement description
            source_type: Source type (text, feishu, file)

        Returns:
            Structured requirement JSON
        """
        prompt = f"""You are a requirement analyst. Analyze the following requirement and convert it to a structured JSON format.

Requirement:
{requirement}

Please provide a structured analysis in the following JSON format:
{{
    "title": "Brief title of the requirement",
    "description": "Detailed description",
    "type": "web|mobile|backend|desktop|other",
    "features": [
        {{
            "name": "Feature name",
            "description": "Feature description",
            "priority": "high|medium|low"
        }}
    ],
    "technical_requirements": [
        "List of technical requirements"
    ],
    "constraints": [
        "List of constraints or limitations"
    ],
    "success_criteria": [
        "List of success criteria"
    ]
}}

Respond with ONLY the JSON, no additional text."""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text
            result = json.loads(content)
            return {"success": True, "requirement": result}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse JSON: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def validate_requirement(self, requirement: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate structured requirement

        Args:
            requirement: Structured requirement

        Returns:
            Validation result
        """
        required_fields = ["title", "description", "type", "features"]
        missing_fields = [field for field in required_fields if field not in requirement]

        if missing_fields:
            return {
                "valid": False,
                "errors": [f"Missing required field: {field}" for field in missing_fields]
            }

        if not requirement.get("features"):
            return {"valid": False, "errors": ["At least one feature is required"]}

        return {"valid": True, "errors": []}
