"""
Filesystem MCP Server
Provides file system operations as MCP tools.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List


class FilesystemMCPServer:
    """MCP Server for filesystem operations"""

    def __init__(self, base_path: str = None):
        """
        Initialize Filesystem MCP Server

        Args:
            base_path: Base directory for file operations (defaults to current directory)
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools"""
        return [
            {
                "name": "fs_read",
                "description": "Read content from a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path relative to base path"}
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "fs_write",
                "description": "Write content to a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path relative to base path"},
                        "content": {"type": "string", "description": "Content to write"}
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "fs_list",
                "description": "List files and directories",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path (defaults to base path)"}
                    }
                }
            },
            {
                "name": "fs_create_dir",
                "description": "Create a directory",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "Directory path to create"}
                    },
                    "required": ["path"]
                }
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        try:
            if tool_name == "fs_read":
                return self.fs_read(arguments["path"])
            elif tool_name == "fs_write":
                return self.fs_write(arguments["path"], arguments["content"])
            elif tool_name == "fs_list":
                return self.fs_list(arguments.get("path", ""))
            elif tool_name == "fs_create_dir":
                return self.fs_create_dir(arguments["path"])
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def fs_read(self, path: str) -> Dict[str, Any]:
        """Read file content"""
        full_path = self.base_path / path
        if not full_path.exists():
            return {"success": False, "error": f"File not found: {path}"}

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content, "path": str(full_path)}
        except Exception as e:
            return {"success": False, "error": f"Failed to read file: {str(e)}"}

    def fs_write(self, path: str, content: str) -> Dict[str, Any]:
        """Write content to file"""
        full_path = self.base_path / path

        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "path": str(full_path), "bytes_written": len(content)}
        except Exception as e:
            return {"success": False, "error": f"Failed to write file: {str(e)}"}

    def fs_list(self, path: str = "") -> Dict[str, Any]:
        """List directory contents"""
        full_path = self.base_path / path if path else self.base_path

        if not full_path.exists():
            return {"success": False, "error": f"Directory not found: {path}"}

        try:
            items = []
            for item in full_path.iterdir():
                items.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                    "size": item.stat().st_size if item.is_file() else None
                })
            return {"success": True, "path": str(full_path), "items": items}
        except Exception as e:
            return {"success": False, "error": f"Failed to list directory: {str(e)}"}

    def fs_create_dir(self, path: str) -> Dict[str, Any]:
        """Create directory"""
        full_path = self.base_path / path

        try:
            full_path.mkdir(parents=True, exist_ok=True)
            return {"success": True, "path": str(full_path)}
        except Exception as e:
            return {"success": False, "error": f"Failed to create directory: {str(e)}"}

