# Self-Healing Skill 自愈技能

## 概述

Self-Healing Skill 是对 Enhanced Code Skill 的增强包装，提供自动错误恢复和重试功能。当工作流执行过程中遇到错误时，系统会自动分析错误类型，应用相应的修复策略，并重试失败的操作。

## 功能特性

### ✅ Phase 1 - 基础版本（已实现）

1. **自动错误捕获**
   - 捕获所有阶段的异常和错误
   - 详细记录错误上下文和堆栈信息

2. **智能错误分类**
   - JSON 解析错误
   - API 调用错误
   - 网络错误
   - 超时错误
   - 文件操作错误
   - 验证错误
   - 代码生成错误

3. **自动重试机制**
   - 可配置的最大重试次数（默认 3 次）
   - 每次重试前应用修复策略
   - 重试间隔延迟

4. **详细修复日志**
   - 记录每次错误和修复尝试
   - 生成修复报告（JSON 格式）
   - 统计成功率和失败率

### 🚧 Phase 2 - 智能分析（计划中）

- AI 驱动的错误分析
- 错误模式识别
- 智能修复建议生成

### 🚧 Phase 3 - 自动修复（计划中）

- 自动应用修复方案
- 修复验证机制
- 学习历史修复经验

## 使用方法

### 方法 1: 在代码中使用

```python
from skills.self_healing_skill import SelfHealingSkill

# 初始化
skill = SelfHealingSkill(
    api_key="your-api-key",
    project_path="./my_project",
    max_retries=3  # 最大重试次数
)

# 执行工作流
result = skill.execute(
    requirement="你的需求描述",
    review_mode="auto",
    pause_for_review=False
)

# 检查结果
if result["success"]:
    print(f"成功！评分: {result['final_score']}/100")
    if result.get("fix_summary"):
        print(f"修复摘要: {result['fix_summary']}")
else:
    print(f"失败: {result['error']}")
```

### 方法 2: 在 Web UI 中使用

1. 启动 UI: `python run_ui.py`
2. 在侧边栏勾选 "Enable Self-Healing"
3. 设置最大重试次数（1-5）
4. 正常输入需求并生成代码

## 错误类型和修复策略

| 错误类型 | 修复策略 |
|---------|---------|
| JSON 解析错误 | 改进 JSON 提取逻辑 |
| API 错误 | 指数退避重试 |
| 网络错误 | 等待网络恢复后重试 |
| 超时错误 | 增加超时时间重试 |
| 代码生成错误 | 简化任务分解 |
| 验证错误 | 放宽验证规则 |
| 文件错误 | 确保目录存在 |

## 修复日志

修复日志保存在 `项目目录/docs/fix_log.json`，包含：

```json
{
  "fix_records": [
    {
      "stage": "stage4_task_planning",
      "attempt": 1,
      "timestamp": "2026-01-28T20:00:00Z",
      "error": {
        "error_type": "parsing",
        "error_message": "Failed to parse JSON",
        "exception_type": "JSONDecodeError"
      },
      "fix_strategy": "Improved JSON extraction",
      "status": "success",
      "resolved_at": "2026-01-28T20:00:05Z"
    }
  ],
  "summary": {
    "total_attempts": 1,
    "successful_fixes": 1,
    "failed_fixes": 0,
    "success_rate": "100.0%"
  }
}
```

## 配置选项

### max_retries
- **类型**: int
- **默认值**: 3
- **范围**: 1-5
- **说明**: 每个阶段的最大重试次数

### 重试策略
当前实现的重试策略：
1. 记录错误上下文
2. 分类错误类型
3. 应用对应的修复策略
4. 等待 2 秒
5. 重试操作

## 示例场景

### 场景 1: JSON 解析错误自动修复

```
[ATTEMPT 1] Starting workflow...
[ERROR] Workflow failed at stage4_task_planning: Failed to parse JSON
[FIX] Error Type: parsing
[FIX] Strategy: Improved JSON extraction
[FIX] Applying strategy: Improved JSON extraction
[FIX] Strategy applied, ready to retry

[ATTEMPT 2] Starting workflow...
[SUCCESS] Workflow succeeded after 2 attempt(s)
```

### 场景 2: 达到最大重试次数

```
[ATTEMPT 1] Starting workflow...
[ERROR] Workflow failed: API rate limit exceeded

[ATTEMPT 2] Starting workflow...
[ERROR] Workflow failed: API rate limit exceeded

[ATTEMPT 3] Starting workflow...
[ERROR] Workflow failed: API rate limit exceeded

[FAILED] Max retries (3) reached
```

## 最佳实践

1. **合理设置重试次数**
   - 简单项目: 2-3 次
   - 复杂项目: 3-5 次

2. **查看修复日志**
   - 了解常见错误模式
   - 优化需求描述

3. **结合手动审查**
   - 对于关键项目，启用 pause_for_review
   - 在设计阶段人工检查

4. **监控成功率**
   - 查看 fix_summary 了解修复效果
   - 成功率低于 50% 时考虑调整需求

## 限制和注意事项

### 当前限制（Phase 1）
- ⚠️ 不会修改提示词或参数
- ⚠️ 不会自动调整模型设置
- ⚠️ 某些错误无法自动修复（如 API key 错误）

### 无法自动修复的错误
- API key 无效或缺失
- 网络完全断开
- 磁盘空间不足
- 权限不足

### 建议
- 确保 API key 有效
- 确保网络连接稳定
- 确保有足够的磁盘空间
- 确保项目目录有写入权限

## 测试

运行测试脚本：

```bash
python test_self_healing.py
```

## 未来计划

### Phase 2: 智能分析
- [ ] ErrorAnalyzer agent
- [ ] 错误模式识别
- [ ] 智能修复建议

### Phase 3: 自动修复
- [ ] AutoFixer agent
- [ ] 修复验证机制
- [ ] 学习历史经验

## 技术架构

```
SelfHealingSkill
├── EnhancedCodeSkill (基础工作流)
├── ErrorContext (错误上下文)
│   ├── 错误分类
│   └── 上下文捕获
├── FixLogger (修复日志)
│   ├── 记录尝试
│   ├── 记录结果
│   └── 生成报告
└── 重试逻辑
    ├── 最大重试次数
    ├── 修复策略
    └── 延迟重试
```

## 贡献

欢迎贡献新的修复策略和错误处理逻辑！

## 许可证

与主项目相同
