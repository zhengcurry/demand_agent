"""
飞书项目管理 - 创建工作项脚本 Final
"""

import requests
import json
import sys
import io

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 飞书MCP Server配置
MCP_SERVER_URL = "https://project.feishu.cn/mcp_server/v1"
MCP_KEY = "m-e468e82b-0313-445b-bf87-f0e3f9a5723f"
PROJECT_KEY = "662ef8e0b2b6c06ce1ef28db"
USER_KEY = "7371651783610875905"

# 完整的MCP Server URL
FULL_URL = f"{MCP_SERVER_URL}?mcpKey={MCP_KEY}&projectKey={PROJECT_KEY}&userKey={USER_KEY}"


def create_workitem(work_item_type: str, story_name: str):
    """
    创建工作项

    Args:
        work_item_type: 工作项类型
        story_name: 工作项名称
    """
    # 只使用name字段
    fields = [
        {
            "field_key": "name",
            "field_value": story_name
        }
    ]

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "create_workitem",
            "arguments": {
                "project_key": PROJECT_KEY,
                "work_item_type": work_item_type,
                "fields": fields
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"正在创建工作项...")
        print(f"工作项类型: {work_item_type}")
        print(f"工作项名称: {story_name}")
        print(f"项目Key: {PROJECT_KEY}\n")

        response = requests.post(
            FULL_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"响应状态码: {response.status_code}")

        if response.status_code == 200:
            result = response.json()

            # 检查是否有错误
            if "result" in result:
                if result["result"].get("isError"):
                    print("=" * 50)
                    print("❌ 创建失败")
                    print("=" * 50)
                else:
                    print("=" * 50)
                    print("✅ 工作项创建成功!")
                    print("=" * 50)

                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print(json.dumps(result, indent=2, ensure_ascii=False))

            return result
        else:
            print(f"❌ 创建失败: {response.text}")
            return None

    except Exception as e:
        print(f"发生错误: {e}")
        return None


if __name__ == "__main__":
    print("创建工作项")
    print("=" * 50)
    create_workitem(
        work_item_type="story",
        story_name="claude-2026年1月27日2次需求测试"
    )
