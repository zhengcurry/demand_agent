"""
三层AI Agent协同工作流协调器

负责协调三个Agent的执行顺序、数据传递和结果整合。
支持完整流程、单步执行和选择性执行等多种模式。
"""

import asyncio
from typing import Dict, Optional, List, Any
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, AnyMessage

# 使用相对导入，避免模块路径问题
from .agent1_requirement_clarifier import build_agent as build_agent1
from .agent2_prd_builder import build_agent as build_agent2
from .agent3_prototype_assistant import build_agent as build_agent3


class WorkflowCoordinator:
    """三层Agent工作流协调器"""
    
    def __init__(self):
        """初始化协调器"""
        self.agents = {}
        self.session_states = {}
        self.results = {}
    
    def _init_agents(self):
        """初始化所有Agent"""
        if 'agent1' not in self.agents:
            self.agents['agent1'] = build_agent1()
        if 'agent2' not in self.agents:
            self.agents['agent2'] = build_agent2()
        if 'agent3' not in self.agents:
            self.agents['agent3'] = build_agent3()
    
    def _extract_summary_from_agent1(self, messages: List[AnyMessage]) -> str:
        """
        从Agent1的对话中提取需求摘要
        
        Args:
            messages: Agent1的对话历史
            
        Returns:
            提取的需求摘要文本
        """
        # 查找最后一条包含"需求摘要"或类似标识的消息
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and "需求摘要" in msg.content:
                # 提取摘要部分
                content = msg.content
                if "需求摘要" in content:
                    return content
        
        # 如果没有找到明确的摘要，返回最后一条AI消息
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                return msg.content
        
        return ""
    
    def _extract_prd_from_agent2(self, messages: List[AnyMessage]) -> str:
        """
        从Agent2的对话中提取PRD文档
        
        Args:
            messages: Agent2的对话历史
            
        Returns:
            提取的PRD文档文本
        """
        # 返回最后一条AI消息（通常是PRD文档）
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                return msg.content
        
        return ""
    
    def _extract_design_from_agent3(self, messages: List[AnyMessage]) -> str:
        """
        从Agent3的对话中提取设计文档
        
        Args:
            messages: Agent3的对话历史
            
        Returns:
            提取的设计文档文本
        """
        # 返回最后一条AI消息（通常是设计文档）
        for msg in reversed(messages):
            if isinstance(msg, AIMessage):
                return msg.content
        
        return ""
    
    async def run_full_workflow(
        self,
        user_input: str,
        thread_id: str = "default",
        interactive: bool = False
    ) -> Dict[str, Any]:
        """
        执行完整的三层工作流
        
        Args:
            user_input: 用户的初始需求输入
            thread_id: 会话ID，用于保持对话历史
            interactive: 是否交互模式（true时会在每个阶段暂停等待确认）
            
        Returns:
            包含三个阶段结果的字典
        """
        self._init_agents()
        
        results = {
            "stage1": {
                "requirement_summary": "",
                "messages": []
            },
            "stage2": {
                "prd_document": "",
                "messages": []
            },
            "stage3": {
                "design_document": "",
                "messages": []
            }
        }
        
        # ========== 阶段1: 需求澄清 ==========
        print("\n" + "="*60)
        print("【阶段1：需求澄清助手】")
        print("="*60)
        
        config1 = {"configurable": {"thread_id": f"{thread_id}_agent1"}}
        
        # 启动Agent1对话
        response1 = await self.agents['agent1'].ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config1
        )
        
        results["stage1"]["messages"] = response1["messages"]
        
        # 如果是交互模式，可以进行多轮对话
        if interactive:
            print("\n当前需求澄清结果（请确认或继续追问）：")
            print(response1["messages"][-1].content)
            # 这里可以添加交互逻辑，让用户选择是否继续追问
        else:
            # 非交互模式，直接生成最终摘要
            # 添加提示要求生成摘要
            summary_prompt = "请根据我们的对话，生成最终的需求摘要。"
            final_response1 = await self.agents['agent1'].ainvoke(
                {"messages": response1["messages"] + [HumanMessage(content=summary_prompt)]},
                config=config1
            )
            results["stage1"]["messages"] = final_response1["messages"]
        
        # 提取需求摘要
        requirement_summary = self._extract_summary_from_agent1(results["stage1"]["messages"])
        results["stage1"]["requirement_summary"] = requirement_summary
        
        print("\n✅ 阶段1完成，需求摘要已生成")
        
        # ========== 阶段2: PRD生成 ==========
        print("\n" + "="*60)
        print("【阶段2：PRD结构化生成器】")
        print("="*60)
        
        config2 = {"configurable": {"thread_id": f"{thread_id}_agent2"}}
        
        # 将Agent1的需求摘要传递给Agent2
        prd_input = f"请根据以下需求摘要生成PRD文档：\n\n{requirement_summary}"
        
        response2 = await self.agents['agent2'].ainvoke(
            {"messages": [HumanMessage(content=prd_input)]},
            config=config2
        )
        
        results["stage2"]["messages"] = response2["messages"]
        
        # 提取PRD文档
        prd_document = self._extract_prd_from_agent2(results["stage2"]["messages"])
        results["stage2"]["prd_document"] = prd_document
        
        print("\n✅ 阶段2完成，PRD文档已生成")
        
        # ========== 阶段3: 原型辅助 ==========
        print("\n" + "="*60)
        print("【阶段3：原型与交互辅助】")
        print("="*60)
        
        config3 = {"configurable": {"thread_id": f"{thread_id}_agent3"}}
        
        # 将Agent2的PRD文档传递给Agent3
        design_input = f"请根据以下PRD文档生成界面设计方案：\n\n{prd_document}"
        
        response3 = await self.agents['agent3'].ainvoke(
            {"messages": [HumanMessage(content=design_input)]},
            config=config3
        )
        
        results["stage3"]["messages"] = response3["messages"]
        
        # 提取设计文档
        design_document = self._extract_design_from_agent3(results["stage3"]["messages"])
        results["stage3"]["design_document"] = design_document
        
        print("\n✅ 阶段3完成，界面设计方案已生成")
        
        # 保存结果
        self.results[thread_id] = results
        
        return results
    
    async def run_stage1_only(
        self,
        user_input: str,
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        仅执行阶段1：需求澄清
        
        Args:
            user_input: 用户的初始需求输入
            thread_id: 会话ID
            
        Returns:
            包含需求摘要的字典
        """
        self._init_agents()
        
        config = {"configurable": {"thread_id": f"{thread_id}_agent1"}}
        
        response = await self.agents['agent1'].ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )
        
        summary = self._extract_summary_from_agent1(response["messages"])
        
        return {
            "requirement_summary": summary,
            "messages": response["messages"]
        }
    
    async def run_stage2_only(
        self,
        requirement_summary: str,
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        仅执行阶段2：PRD生成
        
        Args:
            requirement_summary: 需求摘要（来自Agent1或手动提供）
            thread_id: 会话ID
            
        Returns:
            包含PRD文档的字典
        """
        self._init_agents()
        
        config = {"configurable": {"thread_id": f"{thread_id}_agent2"}}
        
        input_msg = f"请根据以下需求摘要生成PRD文档：\n\n{requirement_summary}"
        
        response = await self.agents['agent2'].ainvoke(
            {"messages": [HumanMessage(content=input_msg)]},
            config=config
        )
        
        prd_document = self._extract_prd_from_agent2(response["messages"])
        
        return {
            "prd_document": prd_document,
            "messages": response["messages"]
        }
    
    async def run_stage3_only(
        self,
        prd_document: str,
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        仅执行阶段3：原型辅助
        
        Args:
            prd_document: PRD文档（来自Agent2或手动提供）
            thread_id: 会话ID
            
        Returns:
            包含设计文档的字典
        """
        self._init_agents()
        
        config = {"configurable": {"thread_id": f"{thread_id}_agent3"}}
        
        input_msg = f"请根据以下PRD文档生成界面设计方案：\n\n{prd_document}"
        
        response = await self.agents['agent3'].ainvoke(
            {"messages": [HumanMessage(content=input_msg)]},
            config=config
        )
        
        design_document = self._extract_design_from_agent3(response["messages"])
        
        return {
            "design_document": design_document,
            "messages": response["messages"]
        }
    
    async def continue_stage1(
        self,
        user_reply: str,
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        继续阶段1的对话（多轮追问）
        
        Args:
            user_reply: 用户的回复
            thread_id: 会话ID
            
        Returns:
            包含对话历史的字典
        """
        self._init_agents()
        
        config = {"configurable": {"thread_id": f"{thread_id}_agent1"}}
        
        response = await self.agents['agent1'].ainvoke(
            {"messages": [HumanMessage(content=user_reply)]},
            config=config
        )
        
        summary = self._extract_summary_from_agent1(response["messages"])
        
        return {
            "requirement_summary": summary,
            "messages": response["messages"]
        }
    
    def get_results(self, thread_id: str = "default") -> Optional[Dict[str, Any]]:
        """
        获取指定会话的结果
        
        Args:
            thread_id: 会话ID
            
        Returns:
            会话结果字典，如果不存在则返回None
        """
        return self.results.get(thread_id)
    
    def clear_session(self, thread_id: str = "default"):
        """
        清除指定会话的状态和结果
        
        Args:
            thread_id: 会话ID
        """
        if thread_id in self.results:
            del self.results[thread_id]


# 创建全局协调器实例
coordinator = WorkflowCoordinator()


async def run_requirement_workflow(
    user_input: str,
    mode: str = "full",
    thread_id: str = "default",
    input_data: Optional[str] = None
) -> Dict[str, Any]:
    """
    便捷函数：执行需求处理工作流
    
    Args:
        user_input: 用户输入
        mode: 执行模式
            - "full": 完整的三层流程
            - "stage1": 仅需求澄清
            - "stage2": 仅PRD生成（需要input_data提供需求摘要）
            - "stage3": 仅原型辅助（需要input_data提供PRD文档）
        thread_id: 会话ID
        input_data: 输入数据（stage2需要需求摘要，stage3需要PRD文档）
        
    Returns:
        工作流执行结果
    """
    if mode == "full":
        return await coordinator.run_full_workflow(user_input, thread_id)
    elif mode == "stage1":
        return await coordinator.run_stage1_only(user_input, thread_id)
    elif mode == "stage2":
        if not input_data:
            raise ValueError("Stage2模式需要提供input_data（需求摘要）")
        return await coordinator.run_stage2_only(input_data, thread_id)
    elif mode == "stage3":
        if not input_data:
            raise ValueError("Stage3模式需要提供input_data（PRD文档）")
        return await coordinator.run_stage3_only(input_data, thread_id)
    else:
        raise ValueError(f"未知的执行模式: {mode}")
