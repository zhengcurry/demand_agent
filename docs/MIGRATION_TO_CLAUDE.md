# 从扣子平台迁移到Claude的完整指南

本文档提供从扣子（Coze）平台迁移到 Anthropic Claude 的详细步骤。

## 目录
1. [变更概述](#变更概述)
2. [环境配置](#环境配置)
3. [代码变更](#代码变更)
4. [测试验证](#测试验证)
5. [常见问题](#常见问题)

---

## 变更概述

### 主要变更点

| 项目 | 迁移前（Coze） | 迁移后（Claude） |
|------|---------------|-----------------|
| 模型提供商 | 豆包（Doubao） | Anthropic Claude |
| 模型ID | doubao-seed-1-6-thinking-250715 | claude-sonnet-4-5 / claude-opus-4 |
| SDK | langchain-openai | langchain-anthropic |
| 环境变量 | COZE_WORKSPACE_PATH<br>COZE_WORKLOAD_IDENTITY_API_KEY<br>COZE_INTEGRATION_MODEL_BASE_URL | WORKSPACE_PATH<br>ANTHROPIC_API_KEY |
| 依赖包 | coze-coding-utils<br>coze-workload-identity | anthropic<br>langchain-anthropic |

---

## 环境配置

### 1. 安装依赖

```bash
# 安装 Anthropic SDK
pip install anthropic>=0.40.0 langchain-anthropic>=0.3.0

# 或者更新 requirements.txt 后安装
pip install -r requirements.txt
```

### 2. 设置环境变量

**方法一：命令行设置（临时）**
```bash
# Linux/Mac
export WORKSPACE_PATH=$(pwd)
export ANTHROPIC_API_KEY="your-anthropic-api-key"

# Windows (CMD)
set WORKSPACE_PATH=%cd%
set ANTHROPIC_API_KEY=your-anthropic-api-key

# Windows (PowerShell)
$env:WORKSPACE_PATH = $pwd
$env:ANTHROPIC_API_KEY = "your-anthropic-api-key"
```

**方法二：使用 .env 文件（推荐）**

创建 `.env` 文件：
```bash
WORKSPACE_PATH=/path/to/project
ANTHROPIC_API_KEY=your-anthropic-api-key
```

然后在代码中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

### 3. 获取 Anthropic API Key

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册/登录账号
3. 导航到 API Keys 页面
4. 创建新的 API Key
5. 复制并保存（只显示一次）

---

## 代码变更

### 1. Agent 代码变更

已完成的变更（针对三个 Agent）：

**变更前（agent1_requirement_clarifier.py）：**
```python
from langchain_openai import ChatOpenAI
from coze_coding_utils.runtime_ctx.context import default_headers

api_key = os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY")
base_url = os.getenv("COZE_INTEGRATION_MODEL_BASE_URL")

llm = ChatOpenAI(
    model=cfg['config'].get("model"),
    api_key=api_key,
    base_url=base_url,
    temperature=cfg['config'].get('temperature', 0.7),
    streaming=True,
    timeout=cfg['config'].get('timeout', 600),
    extra_body={
        "thinking": {
            "type": cfg['config'].get('thinking', 'disabled')
        }
    },
    default_headers=default_headers(ctx) if ctx else {}
)
```

**变更后：**
```python
from langchain_anthropic import ChatAnthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

thinking_enabled = cfg['config'].get('thinking', 'disabled') == 'enabled'

llm_kwargs = {
    "model": cfg['config'].get("model", "claude-sonnet-4-5"),
    "api_key": api_key,
    "temperature": cfg['config'].get('temperature', 0.7),
    "max_tokens": cfg['config'].get('max_completion_tokens', 8000),
    "timeout": cfg['config'].get('timeout', 600),
}

if thinking_enabled:
    llm_kwargs["model_kwargs"] = {
        "thinking": {
            "type": "enabled",
            "budget_tokens": 10000
        }
    }

llm = ChatAnthropic(**llm_kwargs)
```

### 2. 配置文件变更

更新 `config/agent1_config.json`、`agent2_config.json`、`agent3_config.json`：

**变更前：**
```json
{
    "config": {
        "model": "doubao-seed-1-6-thinking-250715",
        "temperature": 0.7,
        ...
    }
}
```

**变更后：**
```json
{
    "config": {
        "model": "claude-sonnet-4-5",
        "temperature": 0.7,
        ...
    }
}
```

### 3. 可选模型

根据需求选择合适的模型：

| 模型 | 特点 | 适用场景 | 成本 |
|------|------|---------|------|
| claude-opus-4 | 最强推理能力 | 复杂任务，需要深度思考 | 高 |
| claude-sonnet-4-5 | 平衡性能和成本 | 大多数任务（推荐） | 中 |
| claude-sonnet-4 | 较快速度 | 简单任务 | 低 |
| claude-haiku-4 | 最快速度 | 简单、快速响应任务 | 最低 |

**修改建议：**
- Agent 1（需求澄清）：使用 `claude-sonnet-4-5`
- Agent 2（PRD生成）：使用 `claude-sonnet-4-5` 或 `claude-opus-4`
- Agent 3（设计方案）：使用 `claude-sonnet-4-5`

---

## 测试验证

### 1. 简单测试

```bash
# 设置环境变量
export WORKSPACE_PATH=$(pwd)
export ANTHROPIC_API_KEY="your-api-key"

# 测试 Agent 构建
python tests/simple_test.py
```

### 2. 分步测试

```bash
# 测试各个阶段
python tests/test_step_by_step.py
```

### 3. 完整工作流测试

```bash
# 测试端到端工作流
python tests/test_complete_workflow.py
```

### 4. 预期输出

**成功示例：**
```
============================================================
【阶段1：需求澄清助手】
============================================================
处理用户输入...
✅ 阶段1完成，需求摘要已生成

============================================================
【阶段2：PRD结构化生成器】
============================================================
生成PRD文档...
✅ 阶段2完成，PRD文档已生成

============================================================
【阶段3：原型与交互辅助】
============================================================
生成界面设计方案...
✅ 阶段3完成，界面设计方案已生成
```

---

## 常见问题

### Q1: 提示 "ANTHROPIC_API_KEY environment variable is required"

**原因**：未设置 API Key 环境变量

**解决方案**：
```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### Q2: 提示 "No module named 'langchain_anthropic'"

**原因**：未安装 langchain-anthropic 包

**解决方案**：
```bash
pip install langchain-anthropic
```

### Q3: API 调用失败，提示 401 Unauthorized

**原因**：API Key 无效或已过期

**解决方案**：
1. 检查 API Key 是否正确
2. 访问 [Anthropic Console](https://console.anthropic.com/) 验证 Key 是否有效
3. 如果失效，生成新的 API Key

### Q4: 提示 "Rate limit exceeded"

**原因**：超过 API 调用速率限制

**解决方案**：
1. 等待一段时间后重试
2. 升级到更高的 API 计划
3. 在代码中添加重试逻辑（已包含在 LangChain 中）

### Q5: Extended Thinking 模式不工作

**原因**：配置不正确或模型不支持

**解决方案**：
1. 确保使用支持 extended thinking 的模型（Opus 4, Sonnet 4+）
2. 检查配置文件中 `thinking` 设置为 `"enabled"`
3. 确认代码中正确传递了 `model_kwargs`

### Q6: 输出质量与之前不同

**原因**：不同模型的特性差异

**解决方案**：
1. 调整 `temperature` 参数（降低可提高稳定性）
2. 优化 system prompt
3. 尝试使用 `claude-opus-4` 获得更好的输出

### Q7: 成本比之前高

**原因**：Claude 与豆包的定价不同

**解决方案**：
1. 使用 `claude-sonnet-4-5` 而非 Opus 4（成本更低）
2. 减少 `max_completion_tokens` 设置
3. 优化 prompt 以减少 token 消耗
4. 考虑只在需要时开启 thinking 模式

---

## 性能对比

### 模型对比

| 特性 | Doubao Seed | Claude Sonnet 4.5 | Claude Opus 4 |
|------|-------------|-------------------|---------------|
| 推理能力 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 响应速度 | 快 | 中 | 较慢 |
| 成本 | - | 中 | 高 |
| 中文支持 | 优秀 | 优秀 | 优秀 |
| Thinking模式 | ✅ | ✅ | ✅ |

### 建议配置

**开发环境**：使用 `claude-sonnet-4-5`，thinking 模式可选
**生产环境**：根据需求选择，考虑成本和质量平衡

---

## 回滚方案

如果需要回滚到扣子平台，保留以下文件：

```bash
# 备份迁移前的文件
git checkout HEAD~1 -- src/agents/agent1_requirement_clarifier.py
git checkout HEAD~1 -- src/agents/agent2_prd_builder.py
git checkout HEAD~1 -- src/agents/agent3_prototype_assistant.py
git checkout HEAD~1 -- config/agent1_config.json
git checkout HEAD~1 -- config/agent2_config.json
git checkout HEAD~1 -- config/agent3_config.json
```

然后恢复环境变量：
```bash
export COZE_WORKSPACE_PATH=/path/to/project
export COZE_WORKLOAD_IDENTITY_API_KEY="your-key"
export COZE_INTEGRATION_MODEL_BASE_URL="your-url"
```

---

## 下一步

1. ✅ 完成代码迁移
2. ✅ 更新配置文件
3. ✅ 设置环境变量
4. ⬜ 运行测试验证
5. ⬜ 监控生产环境表现
6. ⬜ 优化 prompt 和参数
7. ⬜ 记录成本和性能数据

---

## 参考资源

- [Anthropic API 文档](https://docs.anthropic.com/)
- [LangChain Anthropic 集成](https://python.langchain.com/docs/integrations/chat/anthropic)
- [Claude 模型对比](https://docs.anthropic.com/en/docs/models-overview)
- [Extended Thinking 文档](https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking)

---

## 联系支持

如有问题，请：
1. 查看本文档的常见问题部分
2. 查阅 Anthropic 官方文档
3. 提交 GitHub Issue
4. 联系团队技术支持
