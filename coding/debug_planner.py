"""
Debug test for TaskPlanner
"""
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from agents.task_planner import TaskPlanner


def test_task_planner():
    """Test TaskPlanner directly"""
    print_safe("="*80)
    print_safe("Debug Test: TaskPlanner")
    print_safe("="*80)

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    print_safe(f"\n[OK] API key loaded")

    # Simple test data
    requirement = {
        "title": "Simple Calculator API",
        "description": "A simple calculator API",
        "type": "backend",
        "features": [
            {"name": "Addition", "description": "Add numbers", "priority": "high"}
        ]
    }

    architecture = {
        "tech_stack": {
            "backend": ["Python", "FastAPI"]
        },
        "data_model": []
    }

    api_spec = {
        "paths": {
            "/add": {
                "post": {
                    "summary": "Add two numbers"
                }
            }
        }
    }

    print_safe("\n[TEST] Initializing TaskPlanner...")
    try:
        planner = TaskPlanner(api_key=api_key, model="claude-sonnet-4-5-20250929")
        print_safe("[OK] TaskPlanner initialized")
    except Exception as e:
        print_safe(f"[ERROR] Failed to initialize: {e}")
        import traceback
        traceback.print_exc()
        return False

    print_safe("\n[TEST] Planning tasks...")
    print_safe("This may take 30-60 seconds...")

    try:
        result = planner.plan(requirement, architecture, api_spec)

        print_safe(f"\n[RESULT] Success: {result.get('success')}")

        if result.get('success'):
            print_safe("[OK] Task planning succeeded")
            task_plan = result['task_plan']
            tasks = task_plan.get('tasks', [])
            print_safe(f"\nNumber of tasks: {len(tasks)}")

            if tasks:
                print_safe("\nFirst task:")
                print_safe(json.dumps(tasks[0], indent=2, ensure_ascii=False)[:500])

            return True
        else:
            print_safe(f"[ERROR] Task planning failed")
            print_safe(f"Error: {result.get('error')}")
            if 'raw_response' in result:
                print_safe(f"\nRaw response (first 1000 chars):")
                print_safe(result['raw_response'][:1000])
            return False

    except Exception as e:
        print_safe(f"[ERROR] Exception during planning: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_task_planner()
    sys.exit(0 if success else 1)
