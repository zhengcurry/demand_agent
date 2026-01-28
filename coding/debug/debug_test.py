"""
Debug test for Enhanced Code Skill
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from agents.requirement_analyst import RequirementAnalyst


def test_requirement_analyst():
    """Test RequirementAnalyst directly"""
    print_safe("="*80)
    print_safe("Debug Test: RequirementAnalyst")
    print_safe("="*80)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    print_safe(f"\n[OK] API key loaded: {api_key[:20]}...")

    # Test requirement
    requirement = """
    开发一个简单的计算器API:

    功能需求:
    1. 支持加法、减法、乘法、除法
    2. 输入验证
    3. 错误处理

    技术要求:
    - 后端: Python + FastAPI
    - 返回JSON格式
    """

    print_safe("\n[TEST] Initializing RequirementAnalyst...")
    try:
        analyst = RequirementAnalyst(api_key=api_key)
        print_safe("[OK] RequirementAnalyst initialized")
    except Exception as e:
        print_safe(f"[ERROR] Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

    print_safe("\n[TEST] Analyzing requirement...")
    try:
        result = analyst.analyze(requirement)

        print_safe(f"\n[RESULT] Success: {result.get('success')}")

        if result.get('success'):
            print_safe("[OK] Requirement analysis succeeded")
            print_safe(f"\nStructured requirement:")
            import json
            print_safe(json.dumps(result['requirement'], indent=2, ensure_ascii=False))
            return True
        else:
            print_safe(f"[ERROR] Requirement analysis failed")
            print_safe(f"Error: {result.get('error')}")
            if 'raw_response' in result:
                print_safe(f"\nRaw response:")
                print_safe(result['raw_response'])
            return False

    except Exception as e:
        print_safe(f"[ERROR] Exception during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_requirement_analyst()
    sys.exit(0 if success else 1)
