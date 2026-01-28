"""
Enhanced Code Skill
Complete workflow with stage-by-stage reports and review checkpoints.

Features:
- Stage-by-stage execution with detailed reports
- Manual/Auto review checkpoints
- Comprehensive documentation at each stage
- Flexible pause and resume capability
"""
import os
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

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


class EnhancedCodeSkill:
    """
    Enhanced /code skill with stage-by-stage reports and review checkpoints
    """

    def __init__(self, api_key: str, project_path: str = None):
        """
        Initialize Enhanced Code Skill

        Args:
            api_key: Anthropic API key
            project_path: Path to project directory
        """
        self.api_key = api_key
        self.project_path = Path(project_path) if project_path else Path.cwd()

        # Initialize agents (using Sonnet for all agents for compatibility)
        self.requirement_analyst = RequirementAnalyst(api_key, model="claude-sonnet-4-5-20250929")
        self.system_architect = SystemArchitect(api_key, model="claude-sonnet-4-5-20250929")
        self.api_designer = APIDesigner(api_key, model="claude-sonnet-4-5-20250929")
        self.task_planner = TaskPlanner(api_key, model="claude-sonnet-4-5-20250929")
        self.code_generator = CodeGenerator(api_key, model="claude-sonnet-4-5-20250929")
        self.code_reviewer = CodeReviewer(api_key, model="claude-sonnet-4-5-20250929")

        # Initialize MCP servers
        self.fs_server = FilesystemMCPServer(str(self.project_path))
        self.git_server = GitMCPServer(str(self.project_path))

        # Workflow state
        self.workflow_state = {
            "current_stage": None,
            "stages_completed": [],
            "reports": {},
            "timestamp": datetime.now().isoformat()
        }

    def execute(self, requirement: str, review_mode: str = "auto",
                pause_for_review: bool = False) -> Dict[str, Any]:
        """
        Execute complete code generation workflow with stage reports

        Args:
            requirement: Requirement description
            review_mode: Review mode ('auto' or 'manual')
            pause_for_review: Whether to pause after design stage for review

        Returns:
            Workflow execution result with all stage reports
        """
        print_safe("=" * 70)
        print_safe("🚀 Enhanced Code Generation Workflow")
        print_safe("=" * 70)
        print_safe(f"Review Mode: {review_mode.upper()}")
        print_safe(f"Pause for Review: {'Yes' if pause_for_review else 'No'}")
        print_safe("=" * 70)

        try:
            # Stage 1: Requirement Analysis
            stage1_result = self._stage1_requirement_analysis(requirement)
            if not stage1_result["success"]:
                return stage1_result

            # Stage 2: Design (Architecture + API)
            stage2_result = self._stage2_design(stage1_result["data"])
            if not stage2_result["success"]:
                return stage2_result

            # Stage 3: Design Review (Manual or Auto)
            if pause_for_review and review_mode == "manual":
                # Save current state and wait for manual review
                self._save_checkpoint(stage2_result["data"])
                return {
                    "success": True,
                    "status": "paused_for_review",
                    "message": "Workflow paused for manual review. Use resume() to continue.",
                    "reports": self.workflow_state["reports"],
                    "checkpoint_path": str(self.project_path / "docs" / "workflow_checkpoint.json")
                }

            stage3_result = self._stage3_design_review(
                stage2_result["data"],
                review_mode
            )
            if not stage3_result["success"]:
                return stage3_result

            # Check if design review passed
            if not stage3_result["data"]["review_passed"]:
                return {
                    "success": False,
                    "error": "Design review failed. Please address the issues and retry.",
                    "reports": self.workflow_state["reports"]
                }

            # Stage 4: Task Planning
            stage4_result = self._stage4_task_planning(stage3_result["data"])
            if not stage4_result["success"]:
                return stage4_result

            # Stage 5: Code Generation
            stage5_result = self._stage5_code_generation(stage4_result["data"])
            if not stage5_result["success"]:
                return stage5_result

            # Stage 6: Code Review
            stage6_result = self._stage6_code_review(stage5_result["data"])
            if not stage6_result["success"]:
                return stage6_result

            # Save all reports
            self._save_all_reports()

            print_safe("\n" + "=" * 70)
            print_safe("🎉 Workflow Completed Successfully!")
            print_safe("=" * 70)
            self._print_summary()

            return {
                "success": True,
                "status": "completed",
                "reports": self.workflow_state["reports"],
                "generated_files": stage5_result["data"]["generated_files"],
                "final_score": stage6_result["data"]["review"]["overall_score"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "stage": self.workflow_state.get("current_stage"),
                "reports": self.workflow_state.get("reports", {})
            }

    def _stage1_requirement_analysis(self, requirement: str) -> Dict[str, Any]:
        """Stage 1: Requirement Analysis"""
        self.workflow_state["current_stage"] = "stage1_requirement_analysis"

        print_safe("\n" + "=" * 70)
        print_safe("📋 Stage 1/6: Requirement Analysis")
        print_safe("=" * 70)

        try:
            req_result = self.requirement_analyst.analyze(requirement)
            if not req_result.get("success"):
                return {"success": False, "error": "Requirement analysis failed", "details": req_result}

            # Generate stage report
            report = {
                "stage": "requirement_analysis",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "input": requirement,
                "output": req_result["requirement"],
                "summary": {
                    "requirement_type": req_result["requirement"].get("type", "unknown"),
                    "complexity": req_result["requirement"].get("complexity", "medium"),
                    "estimated_tasks": req_result["requirement"].get("estimated_tasks", 0)
                }
            }

            self.workflow_state["reports"]["stage1_requirement"] = report
            self.workflow_state["stages_completed"].append("stage1")

            print_safe("✅ Requirements analyzed successfully")
            print_safe(f"   Type: {report['summary']['requirement_type']}")
            print_safe(f"   Complexity: {report['summary']['complexity']}")
            print_safe(f"   Estimated Tasks: {report['summary']['estimated_tasks']}")

            return {
                "success": True,
                "data": {"requirement": req_result["requirement"]}
            }

        except Exception as e:
            return {"success": False, "error": f"Stage 1 failed: {str(e)}"}

    def _stage2_design(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 2: Architecture and API Design"""
        self.workflow_state["current_stage"] = "stage2_design"

        print_safe("\n" + "=" * 70)
        print_safe("🏗️  Stage 2/6: Design (Architecture + API)")
        print_safe("=" * 70)

        try:
            requirement = context["requirement"]

            # Architecture Design
            print_safe("\n  [2.1] Designing architecture...")
            arch_result = self.system_architect.design(requirement)
            if not arch_result.get("success"):
                return {"success": False, "error": "Architecture design failed", "details": arch_result}
            print_safe("  ✅ Architecture designed")

            # API Design
            print_safe("\n  [2.2] Designing API...")
            api_result = self.api_designer.design(requirement, arch_result["architecture"])
            if not api_result.get("success"):
                return {"success": False, "error": "API design failed", "details": api_result}
            print_safe("  ✅ API designed")

            # Generate stage report
            report = {
                "stage": "design",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "architecture": arch_result["architecture"],
                "api_spec": api_result["api_spec"],
                "summary": {
                    "components": len(arch_result["architecture"].get("tech_stack", {}).get("backend", [])),
                    "endpoints": len(api_result["api_spec"].get("paths", {})),
                    "data_models": len(arch_result["architecture"].get("data_model", []))
                }
            }

            self.workflow_state["reports"]["stage2_design"] = report
            self.workflow_state["stages_completed"].append("stage2")

            print_safe("\n✅ Design phase completed")
            print_safe(f"   Components: {report['summary']['components']}")
            print_safe(f"   API Endpoints: {report['summary']['endpoints']}")
            print_safe(f"   Data Models: {report['summary']['data_models']}")

            return {
                "success": True,
                "data": {
                    "requirement": requirement,
                    "architecture": arch_result["architecture"],
                    "api_spec": api_result["api_spec"]
                }
            }

        except Exception as e:
            return {"success": False, "error": f"Stage 2 failed: {str(e)}"}

    def _stage3_design_review(self, context: Dict[str, Any], review_mode: str) -> Dict[str, Any]:
        """Stage 3: Design Review (Auto or Manual)"""
        self.workflow_state["current_stage"] = "stage3_design_review"

        print_safe("\n" + "=" * 70)
        print_safe(f"🔍 Stage 3/6: Design Review ({review_mode.upper()})")
        print_safe("=" * 70)

        try:
            architecture = context["architecture"]
            api_spec = context["api_spec"]

            if review_mode == "auto":
                # Automated design review
                review_result = self._auto_review_design(architecture, api_spec)
            else:
                # Manual review (simulated for now, in real scenario would wait for user input)
                print_safe("⚠️  Manual review mode selected.")
                print_safe("   In production, this would pause for human review.")
                print_safe("   For demo purposes, using auto-review...")
                review_result = self._auto_review_design(architecture, api_spec)

            # Generate stage report
            report = {
                "stage": "design_review",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "review_mode": review_mode,
                "review_result": review_result,
                "summary": {
                    "review_passed": review_result["passed"],
                    "total_issues": len(review_result.get("issues", [])),
                    "critical_issues": len([i for i in review_result.get("issues", []) if i["severity"] == "critical"]),
                    "suggestions": len(review_result.get("suggestions", []))
                }
            }

            self.workflow_state["reports"]["stage3_design_review"] = report
            self.workflow_state["stages_completed"].append("stage3")

            print_safe(f"\n✅ Design review completed: {'PASSED' if review_result['passed'] else 'FAILED'}")
            print_safe(f"   Total Issues: {report['summary']['total_issues']}")
            print_safe(f"   Critical Issues: {report['summary']['critical_issues']}")
            print_safe(f"   Suggestions: {report['summary']['suggestions']}")

            return {
                "success": True,
                "data": {
                    **context,
                    "design_review": review_result,
                    "review_passed": review_result["passed"]
                }
            }

        except Exception as e:
            return {"success": False, "error": f"Stage 3 failed: {str(e)}"}

    def _stage4_task_planning(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 4: Task Planning and Decomposition"""
        self.workflow_state["current_stage"] = "stage4_task_planning"

        print_safe("\n" + "=" * 70)
        print_safe("📝 Stage 4/6: Task Planning and Decomposition")
        print_safe("=" * 70)

        try:
            print_safe("\n  Planning tasks (this may take 30-60 seconds)...")

            task_result = self.task_planner.plan(
                context["requirement"],
                context["architecture"],
                context["api_spec"]
            )

            if not task_result.get("success"):
                error_msg = task_result.get("error", "Unknown error")
                print_safe(f"\n  ⚠️  Task planning failed: {error_msg}")

                # Log more details if available
                if "raw_response" in task_result:
                    print_safe(f"  Raw response (first 500 chars): {task_result['raw_response'][:500]}")

                return {
                    "success": False,
                    "error": f"Task planning failed: {error_msg}",
                    "details": task_result
                }

            task_plan = task_result["task_plan"]

            # Generate stage report
            report = {
                "stage": "task_planning",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "task_plan": task_plan,
                "summary": {
                    "total_tasks": len(task_plan.get("tasks", [])),
                    "task_breakdown": self._analyze_tasks(task_plan.get("tasks", [])),
                    "estimated_effort": task_plan.get("estimated_effort", "unknown")
                }
            }

            self.workflow_state["reports"]["stage4_task_planning"] = report
            self.workflow_state["stages_completed"].append("stage4")

            print_safe(f"\n✅ Task planning completed")
            print_safe(f"   Total Tasks: {report['summary']['total_tasks']}")
            print_safe(f"   Task Breakdown:")
            for task_type, count in report['summary']['task_breakdown'].items():
                print_safe(f"      - {task_type}: {count}")

            return {
                "success": True,
                "data": {
                    **context,
                    "task_plan": task_plan
                }
            }

        except Exception as e:
            print_safe(f"\n  ⚠️  Exception in task planning: {str(e)}")
            import traceback
            traceback.print_exc()
            return {"success": False, "error": f"Stage 4 failed: {str(e)}"}

    def _stage5_code_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 5: Code Generation"""
        self.workflow_state["current_stage"] = "stage5_code_generation"

        print_safe("\n" + "=" * 70)
        print_safe("💻 Stage 5/6: Code Generation")
        print_safe("=" * 70)

        try:
            task_plan = context["task_plan"]
            generated_files = []
            completed_tasks = []
            failed_tasks = []

            gen_context = {
                "requirement": context["requirement"],
                "architecture": context["architecture"],
                "api_spec": context["api_spec"]
            }

            total_tasks = len(task_plan.get("tasks", []))
            print_safe(f"\n  Generating code for {total_tasks} tasks...\n")

            for i, task in enumerate(task_plan.get("tasks", []), 1):
                print_safe(f"  [{i}/{total_tasks}] {task.get('title', 'Unknown task')}")

                code_result = self.code_generator.generate(task, gen_context)
                if not code_result.get("success"):
                    print_safe(f"      ⚠️  Failed to generate code")
                    failed_tasks.append(task["id"])
                    continue

                # Write generated files
                code_data = code_result["code"]
                for file_info in code_data.get("files", []):
                    file_path = file_info["path"]
                    content = file_info["content"]

                    write_result = self.fs_server.fs_write(file_path, content)
                    if write_result.get("success"):
                        generated_files.append(file_path)
                        print_safe(f"      ✅ {file_path}")

                # Write test files
                for test_info in code_data.get("tests", []):
                    test_path = test_info["path"]
                    content = test_info["content"]

                    write_result = self.fs_server.fs_write(test_path, content)
                    if write_result.get("success"):
                        generated_files.append(test_path)
                        print_safe(f"      ✅ {test_path} (test)")

                completed_tasks.append(task["id"])

            # Generate stage report
            report = {
                "stage": "code_generation",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "generated_files": generated_files,
                "summary": {
                    "total_tasks": total_tasks,
                    "completed_tasks": len(completed_tasks),
                    "failed_tasks": len(failed_tasks),
                    "total_files": len(generated_files),
                    "success_rate": f"{(len(completed_tasks) / total_tasks * 100):.1f}%"
                }
            }

            self.workflow_state["reports"]["stage5_code_generation"] = report
            self.workflow_state["stages_completed"].append("stage5")

            print_safe(f"\n✅ Code generation completed")
            print_safe(f"   Generated Files: {len(generated_files)}")
            print_safe(f"   Success Rate: {report['summary']['success_rate']}")

            return {
                "success": True,
                "data": {
                    **context,
                    "generated_files": generated_files,
                    "completed_tasks": completed_tasks
                }
            }

        except Exception as e:
            return {"success": False, "error": f"Stage 5 failed: {str(e)}"}

    def _stage6_code_review(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Stage 6: Code Review"""
        self.workflow_state["current_stage"] = "stage6_code_review"

        print_safe("\n" + "=" * 70)
        print_safe("✅ Stage 6/6: Code Review")
        print_safe("=" * 70)

        try:
            generated_files = context["generated_files"]

            print_safe(f"\n  Reviewing {len(generated_files)} files...\n")

            review_result = self.code_reviewer.review(
                {"files": generated_files},
                context["requirement"]
            )

            if not review_result.get("success"):
                print_safe("  ⚠️  Code review encountered issues")
                review = {"overall_score": 0, "issues": [], "suggestions": []}
            else:
                review = review_result["review"]

            # Generate stage report
            report = {
                "stage": "code_review",
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "review": review,
                "summary": {
                    "overall_score": review.get("overall_score", 0),
                    "total_issues": len(review.get("issues", [])),
                    "critical_issues": len([i for i in review.get("issues", []) if i.get("severity") == "critical"]),
                    "total_suggestions": len(review.get("suggestions", [])),
                    "quality_level": self._get_quality_level(review.get("overall_score", 0))
                }
            }

            self.workflow_state["reports"]["stage6_code_review"] = report
            self.workflow_state["stages_completed"].append("stage6")

            print_safe(f"\n✅ Code review completed")
            print_safe(f"   Overall Score: {report['summary']['overall_score']}/100")
            print_safe(f"   Quality Level: {report['summary']['quality_level']}")
            print_safe(f"   Total Issues: {report['summary']['total_issues']}")
            print_safe(f"   Critical Issues: {report['summary']['critical_issues']}")

            return {
                "success": True,
                "data": {
                    **context,
                    "review": review
                }
            }

        except Exception as e:
            return {"success": False, "error": f"Stage 6 failed: {str(e)}"}

    def _auto_review_design(self, architecture: Dict, api_spec: Dict) -> Dict[str, Any]:
        """Automated design review"""
        issues = []
        suggestions = []

        # Check architecture completeness (warnings only, not critical)
        if not architecture.get("tech_stack"):
            issues.append({
                "severity": "high",
                "message": "No tech stack defined in architecture"
            })
        else:
            # Check if tech_stack has content
            tech_stack = architecture.get("tech_stack", {})
            if not any(tech_stack.values()):
                issues.append({
                    "severity": "medium",
                    "message": "Tech stack is defined but empty"
                })

        if not architecture.get("data_model"):
            issues.append({
                "severity": "medium",
                "message": "No data models defined (may be acceptable for simple APIs)"
            })

        # Check API spec (OpenAPI format) - only critical if completely missing
        if not api_spec:
            issues.append({
                "severity": "critical",
                "message": "API specification is missing"
            })
        elif not api_spec.get("paths"):
            issues.append({
                "severity": "high",
                "message": "No API paths defined in specification"
            })
        elif len(api_spec.get("paths", {})) == 0:
            issues.append({
                "severity": "high",
                "message": "API paths object is empty"
            })

        # Add suggestions
        data_models = architecture.get("data_model", [])
        if len(data_models) > 10:
            suggestions.append("Consider breaking down into microservices")

        paths_count = len(api_spec.get("paths", {}))
        if paths_count > 20:
            suggestions.append("Large number of endpoints - consider API versioning")

        # Only fail on critical issues
        critical_count = len([i for i in issues if i["severity"] == "critical"])
        passed = critical_count == 0

        return {
            "passed": passed,
            "issues": issues,
            "suggestions": suggestions,
            "timestamp": datetime.now().isoformat()
        }

    def _analyze_tasks(self, tasks: List[Dict]) -> Dict[str, int]:
        """Analyze task breakdown by type"""
        breakdown = {}
        for task in tasks:
            task_type = task.get("type", "other")
            breakdown[task_type] = breakdown.get(task_type, 0) + 1
        return breakdown

    def _get_quality_level(self, score: int) -> str:
        """Get quality level from score"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Acceptable"
        elif score >= 60:
            return "Needs Improvement"
        else:
            return "Poor"

    def _save_checkpoint(self, data: Dict[str, Any]):
        """Save workflow checkpoint for manual review"""
        checkpoint = {
            "workflow_state": self.workflow_state,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        self.fs_server.fs_create_dir("docs")
        self.fs_server.fs_write(
            "docs/workflow_checkpoint.json",
            json.dumps(checkpoint, indent=2)
        )

    def _save_all_reports(self):
        """Save all stage reports to files"""
        self.fs_server.fs_create_dir("docs")

        # Save individual stage reports
        for stage_name, report in self.workflow_state["reports"].items():
            filename = f"docs/{stage_name}_report.json"
            self.fs_server.fs_write(
                filename,
                json.dumps(report, indent=2)
            )

        # Save complete workflow report
        workflow_report = {
            "workflow_status": "completed",
            "timestamp": datetime.now().isoformat(),
            "stages_completed": self.workflow_state["stages_completed"],
            "reports": self.workflow_state["reports"]
        }

        self.fs_server.fs_write(
            "docs/complete_workflow_report.json",
            json.dumps(workflow_report, indent=2)
        )

    def _print_summary(self):
        """Print workflow summary"""
        reports = self.workflow_state["reports"]

        print_safe("\n📊 Workflow Summary:")
        print_safe(f"   Stages Completed: {len(self.workflow_state['stages_completed'])}/6")

        if "stage1_requirement" in reports:
            req = reports["stage1_requirement"]["summary"]
            print_safe(f"\n   📋 Requirements: {req['requirement_type']} ({req['complexity']})")

        if "stage2_design" in reports:
            design = reports["stage2_design"]["summary"]
            print_safe(f"   🏗️  Design: {design['components']} components, {design['endpoints']} endpoints")

        if "stage3_design_review" in reports:
            review = reports["stage3_design_review"]["summary"]
            print_safe(f"   🔍 Design Review: {'PASSED' if review['review_passed'] else 'FAILED'}")

        if "stage4_task_planning" in reports:
            tasks = reports["stage4_task_planning"]["summary"]
            print_safe(f"   📝 Tasks: {tasks['total_tasks']} tasks planned")

        if "stage5_code_generation" in reports:
            code = reports["stage5_code_generation"]["summary"]
            print_safe(f"   💻 Code Generation: {code['total_files']} files ({code['success_rate']})")

        if "stage6_code_review" in reports:
            review = reports["stage6_code_review"]["summary"]
            print_safe(f"   ✅ Code Review: {review['overall_score']}/100 ({review['quality_level']})")

        print_safe(f"\n   📄 Reports saved in: {self.project_path / 'docs'}")
