# 三层AI Agent需求处理系统

## 🎯 项目简介

一套完整的企业级AI赋能需求处理流程，能够将用户简单的一句话需求转化为标准化的PRD文档和界面设计方案。

### 核心特性

✅ **智能需求澄清**：将模糊的需求想法转化为结构化摘要  
✅ **多模板PRD生成**：支持5种需求类型的PRD模板（功能型/优化型/策略型/数据型/增长型）  
✅ **原型设计辅助**：从PRD生成界面设计方案和AI绘图提示词  
✅ **协同工作流**：三个Agent无缝协作，数据自动流转  
✅ **灵活调用**：支持完整流程、单步执行、选择性执行  
✅ **对话记忆**：每个Agent独立维护对话历史

### 工作流程

```
用户输入（一句话需求）
    ↓
[Agent 1: 需求澄清助手] → 需求摘要
    ↓
[Agent 2: PRD生成器] → PRD文档
    ↓
[Agent 3: 原型辅助] → 界面设计方案
```

## 📁 项目结构

```
.
├── config/                                   # 配置目录
│   ├── agent1_config.json                    # Agent 1 配置
│   ├── agent2_config.json                    # Agent 2 配置
│   └── agent3_config.json                    # Agent 3 配置
├── docs/                                     # 文档目录
│   └── USAGE.md                              # 使用文档
├── src/
│   ├── agents/                               # Agent代码
│   │   ├── agent1_requirement_clarifier.py   # Agent 1: 需求澄清助手
│   │   ├── agent2_prd_builder.py            # Agent 2: PRD生成器
│   │   ├── agent3_prototype_assistant.py     # Agent 3: 原型辅助
│   │   ├── workflow_coordinator.py          # 工作流协调器
│   │   └── __init__.py
│   └── storage/                             # 存储层
│       └── memory/
│           └── memory_saver.py               # 记忆存储
└── tests/                                    # 测试目录
    ├── test_complete_workflow.py            # 完整工作流测试
    ├── test_step_by_step.py                 # 分步测试
    └── simple_test.py                       # 简单测试
```

## 🚀 快速开始

### 1. 环境准备

确保已安装Python 3.8+和必要的依赖。

### 2. 测试Agent构建

```bash
cd /workspace/projects

python -c "
import os
os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'

from src.agents.agent1_requirement_clarifier import build_agent as build_agent1
from src.agents.agent2_prd_builder import build_agent as build_agent2
from src.agents.agent3_prototype_assistant import build_agent as build_agent3

agent1 = build_agent1()
agent2 = build_agent2()
agent3 = build_agent3()

print('✅ 所有Agent构建成功！')
"
```

### 3. 运行完整工作流

```python
import asyncio
import os
from src.agents.workflow_coordinator import run_requirement_workflow

async def main():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 用户输入
    user_input = "我要开发一个用户登录功能，支持账号密码登录和手机验证码登录两种方式"
    
    # 执行完整工作流
    results = await run_requirement_workflow(
        user_input=user_input,
        mode="full",
        thread_id="my_project"
    )
    
    # 输出结果
    print("\n=== 阶段1：需求摘要 ===")
    print(results["stage1"]["requirement_summary"][:500] + "...")
    
    print("\n=== 阶段2：PRD文档 ===")
    print(results["stage2"]["prd_document"][:500] + "...")
    
    print("\n=== 阶段3：设计方案 ===")
    print(results["stage3"]["design_document"][:500] + "...")

asyncio.run(main())
```

## 📖 使用文档

详细的使用文档请查看：[docs/USAGE.md](docs/USAGE.md)

内容包括：
- 系统架构详解
- 各Agent功能说明
- 使用方式（完整流程/分步执行/选择性执行）
- 配置说明
- API参考
- 常见问题
- 进阶使用

## 🔧 三层Agent说明

### Agent 1: 需求澄清助手

**功能定位**：将模糊的需求想法转化为结构化需求摘要

**核心能力**：
- 需求类型识别（增长型/功能型/体验型/策略型/数据型）
- 5W2H追问框架
- 多轮对话收集信息
- 生成结构化需求摘要

**配置文件**：`config/agent1_config.json`

### Agent 2: PRD结构化生成器

**功能定位**：将需求摘要转化为完整的PRD文档

**核心能力**：
- 5种PRD模板支持
- 自动生成用户故事和验收标准
- 完整的PRD结构
- 风险识别和依赖分析

**配置文件**：`config/agent2_config.json`

### Agent 3: 原型与交互辅助

**功能定位**：从PRD生成界面设计方案

**核心能力**：
- 页面清单规划
- 单页详细描述
- AI绘图提示词生成
- 设计系统建议

**配置文件**：`config/agent3_config.json`

## 💡 使用示例

### 完整工作流

```python
from src.agents.workflow_coordinator import run_requirement_workflow

results = await run_requirement_workflow(
    user_input="我要开发一个登录功能",
    mode="full",
    thread_id="project_001"
)
```

### 分步执行

```python
# 步骤1: 需求澄清
result1 = await run_requirement_workflow(
    user_input="我要开发一个登录功能",
    mode="stage1",
    thread_id="project_001"
)

# 步骤2: 生成PRD
result2 = await run_requirement_workflow(
    user_input="",
    mode="stage2",
    thread_id="project_001",
    input_data=result1["requirement_summary"]
)

# 步骤3: 生成设计
result3 = await run_requirement_workflow(
    user_input="",
    mode="stage3",
    thread_id="project_001",
    input_data=result2["prd_document"]
)
```

## 🎨 技术栈

- **LangChain**: Agent框架
- **LangGraph**: 状态管理和工作流编排
- **Doubao Seed**: 大语言模型（思考模型）
- **Python 3.8+**: 编程语言

## 📝 测试

### 运行测试

```bash
# 测试Agent构建
python tests/simple_test.py

# 分步测试
python tests/test_step_by_step.py

# 完整工作流测试
python tests/test_complete_workflow.py
```

## 🔍 配置说明

### 模型配置

每个Agent都有独立的配置文件，主要配置项：

```json
{
    "config": {
        "model": "doubao-seed-1-6-thinking-250715",
        "temperature": 0.7,
        "top_p": 0.9,
        "max_completion_tokens": 8000,
        "timeout": 600,
        "thinking": "enabled"
    },
    "sp": "System Prompt..."
}
```

**配置项说明**：
- `model`: 使用的模型ID
- `temperature`: 输出的随机性（0-2）
- `top_p`: 核采样参数（0-1）
- `max_completion_tokens`: 最大输出token数
- `timeout`: 请求超时时间（秒）
- `thinking`: 是否开启思考模式
- `sp`: System Prompt（角色定义和任务目标）

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👥 团队

本项目由Coze Coding搭建，采用LangChain和LangGraph框架。

## 📧 联系方式

如有问题或建议，请提交Issue。

---

**祝使用愉快！** 🎉
