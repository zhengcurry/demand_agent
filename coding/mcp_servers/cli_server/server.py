"""
CLI MCP Server
Provides command-line execution as MCP tools.
"""
import subprocess
import shlex
from pathlib import Path
from typing import Dict, Any, List


class CLIMCPServer:
    """MCP Server for CLI operations"""

    def __init__(self, working_dir: str = None):
        """
        Initialize CLI MCP Server

        Args:
            working_dir: Working directory for command execution
        """
        self.working_dir = Path(working_dir) if working_dir else Path.cwd()

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools"""
        return [
            {
                "name": "cli_execute",
                "description": "Execute a shell command",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {"type": "string", "description": "Command to execute"},
                        "timeout": {"type": "integer", "description": "Timeout in seconds (default: 300)"}
                    },
                    "required": ["command"]
                }
            },
            {
                "name": "cli_run_tests",
                "description": "Run project tests",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "test_command": {"type": "string", "description": "Test command (default: pytest)"}
                    }
                }
            },
            {
                "name": "cli_build",
                "description": "Build the project",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "build_command": {"type": "string", "description": "Build command"}
                    }
                }
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        try:
            if tool_name == "cli_execute":
                return self.cli_execute(
                    arguments["command"],
                    arguments.get("timeout", 300)
                )
            elif tool_name == "cli_run_tests":
                return self.cli_run_tests(arguments.get("test_command", "pytest"))
            elif tool_name == "cli_build":
                return self.cli_build(arguments.get("build_command", ""))
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cli_execute(self, command: str, timeout: int = 300) -> Dict[str, Any]:
        """Execute a shell command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=self.working_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cli_run_tests(self, test_command: str = "pytest") -> Dict[str, Any]:
        """Run tests"""
        return self.cli_execute(test_command)

    def cli_build(self, build_command: str) -> Dict[str, Any]:
        """Build project"""
        if not build_command:
            return {"success": False, "error": "Build command not specified"}
        return self.cli_execute(build_command)
