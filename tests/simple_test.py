"""
简单的三层Agent工作流测试
"""

import asyncio
import sys
import os

# 确保能导入模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 直接导入需要的函数，避免相对导入问题
import importlib.util

def load_module_from_path(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# 加载三个Agent模块
agent1_module = load_module_from_path('agent1', 'src/agents/agent1_requirement_clarifier.py')
agent2_module = load_module_from_path('agent2', 'src/agents/agent2_prd_builder.py')
agent3_module = load_module_from_path('agent3', 'src/agents/agent3_prototype_assistant.py')

async def test_agents():
    """测试三个Agent是否能正常构建"""
    
    print("="*60)
    print("测试三层Agent构建")
    print("="*60)
    
    try:
        # 测试Agent 1
        print("\n1. 测试Agent 1 (需求澄清助手)...")
        agent1 = agent1_module.build_agent()
        print("   ✅ Agent 1 构建成功")
        
        # 测试Agent 2
        print("\n2. 测试Agent 2 (PRD生成器)...")
        agent2 = agent2_module.build_agent()
        print("   ✅ Agent 2 构建成功")
        
        # 测试Agent 3
        print("\n3. 测试Agent 3 (原型辅助)...")
        agent3 = agent3_module.build_agent()
        print("   ✅ Agent 3 构建成功")
        
        print("\n" + "="*60)
        print("所有Agent构建测试通过！")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_agents())
