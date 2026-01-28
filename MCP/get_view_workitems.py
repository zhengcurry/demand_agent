"""
飞书项目管理 - 获取视图工作项列表并筛选
支持根据项目、版本、业务线进行筛选
"""

import requests
import json
import sys
import io
from typing import List, Dict, Optional

# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 飞书MCP Server配置
MCP_SERVER_URL = "https://project.feishu.cn/mcp_server/v1"
MCP_KEY = "m-e468e82b-0313-445b-bf87-f0e3f9a5723f"
PROJECT_KEY = "662ef8e0b2b6c06ce1ef28db"
USER_KEY = "7371651783610875905"

# 完整的MCP Server URL
FULL_URL = f"{MCP_SERVER_URL}?mcpKey={MCP_KEY}&projectKey={PROJECT_KEY}&userKey={USER_KEY}"


def get_view_detail(
    view_id: str,
    fields: Optional[List[str]] = None,
    page_num: int = 1
) -> Optional[Dict]:
    """
    获取指定视图的工作项列表

    Args:
        view_id: 视图ID
        fields: 要查询的字段列表
        page_num: 页码（从1开始）

    Returns:
        视图详情数据
    """
    # 默认查询的字段
    if fields is None:
        fields = [
            "name",  # 名称
            "field_c13a6c",  # 关联项目
            "field_ab3f51",  # 规划版本
            "business",  # 所属业务线
            "work_item_status",  # 需求状态
            "priority",  # 优先级
            "owner",  # 创建者
            "current_status_operator",  # 当前负责人
            "work_item_id",  # 工作项ID
            "description",  # 描述
            "wiki",  # 需求文档URL
            "field_4972f5"  # 需求交付物清单
        ]

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "get_view_detail",
            "arguments": {
                "project_key": PROJECT_KEY,
                "view_id": view_id,
                "fields": fields,
                "page_num": page_num
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        print(f"正在获取视图工作项列表...")
        print(f"视图ID: {view_id}")
        print(f"项目Key: {PROJECT_KEY}")
        print(f"页码: {page_num}\n")

        response = requests.post(
            FULL_URL,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()

            if "result" in result and not result["result"].get("isError"):
                print("=" * 50)
                print("✅ 获取视图数据成功!")
                print("=" * 50)
                return result
            else:
                print("=" * 50)
                print("❌ 获取失败")
                print("=" * 50)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                return None
        else:
            print(f"❌ 请求失败: {response.text}")
            return None

    except Exception as e:
        print(f"发生错误: {e}")
        return None


def filter_workitems(
    workitems: List[Dict],
    project_filter: Optional[str] = None,
    version_filter: Optional[str] = None,
    business_filter: Optional[str] = None
) -> List[Dict]:
    """
    根据条件筛选工作项

    Args:
        workitems: 工作项列表
        project_filter: 项目筛选条件（field_c13a6c）
        version_filter: 版本筛选条件（field_ab3f51）
        business_filter: 业务线筛选条件（business）

    Returns:
        筛选后的工作项列表
    """
    filtered = workitems

    if project_filter:
        filtered = [
            item for item in filtered
            if project_filter.lower() in str(item.get("field_c13a6c", "")).lower()
        ]
        print(f"按项目筛选 (field_c13a6c 包含 '{project_filter}'): {len(filtered)} 项")

    if version_filter:
        filtered = [
            item for item in filtered
            if version_filter.lower() in str(item.get("field_ab3f51", "")).lower()
        ]
        print(f"按版本筛选 (field_ab3f51 包含 '{version_filter}'): {len(filtered)} 项")

    if business_filter:
        filtered = [
            item for item in filtered
            if business_filter.lower() in str(item.get("business", "")).lower()
        ]
        print(f"按业务线筛选 (business 包含 '{business_filter}'): {len(filtered)} 项")

    return filtered


def parse_view_response(result: Dict) -> List[Dict]:
    """
    解析视图响应数据，提取工作项列表

    Args:
        result: API响应结果

    Returns:
        工作项列表
    """
    workitems = []

    try:
        if "result" in result and "content" in result["result"]:
            content = result["result"]["content"]

            # 查找包含工作项数据的文本内容
            for item in content:
                if item.get("type") == "text":
                    text = item.get("text", "")

                    # 尝试解析Markdown表格
                    if "| 工作项 ID |" in text or "|---|" in text:
                        workitems = parse_markdown_table(text)
                        if workitems:
                            return workitems

                    # 尝试解析为JSON
                    try:
                        if text.strip().startswith("{") or text.strip().startswith("["):
                            data = json.loads(text)
                            if isinstance(data, list):
                                workitems.extend(data)
                            elif isinstance(data, dict) and "items" in data:
                                workitems.extend(data["items"])
                    except json.JSONDecodeError:
                        pass

        return workitems
    except Exception as e:
        print(f"解析响应数据时出错: {e}")
        return []


def parse_markdown_table(text: str) -> List[Dict]:
    """
    解析Markdown表格格式的工作项数据

    Args:
        text: Markdown表格文本

    Returns:
        工作项列表
    """
    workitems = []

    try:
        lines = text.split('\n')
        headers = []
        data_started = False

        for line in lines:
            line = line.strip()

            # 跳过空行
            if not line:
                continue

            # 查找表头
            if "| 工作项 ID |" in line:
                # 解析表头
                headers = [h.strip() for h in line.split('|') if h.strip()]
                continue

            # 跳过分隔线
            if line.startswith('|---') or line.startswith('| ---'):
                data_started = True
                continue

            # 解析数据行
            if data_started and line.startswith('|'):
                values = [v.strip() for v in line.split('|') if v != '']

                if len(values) == len(headers):
                    # 创建工作项字典
                    workitem = {}

                    for i, header in enumerate(headers):
                        value = values[i]

                        # 映射表头到字段key
                        if header == "工作项 ID":
                            workitem["work_item_id"] = value
                        elif header == "所属业务线":
                            workitem["business"] = value
                        elif header == "创建者":
                            workitem["owner"] = value
                        elif header == "名称":
                            workitem["name"] = value
                        elif header == "规划版本":
                            # 解析JSON格式的版本信息
                            if value and value != "null" and value.startswith("{"):
                                try:
                                    version_data = json.loads(value)
                                    workitem["field_ab3f51"] = version_data.get("工作项名称", value)
                                    workitem["field_ab3f51_id"] = version_data.get("工作项 ID", "")
                                except:
                                    workitem["field_ab3f51"] = value
                            else:
                                workitem["field_ab3f51"] = value
                        elif header == "优先级":
                            workitem["priority"] = value
                        elif header == "当前负责人":
                            workitem["current_status_operator"] = value
                        elif header == "关联项目":
                            # 解析JSON格式的项目信息
                            if value and value != "null" and value.startswith("{"):
                                try:
                                    project_data = json.loads(value)
                                    workitem["field_c13a6c"] = project_data.get("工作项名称", value)
                                    workitem["field_c13a6c_id"] = project_data.get("工作项 ID", "")
                                except:
                                    workitem["field_c13a6c"] = value
                            else:
                                workitem["field_c13a6c"] = value
                        elif header == "需求状态":
                            workitem["work_item_status"] = value
                        elif header == "描述":
                            workitem["description"] = value
                        elif header == "需求文档URL":
                            workitem["wiki"] = value
                        elif header == "需求交付物清单":
                            workitem["field_4972f5"] = value

                    workitems.append(workitem)

        return workitems
    except Exception as e:
        print(f"解析Markdown表格时出错: {e}")
        return []


def display_workitems(workitems: List[Dict]):
    """
    显示工作项列表

    Args:
        workitems: 工作项列表
    """
    if not workitems:
        print("\n没有找到工作项")
        return

    print(f"\n共找到 {len(workitems)} 个工作项:")
    print("=" * 100)

    for idx, item in enumerate(workitems, 1):
        print(f"\n{idx}. {item.get('name', '未命名')}")
        print(f"   工作项ID: {item.get('work_item_id', 'N/A')}")
        print(f"   关联项目 (field_c13a6c): {item.get('field_c13a6c', 'N/A')}")
        print(f"   规划版本 (field_ab3f51): {item.get('field_ab3f51', 'N/A')}")
        print(f"   所属业务线 (business): {item.get('business', 'N/A')}")
        print(f"   状态: {item.get('work_item_status', 'N/A')}")
        print(f"   优先级: {item.get('priority', 'N/A')}")
        print("-" * 100)


if __name__ == "__main__":
    # 配置参数
    VIEW_ID = "8SReqkNvg"  # 可修改的视图ID

    # 筛选条件（设置为None表示不筛选）
    PROJECT_FILTER = None  # 例如: "项目A"
    VERSION_FILTER = None  # 例如: "v1.0"
    BUSINESS_FILTER = None  # 例如: "YF-工业产品线"

    print("=" * 100)
    print("飞书项目管理 - 获取视图工作项列表")
    print("=" * 100)
    print(f"\n配置:")
    print(f"  视图ID: {VIEW_ID}")
    print(f"  项目筛选: {PROJECT_FILTER or '无'}")
    print(f"  版本筛选: {VERSION_FILTER or '无'}")
    print(f"  业务线筛选: {BUSINESS_FILTER or '无'}")
    print()

    # 获取视图数据
    result = get_view_detail(view_id=VIEW_ID, page_num=1)

    if result:
        # 打印原始响应（用于调试）
        print("\n原始响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        # 解析工作项列表
        workitems = parse_view_response(result)

        if workitems:
            # 应用筛选条件
            if PROJECT_FILTER or VERSION_FILTER or BUSINESS_FILTER:
                print("\n" + "=" * 100)
                print("应用筛选条件:")
                print("=" * 100)
                workitems = filter_workitems(
                    workitems,
                    project_filter=PROJECT_FILTER,
                    version_filter=VERSION_FILTER,
                    business_filter=BUSINESS_FILTER
                )

            # 显示结果
            display_workitems(workitems)
        else:
            print("\n⚠️ 未能解析出工作项数据，请检查响应格式")
