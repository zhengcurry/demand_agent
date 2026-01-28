"""
Test Self-Healing Skill
Tests the self-healing functionality with simulated errors
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from env_config import get_api_key
from skills.self_healing_skill import SelfHealingSkill
from utils import print_safe


def test_self_healing():
    """Test self-healing skill"""
    print_safe("="*70)
    print_safe("Test: Self-Healing Skill")
    print_safe("="*70)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    # Simple test requirement
    requirement = """
    开发一个简单的Hello World API:

    功能需求:
    1. 返回 "Hello, World!" 消息
    2. 支持自定义名字参数

    技术要求:
    - 后端: Python + FastAPI
    - 返回JSON格式
    """

    print_safe("\n[TEST] Initializing Self-Healing Skill...")
    try:
        skill = SelfHealingSkill(
            api_key=api_key,
            project_path="./test_self_healing",
            max_retries=2  # Use 2 retries for faster testing
        )
        print_safe("[OK] Self-Healing Skill initialized\n")
    except Exception as e:
        print_safe(f"[ERROR] Failed to initialize: {e}")
        return False

    print_safe("[TEST] Running workflow with self-healing...")
    print_safe("This will automatically retry on errors.\n")

    try:
        result = skill.execute(
            requirement=requirement,
            review_mode="auto",
            pause_for_review=False
        )

        if result.get("success"):
            print_safe("\n" + "="*70)
            print_safe("[SUCCESS] Self-Healing Skill Test Passed!")
            print_safe("="*70)
            print_safe(f"\nStatus: {result.get('status')}")
            print_safe(f"Final Score: {result.get('final_score')}/100")
            print_safe(f"Generated Files: {len(result.get('generated_files', []))}")

            # Show fix summary
            if result.get("fix_summary"):
                print_safe(f"\n[FIX SUMMARY] {result.get('fix_summary')}")
                print_safe(f"[FIX LOG] {result.get('fix_log_path')}")

            return True
        else:
            print_safe(f"\n[ERROR] Workflow failed: {result.get('error')}")

            # Show fix summary even on failure
            if result.get("fix_summary"):
                print_safe(f"\n[FIX SUMMARY] {result.get('fix_summary')}")
                print_safe(f"[FIX LOG] {result.get('fix_log_path')}")

            return False

    except Exception as e:
        print_safe(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_self_healing()
    sys.exit(0 if success else 1)
