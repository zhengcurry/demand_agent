"""
Tests for Git MCP Server
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from mcp_servers.git_server import GitMCPServer


class TestGitMCPServer:
    """Test cases for Git MCP Server"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    @pytest.fixture
    def git_server(self, temp_dir):
        """Create Git MCP Server instance"""
        return GitMCPServer(temp_dir)

    def test_git_init(self, git_server):
        """Test initializing Git repository"""
        result = git_server.git_init()
        assert result["success"] is True

    def test_git_status(self, git_server):
        """Test Git status"""
        git_server.git_init()
        result = git_server.git_status()
        assert result["success"] is True

    def test_get_tools(self, git_server):
        """Test getting available tools"""
        tools = git_server.get_tools()
        assert len(tools) == 5
        tool_names = [t["name"] for t in tools]
        assert "git_init" in tool_names
        assert "git_add" in tool_names
        assert "git_commit" in tool_names
        assert "git_diff" in tool_names
        assert "git_status" in tool_names
