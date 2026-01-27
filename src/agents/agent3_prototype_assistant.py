import os
import json
from typing import Annotated
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
import sys
# 添加src目录到Python路径
workspace_path = os.getenv("WORKSPACE_PATH", os.getcwd())
sys.path.insert(0, os.path.join(workspace_path, "src"))
from storage.memory.memory_saver import get_memory_saver

LLM_CONFIG = "config/agent3_config.json"

# 原型设计需要参考PRD内容，需要较长的对话历史，设置为40轮（80条消息）
MAX_MESSAGES = 80

def _windowed_messages(old, new):
    """滑动窗口: 只保留最近 MAX_MESSAGES 条消息"""
    return add_messages(old, new)[-MAX_MESSAGES:]  # type: ignore

class AgentState(MessagesState):
    messages: Annotated[list[AnyMessage], _windowed_messages]

def build_agent(ctx=None):
    workspace_path = os.getenv("WORKSPACE_PATH", os.getcwd())
    config_path = os.path.join(workspace_path, LLM_CONFIG)

    with open(config_path, 'r', encoding='utf-8') as f:
        cfg = json.load(f)

    # 从环境变量读取 Anthropic API Key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    # 检查是否启用 extended thinking 模式
    thinking_enabled = cfg['config'].get('thinking', 'disabled') == 'enabled'

    # 构建 ChatAnthropic 实例
    llm_kwargs = {
        "model": cfg['config'].get("model", "claude-sonnet-4-5"),
        "api_key": api_key,
        "temperature": cfg['config'].get('temperature', 0.7),
        "max_tokens": cfg['config'].get('max_completion_tokens', 8000),
        "timeout": cfg['config'].get('timeout', 600),
    }

    # 如果启用 thinking 模式，使用支持 extended thinking 的模型
    if thinking_enabled:
        llm_kwargs["model_kwargs"] = {
            "thinking": {
                "type": "enabled",
                "budget_tokens": 10000
            }
        }

    llm = ChatAnthropic(**llm_kwargs)

    return create_agent(
        model=llm,
        system_prompt=cfg.get("sp"),
        tools=[],
        checkpointer=get_memory_saver(),
        state_schema=AgentState,
    )
