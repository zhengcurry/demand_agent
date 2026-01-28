"""
Example: Using Enhanced Code Skill with stage reports and review checkpoints
"""
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from utils import print_safe
from env_config import get_api_key
from skills.enhanced_code_skill import EnhancedCodeSkill


def example_auto_workflow():
    """Example 1: Fully automated workflow with auto-review"""
    print_safe("\n" + "="*80)
    print_safe("Example 1: Fully Automated Workflow (Auto-Review)")
    print_safe("="*80)

    api_key = get_api_key()
    if not api_key:
        return

    # Define requirement
    requirement = """
    开发一个用户认证系统:

    功能需求:
    1. 用户注册功能（邮箱验证）
    2. 用户登录功能（支持记住我）
    3. 密码重置功能
    4. 用户信息管理

    技术要求:
    - 后端: Python + FastAPI
    - 数据库: PostgreSQL
    - 身份验证: JWT Token
    - 密码加密: bcrypt

    非功能需求:
    - 安全性高
    - API文档完善
    - 包含单元测试
    """

    # Initialize enhanced skill
    skill = EnhancedCodeSkill(
        api_key=api_key,
        project_path="./auth_system_auto"
    )

    # Execute with auto-review (no pause)
    result = skill.execute(
        requirement=requirement,
        review_mode="auto",
        pause_for_review=False
    )

    # Print result
    if result["success"]:
        print_safe("\n✅ Workflow completed successfully!")
        print_safe(f"\nFinal Score: {result['final_score']}/100")
        print_safe(f"Generated Files: {len(result['generated_files'])}")
        print_safe(f"\nReports available in: ./auth_system_auto/docs/")
    else:
        print_safe(f"\n❌ Workflow failed: {result.get('error')}")


def example_with_manual_review_pause():
    """Example 2: Workflow with manual review checkpoint (paused)"""
    print_safe("\n" + "="*80)
    print_safe("Example 2: Workflow with Manual Review Checkpoint (Paused)")
    print_safe("="*80)

    api_key = get_api_key()
    if not api_key:
        return

    requirement = """
    开发一个简单的博客系统:

    功能需求:
    1. 文章发布和编辑
    2. 文章分类和标签
    3. 评论功能
    4. 文章搜索

    技术要求:
    - 后端: Python + Flask
    - 前端: React
    - 数据库: SQLite
    """

    skill = EnhancedCodeSkill(
        api_key=api_key,
        project_path="./blog_system_manual"
    )

    # Execute with manual review (will pause after design stage)
    result = skill.execute(
        requirement=requirement,
        review_mode="manual",
        pause_for_review=True
    )

    if result.get("status") == "paused_for_review":
        print_safe("\n⏸️  Workflow paused for manual review")
        print_safe(f"\nCheckpoint saved at: {result['checkpoint_path']}")
        print_safe("\nReview the design reports:")
        print_safe("  - docs/stage1_requirement_report.json")
        print_safe("  - docs/stage2_design_report.json")
        print_safe("\nAfter review, you can:")
        print_safe("  1. Resume: skill.resume_from_checkpoint()")
        print_safe("  2. Modify and retry")


def example_view_reports():
    """Example 3: View detailed stage reports"""
    print_safe("\n" + "="*80)
    print_safe("Example 3: Viewing Detailed Stage Reports")
    print_safe("="*80)

    import json

    # Assuming you've run example_auto_workflow first
    reports_dir = Path("./auth_system_auto/docs")

    if not reports_dir.exists():
        print_safe("⚠️  No reports found. Run example_auto_workflow() first.")
        return

    print_safe("\nAvailable Reports:")
    print_safe("-" * 80)

    report_files = [
        "stage1_requirement_report.json",
        "stage2_design_report.json",
        "stage3_design_review_report.json",
        "stage4_task_planning_report.json",
        "stage5_code_generation_report.json",
        "stage6_code_review_report.json",
        "complete_workflow_report.json"
    ]

    for report_file in report_files:
        report_path = reports_dir / report_file
        if report_path.exists():
            with open(report_path, 'r', encoding='utf-8') as f:
                report = json.load(f)

            print_safe(f"\n📄 {report_file}")
            print_safe(f"   Stage: {report.get('stage', 'N/A')}")
            print_safe(f"   Status: {report.get('status', 'N/A')}")
            print_safe(f"   Timestamp: {report.get('timestamp', 'N/A')}")

            if 'summary' in report:
                print_safe(f"   Summary:")
                for key, value in report['summary'].items():
                    print_safe(f"      - {key}: {value}")


def main():
    """Main function to run examples"""
    print_safe("="*80)
    print_safe("Enhanced Code Skill Examples")
    print_safe("="*80)
    print_safe("\nAvailable Examples:")
    print_safe("  1. Fully Automated Workflow (Auto-Review)")
    print_safe("  2. Workflow with Manual Review Checkpoint")
    print_safe("  3. View Detailed Stage Reports")
    print_safe("\n")

    choice = input("Select example (1-3, or 'all' to run all): ").strip()

    if choice == "1":
        example_auto_workflow()
    elif choice == "2":
        example_with_manual_review_pause()
    elif choice == "3":
        example_view_reports()
    elif choice.lower() == "all":
        example_auto_workflow()
        print_safe("\n" + "="*80 + "\n")
        example_with_manual_review_pause()
        print_safe("\n" + "="*80 + "\n")
        example_view_reports()
    else:
        print_safe("Invalid choice. Running example 1 by default...")
        example_auto_workflow()


if __name__ == "__main__":
    main()
