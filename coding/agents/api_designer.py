"""
API Designer Agent
Designs API specifications based on architecture and requirements.
"""
import json
from typing import Dict, Any
from anthropic import Anthropic
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils import parse_json_response


class APIDesigner:
    """Agent for designing API specifications"""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-5-20250929"):
        """
        Initialize API Designer

        Args:
            api_key: Anthropic API key
            model: Claude model to use
        """
        self.client = Anthropic(api_key=api_key)
        self.model = model
        self.temperature = 0.2

    def design(self, requirement: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design API specification

        Args:
            requirement: Structured requirement
            architecture: Architecture design

        Returns:
            OpenAPI specification
        """
        prompt = f"""You are an API designer. Design a complete API specification based on the following requirement and architecture.

Requirement:
{json.dumps(requirement, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Please provide a comprehensive API design in OpenAPI 3.0 format:
{{
    "openapi": "3.0.0",
    "info": {{
        "title": "API Title",
        "version": "1.0.0",
        "description": "API Description"
    }},
    "paths": {{
        "/endpoint": {{
            "get": {{
                "summary": "Endpoint summary",
                "parameters": [],
                "responses": {{
                    "200": {{
                        "description": "Success response",
                        "content": {{
                            "application/json": {{
                                "schema": {{}}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }},
    "components": {{
        "schemas": {{}},
        "securitySchemes": {{}}
    }}
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
            return {"success": True, "api_spec": result}
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Failed to parse JSON: {str(e)}", "raw_response": content}
        except Exception as e:
            return {"success": False, "error": str(e)}
