"""
Quick test for Enhanced Code Skill
Tests the new stage-by-stage workflow with reports
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from skills.enhanced_code_skill import EnhancedCodeSkill


def test_enhanced_skill():
    """Quick test of enhanced code skill"""
    print_safe("="*80)
    print_safe("Quick Test: Enhanced Code Skill")
    print_safe("="*80)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    # Define a simple test requirement
    requirement = """
    

    功能需求:
    1. 支持加法、减法、乘法、除法
    2. 输入验证
    3. 错误处理

    技术要求:
    - 后端: Python + FastAPI
    - 返回JSON格式

    非功能需求:
    - 代码简洁
    - 包含单元测试
    """

    print_safe("\n[TEST] Initializing Enhanced Code Skill...")
    try:
        skill = EnhancedCodeSkill(
            api_key=api_key,
            project_path="./test_calculator_api"
        )
        print_safe("[OK] Enhanced Code Skill initialized\n")
    except Exception as e:
        print_safe(f"[ERROR] Failed to initialize: {e}")
        return False

    print_safe("[TEST] Running workflow with auto-review (no pause)...")
    print_safe("This will execute all 6 stages and generate reports.\n")

    try:
        result = skill.execute(
            requirement=requirement,
            review_mode="auto",
            pause_for_review=False
        )

        if result["success"]:
            print_safe("\n" + "="*80)
            print_safe("[SUCCESS] Enhanced Code Skill Test Passed!")
            print_safe("="*80)
            print_safe(f"\nStatus: {result.get('status')}")
            print_safe(f"Final Score: {result.get('final_score')}/100")
            print_safe(f"Generated Files: {len(result.get('generated_files', []))}")
            print_safe(f"\nReports saved in: ./test_calculator_api/docs/")
            print_safe("\nGenerated Reports:")
            print_safe("  - stage1_requirement_report.json")
            print_safe("  - stage2_design_report.json")
            print_safe("  - stage3_design_review_report.json")
            print_safe("  - stage4_task_planning_report.json")
            print_safe("  - stage5_code_generation_report.json")
            print_safe("  - stage6_code_review_report.json")
            print_safe("  - complete_workflow_report.json")
            return True
        else:
            print_safe(f"\n[ERROR] Workflow failed: {result.get('error')}")
            print_safe(f"Stage: {result.get('stage')}")
            return False

    except Exception as e:
        print_safe(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_enhanced_skill()
    sys.exit(0 if success else 1)
