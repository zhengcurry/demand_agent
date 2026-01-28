"""
Simple test to verify the toolkit is working
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from env_config import check_environment


def test_environment():
    """Test if environment is configured"""
    print("Testing environment configuration...")
    if check_environment():
        print("[PASS] Environment configured correctly\n")
        return True
    else:
        print("[FAIL] Environment not configured\n")
        return False


def test_imports():
    """Test if all modules can be imported"""
    print("Testing module imports...")

    try:
        from mcp_servers.filesystem_server import FilesystemMCPServer
        print("  [OK] FilesystemMCPServer")

        from mcp_servers.git_server import GitMCPServer
        print("  [OK] GitMCPServer")

        from mcp_servers.cli_server import CLIMCPServer
        print("  [OK] CLIMCPServer")

        from mcp_servers.feishu_server import FeishuMCPServer
        print("  [OK] FeishuMCPServer")

        from agents.requirement_analyst import RequirementAnalyst
        print("  [OK] RequirementAnalyst")

        from agents.system_architect import SystemArchitect
        print("  [OK] SystemArchitect")

        from agents.api_designer import APIDesigner
        print("  [OK] APIDesigner")

        from agents.task_planner import TaskPlanner
        print("  [OK] TaskPlanner")

        from agents.code_generator import CodeGenerator
        print("  [OK] CodeGenerator")

        from agents.code_reviewer import CodeReviewer
        print("  [OK] CodeReviewer")

        from skills.code_skill import CodeSkill
        print("  [OK] CodeSkill")

        from skills.design_skill import DesignSkill
        print("  [OK] DesignSkill")

        from skills.review_skill import ReviewSkill
        print("  [OK] ReviewSkill")

        from skills.refactor_skill import RefactorSkill
        print("  [OK] RefactorSkill")

        print("\n[PASS] All modules imported successfully\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] Import error: {e}\n")
        return False


def test_mcp_servers():
    """Test MCP servers basic functionality"""
    print("Testing MCP servers...")

    try:
        from mcp_servers.filesystem_server import FilesystemMCPServer

        fs = FilesystemMCPServer()
        tools = fs.get_tools()
        assert len(tools) == 4, "FilesystemMCPServer should have 4 tools"
        print("  [OK] FilesystemMCPServer has 4 tools")

        from mcp_servers.git_server import GitMCPServer
        git = GitMCPServer()
        tools = git.get_tools()
        assert len(tools) == 5, "GitMCPServer should have 5 tools"
        print("  [OK] GitMCPServer has 5 tools")

        from mcp_servers.cli_server import CLIMCPServer
        cli = CLIMCPServer()
        tools = cli.get_tools()
        assert len(tools) == 3, "CLIMCPServer should have 3 tools"
        print("  [OK] CLIMCPServer has 3 tools")

        print("\n[PASS] MCP servers working correctly\n")
        return True

    except Exception as e:
        print(f"\n[FAIL] MCP server error: {e}\n")
        return False


def main():
    """Run all tests"""
    print("="*60)
    print("AI Development Toolkit - System Test")
    print("="*60)
    print()

    results = []

    # Test 1: Environment
    results.append(test_environment())

    # Test 2: Imports
    results.append(test_imports())

    # Test 3: MCP Servers
    results.append(test_mcp_servers())

    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n[SUCCESS] All tests passed! The toolkit is ready to use.")
        print("\nNext steps:")
        print("  1. Run an example: python examples/example_code_skill.py")
        print("  2. Use the CLI: python main.py code \"your requirement\"")
        print("  3. Read the docs: docs/USAGE.md")
        return 0
    else:
        print("\n[ERROR] Some tests failed. Please check the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
