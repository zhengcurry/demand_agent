"""
Simple debug test for Enhanced Code Skill
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key

print_safe("Step 1: Checking API key...")
api_key = get_api_key()
if not api_key:
    print_safe("[ERROR] API key not configured")
    sys.exit(1)
print_safe(f"[OK] API key found (length: {len(api_key)})")

print_safe("\nStep 2: Importing EnhancedCodeSkill...")
try:
    from skills.enhanced_code_skill import EnhancedCodeSkill
    print_safe("[OK] EnhancedCodeSkill imported")
except Exception as e:
    print_safe(f"[ERROR] Failed to import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print_safe("\nStep 3: Initializing EnhancedCodeSkill...")
try:
    skill = EnhancedCodeSkill(
        api_key=api_key,
        project_path="./test_calculator_api"
    )
    print_safe("[OK] EnhancedCodeSkill initialized")
except Exception as e:
    print_safe(f"[ERROR] Failed to initialize: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print_safe("\nStep 4: Testing requirement analyst...")
try:
    from agents.requirement_analyst import RequirementAnalyst
    analyst = RequirementAnalyst(api_key, model="claude-sonnet-4-5-20250929")
    print_safe("[OK] RequirementAnalyst created")

    # Try a simple analysis
    print_safe("\nStep 5: Running simple requirement analysis...")
    result = analyst.analyze("Create a simple calculator with add and subtract functions")
    print_safe(f"[OK] Analysis result: {result.get('success', False)}")
    if result.get('success'):
        print_safe(f"Requirement type: {result['requirement'].get('type', 'unknown')}")
    else:
        print_safe(f"Error: {result.get('error', 'unknown')}")
except Exception as e:
    print_safe(f"[ERROR] Failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print_safe("\n[SUCCESS] All basic tests passed!")
