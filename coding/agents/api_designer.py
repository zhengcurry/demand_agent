"""
API Designer Agent
Designs API specifications based on architecture and requirements.
Uses YAML format for more concise and error-free generation.
"""
import json
import yaml
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
        self.temperature = 0.0  # Deterministic output
        self.use_yaml = True  # Use YAML for more concise generation

    def design(self, requirement: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
        """
        Design API specification using YAML format for efficiency

        Args:
            requirement: Structured requirement
            architecture: Architecture design

        Returns:
            OpenAPI specification (as dict)
        """
        if self.use_yaml:
            return self._design_with_yaml(requirement, architecture)
        else:
            return self._design_with_json(requirement, architecture)

    def _design_with_yaml(self, requirement: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Generate API spec using YAML format (more concise, less error-prone)"""

        prompt = f"""You are an API designer. Design a CONCISE API specification in YAML format.

Requirement:
{json.dumps(requirement, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Generate an OpenAPI 3.0 specification in YAML format. YAML is more concise than JSON:
- No quotes around keys
- No commas between items
- Use indentation for structure

Keep it FOCUSED and CONCISE:
- Only 3-5 ESSENTIAL endpoints
- Brief descriptions (1 sentence)
- Use schema references ($ref)
- Minimal examples

Example YAML format:
```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
  description: Brief description
paths:
  /auth/login:
    post:
      summary: User login
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginResponse'
  /auth/register:
    post:
      summary: User registration
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RegisterRequest'
      responses:
        '201':
          description: Created
components:
  schemas:
    LoginRequest:
      type: object
      required: [username, password]
      properties:
        username:
          type: string
        password:
          type: string
    LoginResponse:
      type: object
      properties:
        token:
          type: string
    RegisterRequest:
      type: object
      required: [username, email, password]
      properties:
        username:
          type: string
        email:
          type: string
        password:
          type: string
```

CRITICAL: Respond with ONLY the YAML content, no markdown code blocks, no additional text."""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=8000,  # YAML is much more concise than JSON
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}]
                )

                content = response.content[0].text.strip()

                # Extract token usage information
                token_usage = {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }

                # Remove markdown code blocks if present
                if content.startswith("```yaml"):
                    content = content[7:]
                elif content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()

                # Parse YAML to dict
                api_spec = yaml.safe_load(content)

                # Validate it's a proper OpenAPI spec
                if not isinstance(api_spec, dict) or "openapi" not in api_spec:
                    raise ValueError("Invalid OpenAPI specification structure")

                return {
                    "success": True,
                    "api_spec": api_spec,
                    "token_usage": token_usage,
                    "format": "yaml"
                }

            except yaml.YAMLError as e:
                if attempt < max_retries - 1:
                    prompt = f"""The previous YAML had a syntax error: {str(e)}

Please regenerate the API specification in valid YAML format.

Requirement:
{json.dumps(requirement, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Generate valid YAML. Common issues to avoid:
- Incorrect indentation (use 2 spaces)
- Missing colons after keys
- Inconsistent spacing

Respond with ONLY valid YAML, no markdown blocks."""
                    continue
                else:
                    return {"success": False, "error": f"Failed to parse YAML after {max_retries} attempts: {str(e)}", "raw_response": content}
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return {"success": False, "error": str(e)}

        return {"success": False, "error": "Max retries exceeded"}

    def _design_with_json(self, requirement: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback: Generate API spec using JSON format (kept for compatibility)"""

        prompt = f"""You are an API designer. Design a CONCISE API specification based on the following requirement and architecture.

Requirement:
{json.dumps(requirement, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Please provide a CONCISE API design in OpenAPI 3.0 format. Keep it simple and focused:
- Include only the ESSENTIAL endpoints (3-5 main endpoints)
- Use simple schema references instead of inline schemas
- Keep descriptions brief (1-2 sentences max)
- Avoid excessive examples and details

Example format:
{{
    "openapi": "3.0.0",
    "info": {{
        "title": "API Title",
        "version": "1.0.0",
        "description": "Brief description"
    }},
    "paths": {{
        "/endpoint": {{
            "post": {{
                "summary": "Brief summary",
                "requestBody": {{
                    "content": {{
                        "application/json": {{
                            "schema": {{"$ref": "#/components/schemas/RequestModel"}}
                        }}
                    }}
                }},
                "responses": {{
                    "200": {{
                        "description": "Success",
                        "content": {{
                            "application/json": {{
                                "schema": {{"$ref": "#/components/schemas/ResponseModel"}}
                            }}
                        }}
                    }}
                }}
            }}
        }}
    }},
    "components": {{
        "schemas": {{
            "RequestModel": {{
                "type": "object",
                "properties": {{
                    "field": {{"type": "string"}}
                }}
            }},
            "ResponseModel": {{
                "type": "object",
                "properties": {{
                    "id": {{"type": "string"}}
                }}
            }}
        }}
    }}
}}

CRITICAL REQUIREMENTS:
1. Keep the response under 10000 tokens - be CONCISE
2. Ensure the JSON is syntactically valid with all commas, brackets, and braces properly placed
3. Every opening bracket/brace MUST have a closing bracket/brace
4. Respond with ONLY the valid JSON, no additional text or markdown"""

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=12000,  # Reduced from 20000
                    temperature=self.temperature,
                    messages=[{"role": "user", "content": prompt}]
                )

                content = response.content[0].text

                # Extract token usage information
                token_usage = {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }

                result = parse_json_response(content)
                return {
                    "success": True,
                    "api_spec": result,
                    "token_usage": token_usage,
                    "format": "json"
                }
            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    # Retry with a more explicit prompt about the error
                    prompt = f"""The previous API specification had a JSON syntax error: {str(e)}

Please regenerate the API specification, ensuring it is valid JSON.

Requirement:
{json.dumps(requirement, indent=2)}

Architecture:
{json.dumps(architecture, indent=2)}

Generate a valid OpenAPI 3.0 specification in JSON format. Pay special attention to:
- All commas between object properties
- Proper closing of all brackets and braces
- No trailing commas before closing brackets

Respond with ONLY the valid JSON."""
                    continue
                else:
                    return {"success": False, "error": f"Failed to parse JSON after {max_retries} attempts: {str(e)}", "raw_response": content}
            except Exception as e:
                if attempt < max_retries - 1:
                    continue
                return {"success": False, "error": str(e)}

        return {"success": False, "error": "Max retries exceeded"}
