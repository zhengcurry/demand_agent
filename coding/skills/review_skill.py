"""
Review Skill
Reviews existing code for quality, security, and best practices.
"""
import json
from typing import Dict, Any, List
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from agents.code_reviewer import CodeReviewer
from mcp_servers.filesystem_server import FilesystemMCPServer


class ReviewSkill:
    """
    /review skill - Code review workflow
    """

    def __init__(self, api_key: str, project_path: str = None):
        """
        Initialize Review Skill

        Args:
            api_key: Anthropic API key
            project_path: Path to project directory
        """
        self.api_key = api_key
        self.project_path = Path(project_path) if project_path else Path.cwd()

        # Initialize agent
        self.code_reviewer = CodeReviewer(api_key)

        # Initialize MCP server
        self.fs_server = FilesystemMCPServer(str(self.project_path))

    def execute(self, files: List[str] = None, requirement_path: str = None) -> Dict[str, Any]:
        """
        Execute code review workflow

        Args:
            files: List of files to review (if None, review all Python files)
            requirement_path: Path to requirement document

        Returns:
            Review workflow result
        """
        print_safe("🔍 Starting /review workflow...")

        try:
            # Get files to review
            if not files:
                files = self._find_python_files()

            if not files:
                return {"success": False, "error": "No files found to review"}

            print_safe(f"\n📁 Found {len(files)} files to review")

            # Load requirement if provided
            requirement = {}
            if requirement_path:
                req_result = self.fs_server.fs_read(requirement_path)
                if req_result.get("success"):
                    try:
                        requirement = json.loads(req_result["content"])
                    except:
                        pass

            # Read all files
            code_files = []
            for file_path in files:
                read_result = self.fs_server.fs_read(file_path)
                if read_result.get("success"):
                    code_files.append({
                        "path": file_path,
                        "content": read_result["content"]
                    })

            # Perform review
            print_safe("\n🔍 Reviewing code...")
            review_result = self.code_reviewer.review(
                {"files": code_files},
                requirement
            )

            if not review_result.get("success"):
                return {"success": False, "error": "Code review failed", "details": review_result}

            review = review_result["review"]

            # Display results
            print_safe(f"\n📊 Review Results:")
            print_safe(f"  Overall Score: {review.get('overall_score', 0)}/100")
            print_safe(f"  Issues Found: {len(review.get('issues', []))}")

            # Display critical issues
            critical_issues = [i for i in review.get("issues", []) if i.get("severity") == "critical"]
            if critical_issues:
                print_safe(f"\n⚠️  Critical Issues ({len(critical_issues)}):")
                for issue in critical_issues[:5]:
                    print_safe(f"    - {issue.get('file')}: {issue.get('description')}")

            # Save review report
            self._save_review(review)

            print_safe("\n🎉 /review workflow completed!")
            return {"success": True, "review": review}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _find_python_files(self) -> List[str]:
        """Find all Python files in project"""
        python_files = []
        for path in self.project_path.rglob("*.py"):
            if ".venv" not in str(path) and "venv" not in str(path):
                rel_path = path.relative_to(self.project_path)
                python_files.append(str(rel_path))
        return python_files

    def _save_review(self, review: Dict[str, Any]):
        """Save review report"""
        self.fs_server.fs_create_dir("docs")
        self.fs_server.fs_write(
            "docs/code_review.json",
            json.dumps(review, indent=2)
        )
        print_safe("\n📄 Review report saved to docs/code_review.json")
