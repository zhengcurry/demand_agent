"""
Debug test for SystemArchitect
"""
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from agents.system_architect import SystemArchitect


def test_system_architect():
    """Test SystemArchitect directly"""
    print_safe("="*80)
    print_safe("Debug Test: SystemArchitect")
    print_safe("="*80)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    print_safe(f"\n[OK] API key loaded")

    # Test requirement (simple structure)
    requirement = {
        "title": "Simple Calculator API",
        "description": "A simple calculator API",
        "type": "backend",
        "features": [
            {"name": "Addition", "description": "Add numbers", "priority": "high"}
        ]
    }

    print_safe("\n[TEST] Initializing SystemArchitect...")
    try:
        # Try with Sonnet first (Opus might not be available)
        architect = SystemArchitect(api_key=api_key, model="claude-sonnet-4-5-20250929")
        print_safe("[OK] SystemArchitect initialized with Sonnet")
    except Exception as e:
        print_safe(f"[ERROR] Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

    print_safe("\n[TEST] Designing architecture...")
    try:
        result = architect.design(requirement)

        print_safe(f"\n[RESULT] Success: {result.get('success')}")

        if result.get('success'):
            print_safe("[OK] Architecture design succeeded")
            print_safe(f"\nArchitecture:")
            print_safe(json.dumps(result['architecture'], indent=2, ensure_ascii=False)[:500])
            return True
        else:
            print_safe(f"[ERROR] Architecture design failed")
            print_safe(f"Error: {result.get('error')}")
            if 'raw_response' in result:
                print_safe(f"\nRaw response:")
                print_safe(result['raw_response'][:500])
            return False

    except Exception as e:
        print_safe(f"[ERROR] Exception during design: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_system_architect()
    sys.exit(0 if success else 1)
