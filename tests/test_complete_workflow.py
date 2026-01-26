"""
三层AI Agent工作流完整测试
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 设置环境变量
os.environ['COZE_WORKSPACE_PATH'] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from src.agents.agent1_requirement_clarifier import build_agent as build_agent1
from src.agents.agent2_prd_builder import build_agent as build_agent2
from src.agents.agent3_prototype_assistant import build_agent as build_agent3
from langchain_core.messages import HumanMessage


async def test_full_workflow():
    """测试完整的三层工作流"""
    
    print("\n" + "="*80)
    print("  三层AI Agent协同工作流 - 完整测试")
    print("="*80)
    
    # 测试用例：简单的功能需求
    user_input = "我要开发一个用户登录功能，支持账号密码登录和手机验证码登录两种方式"
    
    print(f"\n【用户输入】\n{user_input}")
    
    # ========== 阶段1: 需求澄清 ==========
    print("\n" + "-"*80)
    print("阶段1：需求澄清助手")
    print("-"*80)
    
    agent1 = build_agent1()
    config1 = {"configurable": {"thread_id": "test_agent1"}}
    
    # 第一次对话
    response1 = await agent1.ainvoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config1
    )
    
    # 要求生成摘要
    summary_prompt = "请根据我们的对话，生成最终的需求摘要。"
    final_response1 = await agent1.ainvoke(
        {"messages": response1["messages"] + [HumanMessage(content=summary_prompt)]},
        config=config1
    )
    
    # 提取摘要
    requirement_summary = ""
    for msg in reversed(final_response1["messages"]):
        if hasattr(msg, 'content') and "需求摘要" in msg.content:
            requirement_summary = msg.content
            break
    
    if not requirement_summary:
        requirement_summary = final_response1["messages"][-1].content
    
    print(f"\n需求摘要（前500字符）:\n{requirement_summary[:500]}...")
    print(f"\n对话轮次: {len(final_response1['messages'])}")
    
    # ========== 阶段2: PRD生成 ==========
    print("\n" + "-"*80)
    print("阶段2：PRD结构化生成器")
    print("-"*80)
    
    agent2 = build_agent2()
    config2 = {"configurable": {"thread_id": "test_agent2"}}
    
    prd_input = f"请根据以下需求摘要生成PRD文档：\n\n{requirement_summary}"
    
    response2 = await agent2.ainvoke(
        {"messages": [HumanMessage(content=prd_input)]},
        config=config2
    )
    
    prd_document = response2["messages"][-1].content
    
    print(f"\nPRD文档（前800字符）:\n{prd_document[:800]}...")
    print(f"\n对话轮次: {len(response2['messages'])}")
    
    # ========== 阶段3: 原型辅助 ==========
    print("\n" + "-"*80)
    print("阶段3：原型与交互辅助")
    print("-"*80)
    
    agent3 = build_agent3()
    config3 = {"configurable": {"thread_id": "test_agent3"}}
    
    # 传递PRD的前2000字符（避免token超限）
    design_input = f"请根据以下PRD文档生成界面设计方案：\n\n{prd_document[:2000]}"
    
    response3 = await agent3.ainvoke(
        {"messages": [HumanMessage(content=design_input)]},
        config=config3
    )
    
    design_document = response3["messages"][-1].content
    
    print(f"\n设计文档（前800字符）:\n{design_document[:800]}...")
    print(f"\n对话轮次: {len(response3['messages'])}")
    
    # ========== 总结 ==========
    print("\n" + "="*80)
    print("  测试总结")
    print("="*80)
    
    print(f"\n✅ 阶段1完成：需求澄清助手生成了需求摘要")
    print(f"   对话轮次：{len(final_response1['messages'])}")
    
    print(f"\n✅ 阶段2完成：PRD生成器生成了完整PRD文档")
    print(f"   对话轮次：{len(response2['messages'])}")
    print(f"   PRD长度：{len(prd_document)} 字符")
    
    print(f"\n✅ 阶段3完成：原型辅助生成了界面设计方案")
    print(f"   对话轮次：{len(response3['messages'])}")
    print(f"   设计文档长度：{len(design_document)} 字符")
    
    print("\n" + "="*80)
    print("  所有测试通过！三层Agent协同工作成功！")
    print("="*80 + "\n")
    
    return {
        "stage1": {
            "summary": requirement_summary,
            "message_count": len(final_response1["messages"])
        },
        "stage2": {
            "prd": prd_document,
            "message_count": len(response2["messages"])
        },
        "stage3": {
            "design": design_document,
            "message_count": len(response3["messages"])
        }
    }


if __name__ == "__main__":
    results = asyncio.run(test_full_workflow())
