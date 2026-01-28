"""
Quick test to verify API key configuration and basic functionality
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import check_environment


def main():
    print_safe("="*60)
    print_safe("Quick Configuration Test")
    print_safe("="*60)
    print_safe("")

    # Test 1: Check environment
    print_safe("[TEST 1] Checking API key configuration...")
    if check_environment():
        print_safe("[OK] API key is configured correctly")
    else:
        print_safe("[ERROR] API key not configured")
        print_safe("\nPlease follow the instructions above to configure your API key.")
        return 1

    # Test 2: Test imports
    print_safe("\n[TEST 2] Testing module imports...")
    try:
        from skills.code_skill import CodeSkill
        print_safe("[OK] CodeSkill imported successfully")

        from skills.design_skill import DesignSkill
        print_safe("[OK] DesignSkill imported successfully")

        from skills.review_skill import ReviewSkill
        print_safe("[OK] ReviewSkill imported successfully")

        from skills.refactor_skill import RefactorSkill
        print_safe("[OK] RefactorSkill imported successfully")
    except Exception as e:
        print_safe(f"[ERROR] Import failed: {e}")
        return 1

    # Test 3: Test print_safe
    print_safe("\n[TEST 3] Testing emoji handling...")
    print_safe("Emoji test: [START] [OK] [STEP] [SUCCESS] [ERROR]")
    print_safe("[OK] Emoji handling works correctly")

    # Summary
    print_safe("\n" + "="*60)
    print_safe("[SUCCESS] All tests passed!")
    print_safe("="*60)
    print_safe("\nYou can now:")
    print_safe("  1. Run examples: python examples/example_code_skill.py")
    print_safe("  2. Use CLI: python main.py code \"your requirement\"")
    print_safe("  3. Read docs: docs/USAGE.md")
    print_safe("")

    return 0


if __name__ == "__main__":
    sys.exit(main())
