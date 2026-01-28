"""
Simplified test - Skip design review to test full workflow
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from skills.code_skill import CodeSkill


def test_original_code_skill():
    """Test original CodeSkill (without enhanced features)"""
    print_safe("="*80)
    print_safe("Test: Original Code Skill (Simpler Workflow)")
    print_safe("="*80)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    # Simple requirement
    requirement = """
    开发一个简单的计算器API:

    功能需求:
    1. 支持加法运算
    2. 输入验证

    技术要求:
    - 后端: Python + FastAPI
    - 返回JSON格式
    """

    print_safe("\n[TEST] Initializing CodeSkill...")
    try:
        skill = CodeSkill(
            api_key=api_key,
            project_path="./test_simple_calc"
        )
        print_safe("[OK] CodeSkill initialized\n")
    except Exception as e:
        print_safe(f"[ERROR] Failed to initialize: {e}")
        return False

    print_safe("[TEST] Running original workflow...")
    print_safe("This uses the simpler, proven workflow.\n")

    try:
        result = skill.execute(
            requirement=requirement,
            mode="auto"
        )

        if result["success"]:
            print_safe("\n" + "="*80)
            print_safe("[SUCCESS] Original Code Skill Test Passed!")
            print_safe("="*80)
            print_safe(f"\nGenerated Files: {len(result.get('results', {}).get('generated_files', []))}")
            print_safe(f"Project Path: ./test_simple_calc/")
            return True
        else:
            print_safe(f"\n[ERROR] Workflow failed: {result.get('error')}")
            return False

    except Exception as e:
        print_safe(f"\n[ERROR] Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_original_code_skill()
    sys.exit(0 if success else 1)
