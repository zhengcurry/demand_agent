"""
Design Skill
Executes only the design phase (requirement analysis + architecture + API design).
"""
import json
from typing import Dict, Any
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from agents.api_designer import APIDesigner
from mcp_servers.filesystem_server import FilesystemMCPServer


class DesignSkill:
    """
    /design skill - Design phase only workflow
    """

    def __init__(self, api_key: str, project_path: str = None):
        """
        Initialize Design Skill

        Args:
            api_key: Anthropic API key
            project_path: Path to project directory
        """
        self.api_key = api_key
        self.project_path = Path(project_path) if project_path else Path.cwd()

        # Initialize agents
        self.requirement_analyst = RequirementAnalyst(api_key)
        self.system_architect = SystemArchitect(api_key)
        self.api_designer = APIDesigner(api_key)

        # Initialize MCP server
        self.fs_server = FilesystemMCPServer(str(self.project_path))

    def execute(self, requirement: str) -> Dict[str, Any]:
        """
        Execute design workflow

        Args:
            requirement: Requirement description

        Returns:
            Design workflow result
        """
        print_safe("🎨 Starting /design workflow...")
        results = {}

        try:
            # Step 1: Requirement Analysis
            print_safe("\n📋 Step 1: Analyzing requirements...")
            req_result = self.requirement_analyst.analyze(requirement)
            if not req_result.get("success"):
                return {"success": False, "error": "Requirement analysis failed", "details": req_result}
            results["requirement"] = req_result["requirement"]
            print_safe("✅ Requirements analyzed")

            # Step 2: Architecture Design
            print_safe("\n🏗️  Step 2: Designing architecture...")
            arch_result = self.system_architect.design(results["requirement"])
            if not arch_result.get("success"):
                return {"success": False, "error": "Architecture design failed", "details": arch_result}
            results["architecture"] = arch_result["architecture"]
            print_safe("✅ Architecture designed")

            # Step 3: API Design
            print_safe("\n🔌 Step 3: Designing API...")
            api_result = self.api_designer.design(results["requirement"], results["architecture"])
            if not api_result.get("success"):
                return {"success": False, "error": "API design failed", "details": api_result}
            results["api_spec"] = api_result["api_spec"]
            print_safe("✅ API designed")

            # Save design documents
            self._save_results(results)

            print_safe("\n🎉 /design workflow completed successfully!")
            return {"success": True, "results": results}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _save_results(self, results: Dict[str, Any]):
        """Save design results to files"""
        self.fs_server.fs_create_dir("docs")

        # Save requirement
        self.fs_server.fs_write(
            "docs/requirement.json",
            json.dumps(results.get("requirement", {}), indent=2)
        )

        # Save architecture
        self.fs_server.fs_write(
            "docs/architecture.json",
            json.dumps(results.get("architecture", {}), indent=2)
        )

        # Save API spec
        self.fs_server.fs_write(
            "docs/api_spec.json",
            json.dumps(results.get("api_spec", {}), indent=2)
        )

        print_safe("\n📄 Design documents saved to docs/")
