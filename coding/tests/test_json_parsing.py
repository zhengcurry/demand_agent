"""
Test JSON parsing improvements
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from utils import parse_json_response, clean_json_response

# Test cases
test_cases = [
    # Case 1: Clean JSON
    ('{"tasks": [{"id": "1"}]}', True),

    # Case 2: JSON with markdown
    ('```json\n{"tasks": [{"id": "1"}]}\n```', True),

    # Case 3: JSON with extra text before
    ('Here is the JSON:\n{"tasks": [{"id": "1"}]}', True),

    # Case 4: JSON with extra text after
    ('{"tasks": [{"id": "1"}]}\nThat\'s all!', True),

    # Case 5: JSON with both
    ('Here is the result:\n{"tasks": [{"id": "1"}]}\nDone!', True),

    # Case 6: Invalid JSON
    ('{"tasks": [{"id": "1"', False),
]

print("Testing JSON parsing improvements...")
print("="*70)

passed = 0
failed = 0

for i, (test_input, should_succeed) in enumerate(test_cases, 1):
    print(f"\nTest {i}: ", end="")
    try:
        result = parse_json_response(test_input)
        if should_succeed:
            print("[PASS] Successfully parsed")
            passed += 1
        else:
            print("[FAIL] Should have failed but succeeded")
            failed += 1
    except Exception as e:
        if not should_succeed:
            print(f"[PASS] Failed as expected: {type(e).__name__}")
            passed += 1
        else:
            print(f"[FAIL] Unexpected error: {e}")
            print(f"  Input: {test_input[:100]}...")
            failed += 1

print("\n" + "="*70)
print(f"Results: {passed} passed, {failed} failed")
print("="*70)

if failed == 0:
    print("[SUCCESS] All tests passed!")
    sys.exit(0)
else:
    print("[ERROR] Some tests failed")
    sys.exit(1)
