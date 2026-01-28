"""
System Architect Agent
Designs system architecture based on requirements.
"""
import json
from typing import Dict, Any
from anthropic import Anthropic
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils import parse_json_response


class SystemArchitect:
    """Agent for designing system architecture"""

    def __init__(self, api_key: str, model: str = "claude-opus-4-5-20251101"):
        """
        Initialize System Architect

        Args:
            api_key: Anthropic API key
            model: Claude model to use (Opus for complex reasoning)
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.4

    def design(self, requirement: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design system architecture

        Args:
            requirement: Structured requirement

        Returns:
            Architecture design document
        """
        prompt = f"""You are a system architect. Design a complete system architecture based on the following requirement.

Requirement:
{json.dumps(requirement, indent=2)}

Please provide a comprehensive architecture design in the following JSON format:
{{
    "overview": "High-level architecture overview",
    "tech_stack": {{
        "frontend": ["List of frontend technologies"],
        "backend": ["List of backend technologies"],
        "database": ["List of database technologies"],
        "infrastructure": ["List of infrastructure components"]
    }},
    "directory_structure": {{
        "description": "Directory structure explanation",
        "tree": [
            "project/",
            "  src/",
            "    components/",
            "    services/",
            "  tests/",
            "  docs/"
        ]
    }},
    "data_model": [
        {{
            "entity": "Entity name",
            "fields": [
                {{
                    "name": "field_name",
                    "type": "data_type",
                    "description": "Field description"
                }}
            ]
        }}
    ],
    "architecture_patterns": [
        "List of architectural patterns to use"
    ],
    "security_considerations": [
        "List of security considerations"
    ],
    "scalability_considerations": [
        "List of scalability considerations"
    ]
}}

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
            return {"success": True, "architecture": result}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse JSON: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
