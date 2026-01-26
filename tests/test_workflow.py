"""
三层AI Agent工作流测试脚本
测试三个Agent的协同工作
"""

import asyncio
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.agents.workflow_coordinator import run_requirement_workflow


async def test_full_workflow():
    """测试完整的三层工作流"""
    
    print("\n" + "#"*80)
    print("# 三层AI Agent协同工作流测试")
    print("#"*80)
    
    # 测试用例：简单的功能需求
    user_input = """
    我想开发一个用户登录功能，支持账号密码登录和手机验证码登录两种方式。
    """
    
    print(f"\n【用户输入】\n{user_input}")
    
    # 执行完整工作流
    print("\n" + "="*80)
    print("开始执行完整工作流...")
    print("="*80)
    
    results = await run_requirement_workflow(
        user_input=user_input,
        mode="full",
        thread_id="test_session_1"
    )
    
    # 输出结果
    print("\n" + "="*80)
    print("【工作流执行结果】")
    print("="*80)
    
    # 阶段1结果
    print("\n" + "-"*80)
    print("阶段1：需求澄清助手")
    print("-"*80)
    print("\n需求摘要：")
    print(results["stage1"]["requirement_summary"])
    
    # 阶段2结果
    print("\n" + "-"*80)
    print("阶段2：PRD结构化生成器")
    print("-"*80)
    print("\nPRD文档（前500字符）：")
    print(results["stage2"]["prd_document"][:500] + "...")
    
    # 阶段3结果
    print("\n" + "-"*80)
    print("阶段3：原型与交互辅助")
    print("-"*80)
    print("\n设计文档（前500字符）：")
    print(results["stage3"]["design_document"][:500] + "...")
    
    # 统计信息
    print("\n" + "="*80)
    print("【统计信息】")
    print("="*80)
    print(f"阶段1对话轮次: {len(results['stage1']['messages'])}")
    print(f"阶段2对话轮次: {len(results['stage2']['messages'])}")
    print(f"阶段3对话轮次: {len(results['stage3']['messages'])}")
    
    print("\n✅ 测试完成！\n")


async def test_stage1_only():
    """仅测试阶段1"""
    
    print("\n" + "#"*80)
    print("# 测试阶段1：需求澄清助手")
    print("#"*80)
    
    user_input = "我想做一个活动页面，提升用户注册转化率"
    
    print(f"\n用户输入: {user_input}")
    
    result = await run_requirement_workflow(
        user_input=user_input,
        mode="stage1",
        thread_id="test_session_2"
    )
    
    print("\n需求摘要:")
    print(result["requirement_summary"])
    
    print("\n✅ 阶段1测试完成！\n")


async def test_stage2_only():
    """仅测试阶段2"""
    
    print("\n" + "#"*80)
    print("# 测试阶段2：PRD生成")
    print("#"*80)
    
    # 使用固定的需求摘要
    requirement_summary = """
    # 需求摘要

    ## 1. 需求类型
    功能型

    ## 2. 核心目标
    开发用户登录功能，支持账号密码和手机验证码两种登录方式

    ## 3. 目标用户
    所有需要登录系统的用户

    ## 4. 主要场景
    - 场景1：用户使用账号密码登录
    - 场景2：用户使用手机验证码登录

    ## 5. 关键指标
    - 登录成功率 > 95%
    - 登录响应时间 < 2秒

    ## 6. 功能要点
    - 账号密码登录
    - 手机验证码登录
    - 登录方式切换
    - 记住密码功能

    ## 7. 约束条件
    - 需要保障登录安全
    - 需要支持多端

    ## 8. 期望时间
    2周内完成

    ## 9. 需要进一步确认的事项
    - 是否需要支持第三方登录
    """
    
    print("\n需求摘要:")
    print(requirement_summary[:200] + "...")
    
    result = await run_requirement_workflow(
        user_input="",  # stage2不需要user_input
        mode="stage2",
        thread_id="test_session_3",
        input_data=requirement_summary
    )
    
    print("\nPRD文档（前800字符）:")
    print(result["prd_document"][:800] + "...")
    
    print("\n✅ 阶段2测试完成！\n")


async def test_stage3_only():
    """仅测试阶段3"""
    
    print("\n" + "#"*80)
    print("# 测试阶段3：原型辅助")
    print("#"*80)
    
    # 使用固定的PRD文档片段
    prd_document = """
    # PRD文档：用户登录功能

    ## 一、项目概述
    ### 1.1 需求背景
    为满足用户多样化的登录需求，需提供账号密码登录和手机验证码登录两种方式。

    ### 1.2 项目目标
    1. 实现两种登录方式的切换与验证逻辑
    2. 保障登录数据安全
    3. 优化登录交互体验

    ## 二、用户分析
    ### 2.1 目标用户
    所有需要登录系统的用户

    ### 2.2 使用场景
    - 场景1：账号密码登录
      用户行为：输入账号密码，点击登录
      系统响应：验证成功后跳转首页
      用户价值：快速完成登录

    - 场景2：手机验证码登录
      用户行为：输入手机号，获取验证码，输入验证码，点击登录
      系统响应：验证成功后跳转首页
      用户价值：无需记忆密码

    ## 三、功能需求
    ### 3.1 功能清单
    #### P0级功能
    - 功能1：账号密码登录
      功能描述：支持账号密码登录
      业务规则：账号必须已注册，密码需正确

    - 功能2：手机验证码登录
      功能描述：支持手机验证码登录
      业务规则：手机号必须已注册，验证码需有效

    - 功能3：登录方式切换
      功能描述：在两种登录方式间切换
    """
    
    print("\nPRD文档（前500字符）:")
    print(prd_document[:500] + "...")
    
    result = await run_requirement_workflow(
        user_input="",  # stage3不需要user_input
        mode="stage3",
        thread_id="test_session_4",
        input_data=prd_document
    )
    
    print("\n设计文档（前800字符）:")
    print(result["design_document"][:800] + "...")
    
    print("\n✅ 阶段3测试完成！\n")


async def main():
    """主测试函数"""
    
    print("\n" + "="*80)
    print("  三层AI Agent协同工作流 - 测试套件")
    print("="*80)
    
    # 可选：选择测试类型
    test_type = input("\n请选择测试类型：\n1. 完整工作流测试（推荐）\n2. 仅测试阶段1\n3. 仅测试阶段2\n4. 仅测试阶段3\n5. 全部测试\n\n请输入选项（1-5）：")
    
    if test_type == "1":
        await test_full_workflow()
    elif test_type == "2":
        await test_stage1_only()
    elif test_type == "3":
        await test_stage2_only()
    elif test_type == "4":
        await test_stage3_only()
    elif test_type == "5":
        print("\n执行全部测试...")
        await test_full_workflow()
        await test_stage1_only()
        await test_stage2_only()
        await test_stage3_only()
        print("\n" + "="*80)
        print("  全部测试完成！")
        print("="*80)
    else:
        print("\n无效选项，执行完整工作流测试...")
        await test_full_workflow()


if __name__ == "__main__":
    asyncio.run(main())
