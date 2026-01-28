"""
Tests for CLI MCP Server
"""
import pytest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from mcp_servers.cli_server import CLIMCPServer


class TestCLIMCPServer:
    """Test cases for CLI MCP Server"""

    @pytest.fixture
    def cli_server(self):
        """Create CLI MCP Server instance"""
        return CLIMCPServer()

    def test_cli_execute_simple(self, cli_server):
        """Test executing simple command"""
        result = cli_server.cli_execute("echo test")
        assert result["success"] is True
        assert "test" in result["output"]

    def test_cli_execute_with_error(self, cli_server):
        """Test executing command that fails"""
        result = cli_server.cli_execute("nonexistent_command_xyz")
        assert result["success"] is False

    def test_get_tools(self, cli_server):
        """Test getting available tools"""
        tools = cli_server.get_tools()
        assert len(tools) == 3
        tool_names = [t["name"] for t in tools]
        assert "cli_execute" in tool_names
        assert "cli_run_tests" in tool_names
        assert "cli_build" in tool_names
