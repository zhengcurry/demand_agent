# 三层AI Agent需求处理系统 - 使用文档

## 📋 目录

1. [系统概述](#系统概述)
2. [快速开始](#快速开始)
3. [系统架构](#系统架构)
4. [各Agent功能说明](#各agent功能说明)
5. [使用方式](#使用方式)
6. [配置说明](#配置说明)
7. [API参考](#api参考)
8. [常见问题](#常见问题)
9. [进阶使用](#进阶使用)

---

## 系统概述

三层AI Agent需求处理系统是一套完整的企业级需求处理解决方案，能够将用户的简单需求描述转化为标准化的PRD文档和界面设计方案。

### 核心特性

- ✅ **智能需求澄清**：将模糊的需求想法转化为结构化摘要
- ✅ **多模板PRD生成**：支持5种需求类型的PRD模板
- ✅ **原型设计辅助**：从PRD生成界面设计方案和AI绘图提示词
- ✅ **协同工作流**：三个Agent无缝协作，数据自动流转
- ✅ **灵活调用**：支持完整流程、单步执行、选择性执行
- ✅ **对话记忆**：每个Agent独立维护对话历史

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

---

## 快速开始

### 环境要求

- Python 3.8+
- 网络连接（访问大模型API）
- 已安装依赖（见 requirements.txt）

### 安装

```bash
# 克隆或下载项目
cd /workspace/projects

# 安装依赖（如果需要）
pip install -r requirements.txt
```

### 快速测试

```bash
# 测试Agent构建
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

---

## 系统架构

### 文件结构

```
src/
├── agents/
│   ├── agent1_requirement_clarifier.py   # Agent 1: 需求澄清助手
│   ├── agent2_prd_builder.py            # Agent 2: PRD生成器
│   ├── agent3_prototype_assistant.py     # Agent 3: 原型辅助
│   ├── workflow_coordinator.py           # 工作流协调器
│   └── __init__.py
├── config/
│   ├── agent1_config.json                # Agent 1 配置
│   ├── agent2_config.json                # Agent 2 配置
│   └── agent3_config.json                # Agent 3 配置
└── storage/
    └── memory/
        └── memory_saver.py               # 记忆存储

tests/
├── test_complete_workflow.py             # 完整工作流测试
├── test_step_by_step.py                  # 分步测试
└── simple_test.py                        # 简单测试
```

### 三层Agent说明

#### Agent 1: 需求澄清助手

**功能定位**：将模糊的需求想法转化为结构化需求摘要

**核心能力**：
- 需求类型识别（增长型/功能型/体验型/策略型/数据型）
- 5W2H追问框架
- 多轮对话收集信息
- 生成结构化需求摘要

**配置文件**：`config/agent1_config.json`

#### Agent 2: PRD结构化生成器

**功能定位**：将需求摘要转化为完整的PRD文档

**核心能力**：
- 5种PRD模板支持（功能型/优化型/策略型/数据型/增长型）
- 自动生成用户故事和验收标准
- 完整的PRD结构
- 风险识别和依赖分析

**配置文件**：`config/agent2_config.json`

#### Agent 3: 原型与交互辅助

**功能定位**：从PRD生成界面设计方案

**核心能力**：
- 页面清单规划
- 单页详细描述
- AI绘图提示词生成
- 设计系统建议（色彩、字体、组件等）

**配置文件**：`config/agent3_config.json`

---

## 各Agent功能说明

### Agent 1: 需求澄清助手

#### 输入输出

**输入**：
- 用户的一句话需求
- 可以是多轮对话的交互

**输出**：
- 结构化需求摘要（Markdown格式）
- 包含：需求类型、核心目标、目标用户、主要场景、关键指标、功能要点等

#### 使用示例

```python
import asyncio
import os
from src.agents.agent1_requirement_clarifier import build_agent
from langchain_core.messages import HumanMessage

async def example():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 构建Agent
    agent = build_agent()
    
    # 配置
    config = {"configurable": {"thread_id": "my_session"}}
    
    # 第一次对话
    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="我要开发一个登录功能")]},
        config=config
    )
    
    print(response["messages"][-1].content)
    
    # 要求生成摘要
    summary_response = await agent.ainvoke(
        {"messages": response["messages"] + [HumanMessage(content="请生成需求摘要")]},
        config=config
    )
    
    print(summary_response["messages"][-1].content)

asyncio.run(example())
```

#### 需求类型

Agent 1会识别需求类型并选择对应的追问模板：

| 需求类型 | 特点 | 追问重点 |
|---------|------|---------|
| 增长型 | 关注用户增长、转化 | 目标指标、增长策略 |
| 功能型 | 新增具体功能 | 功能场景、用户价值 |
| 体验优化 | 优化现有体验 | 问题点、优化目标 |
| 策略型 | 涉及业务策略 | 策略规则、影响范围 |
| 数据型 | 数据统计、报表 | 数据指标、展示方式 |

### Agent 2: PRD结构化生成器

#### 输入输出

**输入**：
- 需求摘要（来自Agent 1或手动提供）

**输出**：
- 完整的PRD文档（Markdown格式）
- 包含：项目概述、用户分析、功能需求、非功能需求、技术方案等

#### PRD模板

Agent 2支持5种PRD模板，根据需求类型自动选择：

1. **功能型需求模板**：标准PRD结构
2. **体验优化需求模板**：包含前后对比、A/B测试方案
3. **策略型需求模板**：包含策略规则、利益相关方分析
4. **数据型需求模板**：包含数据指标定义、埋点设计
5. **增长型需求模板**：包含增长策略、实验设计

#### 使用示例

```python
import asyncio
import os
from src.agents.agent2_prd_builder import build_agent
from langchain_core.messages import HumanMessage

async def example():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 构建Agent
    agent = build_agent()
    config = {"configurable": {"thread_id": "prd_session"}}
    
    # 需求摘要
    requirement_summary = """
    # 需求摘要
    
    ## 1. 需求类型
    功能型
    
    ## 2. 核心目标
    开发用户登录功能
    
    ## 3. 目标用户
    所有用户
    
    ...
    """
    
    # 生成PRD
    response = await agent.ainvoke(
        {"messages": [HumanMessage(content=f"请生成PRD：{requirement_summary}")]},
        config=config
    )
    
    print(response["messages"][-1].content)

asyncio.run(example())
```

### Agent 3: 原型与交互辅助

#### 输入输出

**输入**：
- PRD文档（来自Agent 2或手动提供）

**输出**：
- 界面设计方案（Markdown格式）
- 包含：页面清单、单页描述、设计提示词、设计系统建议

#### 使用示例

```python
import asyncio
import os
from src.agents.agent3_prototype_assistant import build_agent
from langchain_core.messages import HumanMessage

async def example():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 构建Agent
    agent = build_agent()
    config = {"configurable": {"thread_id": "design_session"}}
    
    # PRD文档
    prd_document = """
    # PRD文档：用户登录功能
    
    ## 三、功能需求
    ### 3.1 功能清单
    - 功能1：账号密码登录
    - 功能2：手机验证码登录
    ...
    """
    
    # 生成设计方案
    response = await agent.ainvoke(
        {"messages": [HumanMessage(content=f"请生成设计方案：{prd_document[:1500]}")]},
        config=config
    )
    
    print(response["messages"][-1].content)

asyncio.run(example())
```

---

## 使用方式

### 方式1: 完整工作流（推荐）

一次性执行三个Agent，自动传递数据：

```python
import asyncio
import os
from src.agents.workflow_coordinator import run_requirement_workflow

async def main():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 用户输入
    user_input = "我要开发一个登录功能，支持账号密码和手机验证码登录"
    
    # 执行完整工作流
    results = await run_requirement_workflow(
        user_input=user_input,
        mode="full",
        thread_id="my_project"
    )
    
    # 获取结果
    print("需求摘要:", results["stage1"]["requirement_summary"])
    print("PRD文档:", results["stage2"]["prd_document"])
    print("设计文档:", results["stage3"]["design_document"])

asyncio.run(main())
```

### 方式2: 分步执行

分别执行每个Agent，适合需要中间人工审核的场景：

```python
import asyncio
import os
from src.agents.workflow_coordinator import run_requirement_workflow

async def main():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 步骤1: 需求澄清
    result1 = await run_requirement_workflow(
        user_input="我要开发一个登录功能",
        mode="stage1",
        thread_id="my_project"
    )
    requirement_summary = result1["requirement_summary"]
    
    # 人工审核需求摘要...
    
    # 步骤2: 生成PRD
    result2 = await run_requirement_workflow(
        user_input="",
        mode="stage2",
        thread_id="my_project",
        input_data=requirement_summary
    )
    prd_document = result2["prd_document"]
    
    # 人工审核PRD...
    
    # 步骤3: 生成设计
    result3 = await run_requirement_workflow(
        user_input="",
        mode="stage3",
        thread_id="my_project",
        input_data=prd_document
    )
    design_document = result3["design_document"]
    
    print("全部完成！")

asyncio.run(main())
```

### 方式3: 选择性执行

只执行需要的阶段：

```python
import asyncio
import os
from src.agents.workflow_coordinator import run_requirement_workflow

async def main():
    os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'
    
    # 只执行PRD生成（已有需求摘要）
    result = await run_requirement_workflow(
        user_input="",
        mode="stage2",
        thread_id="my_project",
        input_data="现有的需求摘要..."
    )
    
    print(result["prd_document"])

asyncio.run(main())
```

---

## 配置说明

### Agent配置文件

每个Agent都有独立的配置文件：

#### config/agent1_config.json

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
    "sp": "Agent 1的System Prompt..."
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

### 模型选择建议

| 场景 | 推荐模型 | 说明 |
|------|---------|------|
| 需求澄清 | doubao-seed-1-6-thinking | 需要深度理解意图 |
| PRD生成 | doubao-seed-1-6-thinking | 需要逻辑严密的结构 |
| 原型辅助 | doubao-seed-1-6-thinking | 需要视觉描述能力 |

### 记忆窗口配置

每个Agent的消息窗口大小可以在代码中调整：

```python
# agent1_requirement_clarifier.py
MAX_MESSAGES = 60  # 30轮对话

# agent2_prd_builder.py
MAX_MESSAGES = 60  # 30轮对话

# agent3_prototype_assistant.py
MAX_MESSAGES = 80  # 40轮对话
```

---

## API参考

### run_requirement_workflow

执行需求处理工作流的主函数。

**参数**：
- `user_input` (str): 用户输入的初始需求
- `mode` (str): 执行模式
  - `"full"`: 完整的三层流程
  - `"stage1"`: 仅需求澄清
  - `"stage2"`: 仅PRD生成（需要input_data）
  - `"stage3"`: 仅原型辅助（需要input_data）
- `thread_id` (str): 会话ID，用于保持对话历史
- `input_data` (str, optional): 输入数据
  - mode="stage2"时：需求摘要
  - mode="stage3"时：PRD文档

**返回**：
```python
{
    "stage1": {
        "requirement_summary": "需求摘要文本",
        "messages": [...]  # 对话历史
    },
    "stage2": {
        "prd_document": "PRD文档文本",
        "messages": [...]
    },
    "stage3": {
        "design_document": "设计文档文本",
        "messages": [...]
    }
}
```

**示例**：
```python
from src.agents.workflow_coordinator import run_requirement_workflow

results = await run_requirement_workflow(
    user_input="我要开发一个登录功能",
    mode="full",
    thread_id="project_001"
)
```

### WorkflowCoordinator

工作流协调器类，提供更细粒度的控制。

**方法**：
- `run_full_workflow(user_input, thread_id, interactive)`: 执行完整流程
- `run_stage1_only(user_input, thread_id)`: 仅执行阶段1
- `run_stage2_only(requirement_summary, thread_id)`: 仅执行阶段2
- `run_stage3_only(prd_document, thread_id)`: 仅执行阶段3
- `continue_stage1(user_reply, thread_id)`: 继续阶段1的对话
- `get_results(thread_id)`: 获取会话结果
- `clear_session(thread_id)`: 清除会话状态

**示例**：
```python
from src.agents.workflow_coordinator import WorkflowCoordinator

coordinator = WorkflowCoordinator()

# 初始化所有Agent
coordinator._init_agents()

# 执行完整流程
results = await coordinator.run_full_workflow(
    user_input="我要开发一个登录功能",
    thread_id="project_001"
)
```

---

## 常见问题

### Q1: 如何调整Agent的输出风格？

修改对应Agent配置文件中的`temperature`参数：
- 0.0-0.3: 更加确定、保守
- 0.4-0.7: 平衡（推荐）
- 0.8-2.0: 更加创造、多样化

### Q2: Agent响应时间过长怎么办？

1. 检查网络连接
2. 考虑使用更快的模型（如doubao-seed-1-6-flash）
3. 减少`max_completion_tokens`参数
4. 分阶段执行，而不是完整工作流

### Q3: 如何保存对话历史？

对话历史通过`checkpointer`自动保存到内存中。如需持久化保存：

```python
# 使用文件或数据库保存results
import json

results = await run_requirement_workflow(...)
with open("results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### Q4: Agent生成的PRD太长怎么办？

1. 在配置文件中减少`max_completion_tokens`
2. 明确告知Agent需要精简的PRD
3. 只执行关键部分，其他部分手动补充

### Q5: 如何集成到现有项目？

有两种方式：

**方式1**: 直接导入使用
```python
from src.agents.workflow_coordinator import run_requirement_workflow

# 在你的代码中调用
results = await run_requirement_workflow(...)
```

**方式2**: 封装为API服务
使用FastAPI等框架封装为HTTP API（见进阶使用）

---

## 进阶使用

### 集成到Web应用

使用FastAPI封装为HTTP服务：

```python
from fastapi import FastAPI
import os

os.environ['COZE_WORKSPACE_PATH'] = '/workspace/projects'

from src.agents.workflow_coordinator import run_requirement_workflow

app = FastAPI()

@app.post("/api/process-requirement")
async def process_requirement(user_input: str):
    results = await run_requirement_workflow(
        user_input=user_input,
        mode="full",
        thread_id="web_app"
    )
    return {
        "requirement_summary": results["stage1"]["requirement_summary"],
        "prd_document": results["stage2"]["prd_document"],
        "design_document": results["stage3"]["design_document"]
    }
```

### 自定义System Prompt

编辑配置文件中的`sp`字段，自定义Agent的行为：

```json
{
    "sp": "# 角色定义\n你是我们的产品专家...\n# 任务目标\n..."
}
```

### 批量处理多个需求

```python
requirements = [
    "我要开发一个登录功能",
    "我要优化购物车体验",
    "我要做一个用户增长活动"
]

async def batch_process():
    results = []
    for req in requirements:
        result = await run_requirement_workflow(
            user_input=req,
            mode="full",
            thread_id=f"batch_{len(results)}"
        )
        results.append(result)
    return results
```

---

## 总结

三层AI Agent需求处理系统提供了一套完整的需求处理解决方案：

1. **Agent 1（需求澄清）**：模糊需求 → 结构化摘要
2. **Agent 2（PRD生成）**：需求摘要 → 完整PRD
3. **Agent 3（原型辅助）**：PRD文档 → 界面设计

系统支持灵活的调用方式，可以完整执行、分步执行或选择性执行，满足不同场景的需求。

**快速开始**：
```bash
python -c "from src.agents.workflow_coordinator import run_requirement_workflow; import asyncio, os; os.environ['COZE_WORKSPACE_PATH']='/workspace/projects'; asyncio.run(run_requirement_workflow('我要开发一个登录功能', 'full', 'test'))"
```

祝使用愉快！🎉
