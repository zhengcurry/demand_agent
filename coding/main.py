"""
Main entry point for the AI Development Toolkit
"""
import os
import sys
import argparse
from pathlib import Path

from env_config import get_api_key, check_environment
from skills.code_skill import CodeSkill
from skills.design_skill import DesignSkill
from skills.review_skill import ReviewSkill
from skills.refactor_skill import RefactorSkill


def main():
    parser = argparse.ArgumentParser(
        description="AI Development Toolkit - From requirements to code"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # /code command
    code_parser = subparsers.add_parser("code", help="Generate code from requirements")
    code_parser.add_argument("requirement", help="Requirement description")
    code_parser.add_argument("--mode", choices=["auto", "semi-auto", "manual"],
                            default="auto", help="Execution mode")
    code_parser.add_argument("--from-feishu", help="Feishu document URL")
    code_parser.add_argument("--project-path", default=".", help="Project path")

    # /design command
    design_parser = subparsers.add_parser("design", help="Create design documents")
    design_parser.add_argument("requirement", help="Requirement description")
    design_parser.add_argument("--project-path", default=".", help="Project path")

    # /review command
    review_parser = subparsers.add_parser("review", help="Review existing code")
    review_parser.add_argument("--files", nargs="+", help="Files to review")
    review_parser.add_argument("--requirement-path", help="Path to requirement document")
    review_parser.add_argument("--project-path", default=".", help="Project path")

    # /refactor command
    refactor_parser = subparsers.add_parser("refactor", help="Refactor existing code")
    refactor_parser.add_argument("--files", nargs="+", required=True, help="Files to refactor")
    refactor_parser.add_argument("--goal", required=True, help="Refactoring goal")
    refactor_parser.add_argument("--project-path", default=".", help="Project path")

    args = parser.parse_args()

    # Get API key using the configuration loader
    api_key = get_api_key()
    if not api_key:
        sys.exit(1)

    # Execute command
    if args.command == "code":
        skill = CodeSkill(api_key=api_key, project_path=args.project_path)
        result = skill.execute(
            requirement=args.requirement,
            mode=args.mode,
            from_feishu=args.from_feishu
        )

    elif args.command == "design":
        skill = DesignSkill(api_key=api_key, project_path=args.project_path)
        result = skill.execute(requirement=args.requirement)

    elif args.command == "review":
        skill = ReviewSkill(api_key=api_key, project_path=args.project_path)
        result = skill.execute(
            files=args.files,
            requirement_path=args.requirement_path
        )

    elif args.command == "refactor":
        skill = RefactorSkill(api_key=api_key, project_path=args.project_path)
        result = skill.execute(files=args.files, refactor_goal=args.goal)

    else:
        parser.print_help()
        sys.exit(1)

    # Print result
    if result.get("success"):
        print("\n✅ Command completed successfully!")
    else:
        print(f"\n❌ Command failed: {result.get('error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
