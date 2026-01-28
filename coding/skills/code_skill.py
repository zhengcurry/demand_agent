"""
Code Skill
Complete workflow from requirement to code implementation.
"""
import os
import json
from typing import Dict, Any, Optional
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from agents.api_designer import APIDesigner
from agents.task_planner import TaskPlanner
from agents.code_generator import CodeGenerator
from agents.code_reviewer import CodeReviewer
from mcp_servers.filesystem_server import FilesystemMCPServer
from mcp_servers.git_server import GitMCPServer


class CodeSkill:
    """
    /code skill - Complete requirement to code workflow
    """

    def __init__(self, api_key: str, project_path: str = None):
        """
        Initialize Code Skill

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
        self.task_planner = TaskPlanner(api_key)
        self.code_generator = CodeGenerator(api_key)
        self.code_reviewer = CodeReviewer(api_key)

        # Initialize MCP servers
        self.fs_server = FilesystemMCPServer(str(self.project_path))
        self.git_server = GitMCPServer(str(self.project_path))

    def execute(self, requirement: str, mode: str = "auto",
                from_feishu: str = None) -> Dict[str, Any]:
        """
        Execute complete code generation workflow

        Args:
            requirement: Requirement description
            mode: Execution mode (auto, semi-auto, manual)
            from_feishu: Feishu document URL

        Returns:
            Workflow execution result
        """
        print_safe("🚀 Starting /code workflow...")
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

            # Step 4: Task Planning
            print_safe("\n📝 Step 4: Planning tasks...")
            task_result = self.task_planner.plan(
                results["requirement"],
                results["architecture"],
                results["api_spec"]
            )
            if not task_result.get("success"):
                return {"success": False, "error": "Task planning failed", "details": task_result}
            results["task_plan"] = task_result["task_plan"]
            print_safe(f"✅ {len(results['task_plan']['tasks'])} tasks planned")

            # Step 5: Code Generation
            print_safe("\n💻 Step 5: Generating code...")
            completed_tasks = []
            generated_files = []

            for i, task in enumerate(results["task_plan"]["tasks"], 1):
                print_safe(f"\n  Task {i}/{len(results['task_plan']['tasks'])}: {task['title']}")

                context = {
                    "requirement": results["requirement"],
                    "architecture": results["architecture"],
                    "api_spec": results["api_spec"]
                }

                code_result = self.code_generator.generate(task, context)
                if not code_result.get("success"):
                    print_safe(f"  ⚠️  Failed to generate code for task {task['id']}")
                    continue

                # Write generated files
                code_data = code_result["code"]
                for file_info in code_data.get("files", []):
                    file_path = file_info["path"]
                    content = file_info["content"]

                    write_result = self.fs_server.fs_write(file_path, content)
                    if write_result.get("success"):
                        generated_files.append(file_path)
                        print_safe(f"  ✅ Generated: {file_path}")

                # Write test files
                for test_info in code_data.get("tests", []):
                    test_path = test_info["path"]
                    content = test_info["content"]

                    write_result = self.fs_server.fs_write(test_path, content)
                    if write_result.get("success"):
                        generated_files.append(test_path)
                        print_safe(f"  ✅ Generated test: {test_path}")

                completed_tasks.append(task["id"])

            results["generated_files"] = generated_files
            print_safe(f"\n✅ Generated {len(generated_files)} files")

            # Step 6: Code Review
            print_safe("\n🔍 Step 6: Reviewing code...")
            review_result = self.code_reviewer.review(
                {"files": generated_files},
                results["requirement"]
            )
            if review_result.get("success"):
                results["review"] = review_result["review"]
                score = results["review"].get("overall_score", 0)
                print_safe(f"✅ Code review complete (Score: {score}/100)")

            # Save workflow results
            self._save_results(results)

            print_safe("\n🎉 /code workflow completed successfully!")
            return {"success": True, "results": results}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _save_results(self, results: Dict[str, Any]):
        """Save workflow results to files"""
        docs_dir = self.project_path / "docs"
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

        # Save review
        if "review" in results:
            self.fs_server.fs_write(
                "docs/code_review.json",
                json.dumps(results["review"], indent=2)
            )
