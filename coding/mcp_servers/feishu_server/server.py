"""
Feishu MCP Server
Provides Feishu document operations as MCP tools.
"""
import requests
from typing import Dict, Any, List


class FeishuMCPServer:
    """MCP Server for Feishu operations"""

    def __init__(self, app_id: str = None, app_secret: str = None):
        """
        Initialize Feishu MCP Server

        Args:
            app_id: Feishu app ID
            app_secret: Feishu app secret
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None

    def get_tools(self) -> List[Dict[str, Any]]:
        """Return list of available tools"""
        return [
            {
                "name": "feishu_read_doc",
                "description": "Read content from a Feishu document",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string", "description": "Feishu document URL or document ID"}
                    },
                    "required": ["url"]
                }
            },
            {
                "name": "feishu_get_token",
                "description": "Get Feishu access token",
                "input_schema": {"type": "object", "properties": {}}
            }
        ]

    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        try:
            if tool_name == "feishu_read_doc":
                return self.feishu_read_doc(arguments["url"])
            elif tool_name == "feishu_get_token":
                return self.feishu_get_token()
            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def feishu_get_token(self) -> Dict[str, Any]:
        """Get Feishu access token"""
        if not self.app_id or not self.app_secret:
            return {"success": False, "error": "App ID and App Secret not configured"}

        try:
            url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
            payload = {
                "app_id": self.app_id,
                "app_secret": self.app_secret
            }
            response = requests.post(url, json=payload)
            data = response.json()

            if data.get("code") == 0:
                self.access_token = data.get("tenant_access_token")
                return {"success": True, "token": self.access_token}
            else:
                return {"success": False, "error": data.get("msg", "Failed to get token")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def feishu_read_doc(self, url: str) -> Dict[str, Any]:
        """Read Feishu document content"""
        if not self.access_token:
            token_result = self.feishu_get_token()
            if not token_result.get("success"):
                return token_result

        try:
            doc_id = self._extract_doc_id(url)
            if not doc_id:
                return {"success": False, "error": "Invalid Feishu document URL"}

            api_url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/raw_content"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = requests.get(api_url, headers=headers)
            data = response.json()

            if data.get("code") == 0:
                content = data.get("data", {}).get("content", "")
                return {"success": True, "content": content, "doc_id": doc_id}
            else:
                return {"success": False, "error": data.get("msg", "Failed to read document")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _extract_doc_id(self, url: str) -> str:
        """Extract document ID from Feishu URL"""
        if "feishu.cn" in url or "larksuite.com" in url:
            parts = url.split("/")
            for i, part in enumerate(parts):
                if part in ["docs", "docx", "wiki"]:
                    if i + 1 < len(parts):
                        return parts[i + 1].split("?")[0]
        return url
