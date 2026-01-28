"""
Tests for Filesystem MCP Server
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from mcp_servers.filesystem_server import FilesystemMCPServer


class TestFilesystemMCPServer:
    """Test cases for Filesystem MCP Server"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests"""
        temp_path = tempfile.mkdtemp()
        yield temp_path
        shutil.rmtree(temp_path)

    @pytest.fixture
    def fs_server(self, temp_dir):
        """Create Filesystem MCP Server instance"""
        return FilesystemMCPServer(temp_dir)

    def test_fs_write_and_read(self, fs_server):
        """Test writing and reading files"""
        content = "Hello, World!"
        write_result = fs_server.fs_write("test.txt", content)
        assert write_result["success"] is True

        read_result = fs_server.fs_read("test.txt")
        assert read_result["success"] is True
        assert read_result["content"] == content

    def test_fs_create_dir(self, fs_server):
        """Test creating directories"""
        result = fs_server.fs_create_dir("test_dir/nested")
        assert result["success"] is True

    def test_fs_list(self, fs_server):
        """Test listing directory contents"""
        fs_server.fs_write("file1.txt", "content1")
        fs_server.fs_write("file2.txt", "content2")

        result = fs_server.fs_list("")
        assert result["success"] is True
        assert len(result["items"]) >= 2

    def test_fs_read_nonexistent(self, fs_server):
        """Test reading non-existent file"""
        result = fs_server.fs_read("nonexistent.txt")
        assert result["success"] is False

    def test_get_tools(self, fs_server):
        """Test getting available tools"""
        tools = fs_server.get_tools()
        assert len(tools) == 4
        tool_names = [t["name"] for t in tools]
        assert "fs_read" in tool_names
        assert "fs_write" in tool_names
        assert "fs_list" in tool_names
        assert "fs_create_dir" in tool_names

    def test_call_tool(self, fs_server):
        """Test calling tools via call_tool method"""
        result = fs_server.call_tool("fs_write", {"path": "test.txt", "content": "test"})
        assert result["success"] is True

        result = fs_server.call_tool("fs_read", {"path": "test.txt"})
        assert result["success"] is True
        assert result["content"] == "test"
