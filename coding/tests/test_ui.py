"""
Quick test for UI app
Verifies that the UI can be imported and basic components work
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

print("Testing UI components...")

# Test imports
try:
    import streamlit as st
    print("[OK] Streamlit imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import Streamlit: {e}")
    sys.exit(1)

try:
    from env_config import get_api_key
    print("[OK] env_config imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import env_config: {e}")
    sys.exit(1)

try:
    from skills.enhanced_code_skill import EnhancedCodeSkill
    print("[OK] EnhancedCodeSkill imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import EnhancedCodeSkill: {e}")
    sys.exit(1)

# Test API key
api_key = get_api_key()
if api_key:
    print(f"[OK] API key found (length: {len(api_key)})")
else:
    print("[WARNING] API key not found (this is OK for testing)")

print("\n" + "="*70)
print("[SUCCESS] All UI components are ready!")
print("="*70)
print("\nTo start the UI, run:")
print("  python run_ui.py")
print("\nOr directly:")
print("  streamlit run ui_app.py")
print("="*70)
