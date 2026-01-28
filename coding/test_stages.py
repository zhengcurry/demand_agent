"""
Test each stage independently to find the issue
"""
import sys
from pathlib import Path
import json

sys.path.append(str(Path(__file__).parent))

from utils import print_safe
from env_config import get_api_key
from agents.requirement_analyst import RequirementAnalyst
from agents.system_architect import SystemArchitect
from agents.api_designer import APIDesigner
from agents.task_planner import TaskPlanner


def test_stage_by_stage():
    """Test each stage independently"""
    print_safe("="*80)
    print_safe("Stage-by-Stage Test")
    print_safe("="*80)

    api_key = get_api_key()
    if not api_key:
        print_safe("[ERROR] API key not configured")
        return False

    requirement_text = "开发一个加法API: 输入两个数字，返回它们的和。使用Python + FastAPI"

    # Stage 1: Requirement Analysis
    print_safe("\n[STAGE 1] Requirement Analysis...")
    analyst = RequirementAnalyst(api_key, model="claude-sonnet-4-5-20250929")
    req_result = analyst.analyze(requirement_text)

    if not req_result.get("success"):
        print_safe(f"[FAIL] Stage 1 failed: {req_result.get('error')}")
        return False

    print_safe("[OK] Stage 1 passed")
    requirement = req_result["requirement"]

    # Stage 2: Architecture Design
    print_safe("\n[STAGE 2] Architecture Design...")
    architect = SystemArchitect(api_key, model="claude-sonnet-4-5-20250929")
    arch_result = architect.design(requirement)

    if not arch_result.get("success"):
        print_safe(f"[FAIL] Stage 2 failed: {arch_result.get('error')}")
        return False

    print_safe("[OK] Stage 2 passed")
    architecture = arch_result["architecture"]

    # Stage 3: API Design
    print_safe("\n[STAGE 3] API Design...")
    api_designer = APIDesigner(api_key, model="claude-sonnet-4-5-20250929")
    api_result = api_designer.design(requirement, architecture)

    if not api_result.get("success"):
        print_safe(f"[FAIL] Stage 3 failed: {api_result.get('error')}")
        return False

    print_safe("[OK] Stage 3 passed")
    api_spec = api_result["api_spec"]

    # Stage 4: Task Planning
    print_safe("\n[STAGE 4] Task Planning...")
    print_safe("This may take 30-60 seconds...")

    planner = TaskPlanner(api_key, model="claude-sonnet-4-5-20250929")

    # Check input sizes
    req_size = len(json.dumps(requirement))
    arch_size = len(json.dumps(architecture))
    api_size = len(json.dumps(api_spec))
    print_safe(f"  Input sizes: req={req_size}, arch={arch_size}, api={api_size}")

    task_result = planner.plan(requirement, architecture, api_spec)

    if not task_result.get("success"):
        print_safe(f"[FAIL] Stage 4 failed: {task_result.get('error')}")
        if 'raw_response' in task_result:
            print_safe(f"Raw response (first 500 chars):")
            print_safe(task_result['raw_response'][:500])
        return False

    print_safe("[OK] Stage 4 passed")
    task_plan = task_result["task_plan"]
    print_safe(f"  Generated {len(task_plan.get('tasks', []))} tasks")

    print_safe("\n[SUCCESS] All stages passed!")
    return True


if __name__ == "__main__":
    success = test_stage_by_stage()
    sys.exit(0 if success else 1)
