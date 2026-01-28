"""
Refactor Skill
Refactors existing code based on requirements or best practices.
"""
import json
from typing import Dict, Any, List
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from agents.code_generator import CodeGenerator
from agents.code_reviewer import CodeReviewer
from mcp_servers.filesystem_server import FilesystemMCPServer


class RefactorSkill:
    """
    /refactor skill - Code refactoring workflow
    """

    def __init__(self, api_key: str, project_path: str = None):
        """
        Initialize Refactor Skill

        Args:
            api_key: Anthropic API key
            project_path: Path to project directory
        """
        self.api_key = api_key
        self.project_path = Path(project_path) if project_path else Path.cwd()

        # Initialize agents
        self.code_generator = CodeGenerator(api_key)
        self.code_reviewer = CodeReviewer(api_key)

        # Initialize MCP server
        self.fs_server = FilesystemMCPServer(str(self.project_path))

    def execute(self, files: List[str], refactor_goal: str) -> Dict[str, Any]:
        """
        Execute refactoring workflow

        Args:
            files: List of files to refactor
            refactor_goal: Refactoring goal/description

        Returns:
            Refactoring workflow result
        """
        print_safe("🔧 Starting /refactor workflow...")

        try:
            if not files:
                return {"success": False, "error": "No files specified for refactoring"}

            print_safe(f"\n📁 Refactoring {len(files)} files")
            print_safe(f"🎯 Goal: {refactor_goal}")

            refactored_files = []

            for file_path in files:
                print_safe(f"\n  Processing: {file_path}")

                # Read original file
                read_result = self.fs_server.fs_read(file_path)
                if not read_result.get("success"):
                    print_safe(f"  ⚠️  Failed to read {file_path}")
                    continue

                original_content = read_result["content"]

                # Generate refactored version
                task = {
                    "title": f"Refactor {file_path}",
                    "description": refactor_goal,
                    "files_to_create": [{"path": file_path, "description": "Refactored version"}]
                }

                context = {
                    "original_code": original_content,
                    "refactor_goal": refactor_goal
                }

                code_result = self.code_generator.generate(task, context)
                if not code_result.get("success"):
                    print_safe(f"  ⚠️  Failed to refactor {file_path}")
                    continue

                # Get refactored content
                code_data = code_result["code"]
                if code_data.get("files"):
                    new_content = code_data["files"][0]["content"]

                    # Quick review
                    review_result = self.code_reviewer.quick_review(new_content, file_path)
                    if review_result.get("success"):
                        review = review_result["review"]
                        if review.get("has_critical_issues"):
                            print_safe(f"  ⚠️  Critical issues found, skipping")
                            continue

                    # Write refactored file
                    write_result = self.fs_server.fs_write(file_path, new_content)
                    if write_result.get("success"):
                        refactored_files.append(file_path)
                        print_safe(f"  ✅ Refactored: {file_path}")

            print_safe(f"\n✅ Refactored {len(refactored_files)} files")
            print_safe("\n🎉 /refactor workflow completed!")

            return {
                "success": True,
                "refactored_files": refactored_files,
                "total_files": len(files)
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
