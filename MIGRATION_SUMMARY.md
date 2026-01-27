# 从扣子平台迁移到 Claude - 变更总结

## 完成时间
2026-01-27

## 变更概述

本次迁移将三层AI Agent系统从扣子（Coze）平台的豆包（Doubao）模型迁移到 Anthropic Claude。

---

## 主要变更文件

### 1. Agent 代码 (已修改)
- ✅ `src/agents/agent1_requirement_clarifier.py`
- ✅ `src/agents/agent2_prd_builder.py`
- ✅ `src/agents/agent3_prototype_assistant.py`

**变更内容**：
- 将 `ChatOpenAI` 替换为 `ChatAnthropic`
- 移除扣子平台特定依赖 (`coze_coding_utils`)
- 修改环境变量从 `COZE_*` 改为 `ANTHROPIC_API_KEY`
- 调整 Extended Thinking 配置方式

### 2. 配置文件 (已修改)
- ✅ `config/agent1_config.json`
- ✅ `config/agent2_config.json`
- ✅ `config/agent3_config.json`

**变更内容**：
- 模型ID: `doubao-seed-1-6-thinking-250715` → `claude-sonnet-4-5`

### 3. 文档文件 (已更新)
- ✅ `README.md` - 更新技术栈说明
- ✅ `CLAUDE.md` - 更新项目指南
- ✅ `docs/MIGRATION_TO_CLAUDE.md` - 新建迁移指南

### 4. 脚本文件 (已创建)
- ✅ `scripts/setup_env.sh` - Linux/Mac 环境配置脚本
- ✅ `scripts/setup_env.bat` - Windows 环境配置脚本
- ⚠️  `scripts/load_env.py` - 保留但不再使用（扣子平台专用）

---

## 环境变量变更

### 迁移前 (Coze)
```bash
COZE_WORKSPACE_PATH=/workspace/projects
COZE_WORKLOAD_IDENTITY_API_KEY=xxx
COZE_INTEGRATION_MODEL_BASE_URL=xxx
```

### 迁移后 (Claude)
```bash
WORKSPACE_PATH=/path/to/project
ANTHROPIC_API_KEY=your-api-key
```

---

## 依赖包变更

### 新增依赖
```txt
anthropic>=0.40.0
langchain-anthropic>=0.3.0
```

### 移除依赖（可选）
```txt
coze-coding-utils
coze-workload-identity
cozeloop
```

**注意**：如果项目中有其他功能依赖这些包，请不要移除。

---

## 代码变更详情

### ChatOpenAI → ChatAnthropic

**迁移前**：
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="doubao-seed-1-6-thinking-250715",
    api_key=os.getenv("COZE_WORKLOAD_IDENTITY_API_KEY"),
    base_url=os.getenv("COZE_INTEGRATION_MODEL_BASE_URL"),
    temperature=0.7,
    streaming=True,
    timeout=600,
    extra_body={"thinking": {"type": "enabled"}},
    default_headers=default_headers(ctx) if ctx else {}
)
```

**迁移后**：
```python
from langchain_anthropic import ChatAnthropic

api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise ValueError("ANTHROPIC_API_KEY environment variable is required")

llm_kwargs = {
    "model": "claude-sonnet-4-5",
    "api_key": api_key,
    "temperature": 0.7,
    "max_tokens": 8000,
    "timeout": 600,
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

### 主要差异：
1. ❌ 不再需要 `base_url`（Claude 使用官方 API）
2. ❌ 不再需要 `streaming` 参数（LangChain 自动处理）
3. ❌ 不再需要 `default_headers`（Claude 不需要）
4. ✅ `max_completion_tokens` → `max_tokens`
5. ✅ Thinking 配置方式变更

---

## 测试验证

### 快速测试
```bash
# 设置环境变量
export WORKSPACE_PATH=$(pwd)
export ANTHROPIC_API_KEY="your-api-key"

# 运行测试
python tests/simple_test.py
```

### 完整测试
```bash
python tests/test_complete_workflow.py
```

---

## 回滚方案

如需回滚到扣子平台：

```bash
# 1. 恢复代码
git checkout HEAD~1 -- src/agents/
git checkout HEAD~1 -- config/

# 2. 恢复环境变量
export COZE_WORKSPACE_PATH=/workspace/projects
export COZE_WORKLOAD_IDENTITY_API_KEY="your-key"
export COZE_INTEGRATION_MODEL_BASE_URL="your-url"

# 3. 卸载 Claude 依赖（可选）
pip uninstall anthropic langchain-anthropic
```

---

## 下一步行动

### 立即执行
- [x] 完成代码迁移
- [x] 更新配置文件
- [x] 更新文档
- [ ] 获取 Anthropic API Key
- [ ] 设置环境变量
- [ ] 运行测试验证

### 后续优化
- [ ] 监控生产环境表现
- [ ] 优化 prompt 和参数
- [ ] 记录成本和性能数据
- [ ] 根据实际情况调整模型选择
- [ ] 考虑是否开启 Extended Thinking

---

## 注意事项

### 1. API Key 安全
- ❌ 不要将 API Key 提交到代码仓库
- ✅ 使用环境变量或密钥管理服务
- ✅ 将 `.env` 文件添加到 `.gitignore`

### 2. 成本控制
- Claude 与豆包的定价不同，建议：
  - 使用 `claude-sonnet-4-5` 而非 Opus（成本更低）
  - 合理设置 `max_tokens` 避免浪费
  - 监控 API 使用量
  - 只在必要时开启 Extended Thinking

### 3. 性能差异
- Claude Sonnet 4.5 在大多数任务上性能优于豆包
- Extended Thinking 会增加响应时间但提升质量
- 根据实际需求选择合适的模型

### 4. 兼容性
- 所有原有的工作流逻辑保持不变
- Agent 之间的数据传递方式不变
- 记忆管理和状态保存机制不变

---

## 支持资源

- [迁移完整指南](docs/MIGRATION_TO_CLAUDE.md)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [LangChain Anthropic 集成](https://python.langchain.com/docs/integrations/chat/anthropic)
- [Claude 模型对比](https://docs.anthropic.com/en/docs/models-overview)

---

## 变更记录

| 日期 | 变更人 | 变更内容 |
|------|--------|----------|
| 2026-01-27 | Claude | 完成从扣子到 Claude 的迁移 |

---

**迁移完成！如有问题，请查阅 `docs/MIGRATION_TO_CLAUDE.md` 或提交 Issue。**
