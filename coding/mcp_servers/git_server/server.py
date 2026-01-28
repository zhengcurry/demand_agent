"""
Git MCP Server
Provides Git operations as MCP tools.
"""
import subprocess
from pathlib import Path
from typing import Dict, Any, List


class GitMCPServer:
    """MCP Server for Git operations"""

    def __init__(self, repo_path: str = None):
        """
        Initialize Git MCP Server

        Args:
            repo_path: Path to Git repository (defaults to current directory)
        """
        self.repo_path = Path(repo_path) if repo_path else Path.cwd()

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools"""
        return [
            {
                "name": "git_init",
                "description": "Initialize a Git repository",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "git_add",
                "description": "Add files to staging area",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "files": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of file paths to add"
                        }
                    },
                    "required": ["files"]
                }
            },
            {
                "name": "git_commit",
                "description": "Commit staged changes",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Commit message"}
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "git_diff",
                "description": "Show changes in working directory",
                "input_schema": {"type": "object", "properties": {}}
            },
            {
                "name": "git_status",
                "description": "Show working tree status",
                "input_schema": {"type": "object", "properties": {}}
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        try:
            if tool_name == "git_init":
                return self.git_init()
            elif tool_name == "git_add":
                return self.git_add(arguments["files"])
            elif tool_name == "git_commit":
                return self.git_commit(arguments["message"])
            elif tool_name == "git_diff":
                return self.git_diff()
            elif tool_name == "git_status":
                return self.git_status()
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _run_git_command(self, args: List[str]) -> Dict[str, Any]:
        """Run a Git command"""
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return {"success": True, "output": result.stdout, "stderr": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": e.stderr or str(e)}

    def git_init(self) -> Dict[str, Any]:
        """Initialize Git repository"""
        return self._run_git_command(["init"])

    def git_add(self, files: List[str]) -> Dict[str, Any]:
        """Add files to staging area"""
        return self._run_git_command(["add"] + files)

    def git_commit(self, message: str) -> Dict[str, Any]:
        """Commit staged changes"""
        return self._run_git_command(["commit", "-m", message])

    def git_diff(self) -> Dict[str, Any]:
        """Show changes"""
        return self._run_git_command(["diff"])

    def git_status(self) -> Dict[str, Any]:
        """Show status"""
        return self._run_git_command(["status"])
