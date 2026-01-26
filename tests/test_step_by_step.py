"""
分步测试三个Agent
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


async def test_agent1():
    """测试Agent 1"""
    print("\n" + "="*80)
    print("测试 Agent 1：需求澄清助手")
    print("="*80)
    
    user_input = "我要开发一个用户登录功能，支持账号密码登录和手机验证码登录"
    print(f"\n用户输入: {user_input}\n")
    
    agent1 = build_agent1()
    config = {"configurable": {"thread_id": "test_agent1"}}
    
    # 第一次对话
    response = await agent1.ainvoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )
    
    print("Agent 1 响应（第一次对话）:")
    print(response["messages"][-1].content[:500] + "...\n")
    
    # 要求生成摘要
    summary_prompt = "请根据我们的对话，生成最终的需求摘要。"
    final_response = await agent1.ainvoke(
        {"messages": response["messages"] + [HumanMessage(content=summary_prompt)]},
        config=config
    )
    
    print("\n最终需求摘要:")
    print(final_response["messages"][-1].content)
    
    return final_response["messages"][-1].content


async def test_agent2(requirement_summary):
    """测试Agent 2"""
    print("\n" + "="*80)
    print("测试 Agent 2：PRD生成器")
    print("="*80)
    
    print("\n需求摘要（前300字符）:")
    print(requirement_summary[:300] + "...\n")
    
    agent2 = build_agent2()
    config = {"configurable": {"thread_id": "test_agent2"}}
    
    prd_input = f"请根据以下需求摘要生成PRD文档：\n\n{requirement_summary}"
    
    response = await agent2.ainvoke(
        {"messages": [HumanMessage(content=prd_input)]},
        config=config
    )
    
    print("PRD文档（前1000字符）:")
    print(response["messages"][-1].content[:1000] + "...\n")
    
    print("PRD生成成功！\n")
    
    return response["messages"][-1].content


async def test_agent3(prd_document):
    """测试Agent 3"""
    print("\n" + "="*80)
    print("测试 Agent 3：原型辅助")
    print("="*80)
    
    print("\nPRD文档（前500字符）:")
    print(prd_document[:500] + "...\n")
    
    agent3 = build_agent3()
    config = {"configurable": {"thread_id": "test_agent3"}}
    
    # 只传递PRD的前1500字符，避免token超限
    design_input = f"请根据以下PRD文档生成界面设计方案：\n\n{prd_document[:1500]}"
    
    print("正在生成设计文档...（这可能需要一些时间）\n")
    
    try:
        # 设置超时时间
        response = await asyncio.wait_for(
            agent3.ainvoke(
                {"messages": [HumanMessage(content=design_input)]},
                config=config
            ),
            timeout=120.0  # 2分钟超时
        )
        
        print("设计文档（前1000字符）:")
        print(response["messages"][-1].content[:1000] + "...\n")
        
        print("设计文档生成成功！\n")
        
        return response["messages"][-1].content
        
    except asyncio.TimeoutError:
        print("❌ Agent 3 响应超时，可能需要较长时间处理。\n")
        return ""


async def main():
    """主测试函数"""
    
    print("\n" + "#"*80)
    print("# 三层AI Agent - 分步测试")
    print("#"*80)
    
    try:
        # 测试Agent 1
        requirement_summary = await test_agent1()
        
        input("\n按回车键继续测试Agent 2...")
        
        # 测试Agent 2
        prd_document = await test_agent2(requirement_summary)
        
        input("\n按回车键继续测试Agent 3...")
        
        # 测试Agent 3
        design_document = await test_agent3(prd_document)
        
        print("\n" + "="*80)
        print("测试总结")
        print("="*80)
        print("\n✅ Agent 1 (需求澄清助手) - 测试通过")
        print("✅ Agent 2 (PRD生成器) - 测试通过")
        if design_document:
            print("✅ Agent 3 (原型辅助) - 测试通过")
        else:
            print("⚠️  Agent 3 (原型辅助) - 响应超时")
        
        print("\n" + "#"*80)
        print("# 测试完成")
        print("#"*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
