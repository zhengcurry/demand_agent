"""
Minimal test to reproduce the task planning issue
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from skills.enhanced_code_skill import EnhancedCodeSkill


def test_minimal():
    """Minimal test with very simple requirement"""
    print_safe("="*80)
    print_safe("Minimal Test: Enhanced Code Skill")
    print_safe("="*80)

    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    # Very simple requirement
    requirement = """
    开发一个加法API:
    - 输入两个数字
    - 返回它们的和
    - 使用Python + FastAPI
    """

    print_safe("\n[TEST] Initializing...")
    skill = EnhancedCodeSkill(
        api_key=api_key,
        project_path="./test_minimal"
    )

    print_safe("\n[TEST] Running workflow...")
    try:
        result = skill.execute(
            requirement=requirement,
            review_mode="auto",
            pause_for_review=False
        )

        if result["success"]:
            print_safe("\n[SUCCESS] Test passed!")
            print_safe(f"Status: {result.get('status')}")
            if result.get('status') == 'completed':
                print_safe(f"Final Score: {result.get('final_score')}/100")
                print_safe(f"Generated Files: {len(result.get('generated_files', []))}")
            return True
        else:
            print_safe(f"\n[ERROR] Test failed: {result.get('error')}")
            print_safe(f"Stage: {result.get('stage')}")
            if 'details' in result:
                print_safe(f"Details: {result['details']}")
            return False

    except Exception as e:
        print_safe(f"\n[ERROR] Exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_minimal()
    sys.exit(0 if success else 1)
