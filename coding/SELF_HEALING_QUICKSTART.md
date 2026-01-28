# 自愈功能快速开始

## 🚀 立即使用

### 在 Web UI 中使用（推荐）

1. **启动 UI**
   ```bash
   python run_ui.py
   ```

2. **启用自愈功能**
   - 在侧边栏找到 "🔧 Self-Healing" 部分
   - 勾选 "Enable Self-Healing"
   - 设置最大重试次数（推荐 3 次）

3. **正常使用**
   - 输入需求
   - 点击"生成代码"
   - 系统会自动处理错误并重试

4. **查看结果**
   - 成功后会显示修复摘要（如果有重试）
   - 失败后会显示详细的修复尝试记录
   - 修复日志保存在 `项目目录/docs/fix_log.json`

## 📊 示例输出

### 成功场景
```
[ATTEMPT 1] Starting workflow...
[ERROR] Workflow failed at stage4: Failed to parse JSON
[FIX] Error Type: parsing
[FIX] Strategy: Improved JSON extraction
[RETRY] Attempting to fix and retry...

[ATTEMPT 2] Starting workflow...
[SUCCESS] Workflow succeeded after 2 attempt(s)

Fix Summary: Fix Attempts: 1 | Successful: 1 | Failed: 0 | Success Rate: 100.0%
```

### 失败场景
```
[ATTEMPT 1] Starting workflow...
[ERROR] API rate limit exceeded

[ATTEMPT 2] Starting workflow...
[ERROR] API rate limit exceeded

[ATTEMPT 3] Starting workflow...
[ERROR] API rate limit exceeded

[FAILED] Max retries (3) reached

Fix Summary: Fix Attempts: 3 | Successful: 0 | Failed: 3 | Success Rate: 0.0%
```

## 🔧 在代码中使用

```python
from skills.self_healing_skill import SelfHealingSkill

# 初始化
skill = SelfHealingSkill(
    api_key="your-api-key",
    project_path="./my_project",
    max_retries=3
)

# 执行
result = skill.execute(
    requirement="你的需求",
    review_mode="auto"
)

# 检查结果
if result["success"]:
    print(f"✅ 成功！评分: {result['final_score']}/100")
    if result.get("fix_summary"):
        print(f"🔧 {result['fix_summary']}")
else:
    print(f"❌ 失败: {result['error']}")
    if result.get("fix_summary"):
        print(f"🔧 {result['fix_summary']}")
```

## 📝 查看修复日志

修复日志保存在 `项目目录/docs/fix_log.json`：

```bash
# 查看日志
cat ./generated_project/docs/fix_log.json

# 或在 Python 中
import json
with open("./generated_project/docs/fix_log.json") as f:
    log = json.load(f)
    print(json.dumps(log, indent=2))
```

## ⚙️ 配置建议

| 项目类型 | 推荐重试次数 | 原因 |
|---------|------------|------|
| 简单项目 | 2-3 次 | 快速失败，节省时间 |
| 中等项目 | 3 次（默认） | 平衡成功率和时间 |
| 复杂项目 | 4-5 次 | 提高成功率 |
| 测试/实验 | 1-2 次 | 快速验证 |

## 🎯 最佳实践

1. **首次使用建议**
   - 从简单需求开始测试
   - 观察修复日志了解常见错误
   - 逐步增加需求复杂度

2. **需求描述优化**
   - 清晰具体的需求描述可以减少错误
   - 避免过于复杂的单个需求
   - 分阶段描述大型项目

3. **监控和调整**
   - 查看修复摘要了解成功率
   - 成功率低于 50% 时考虑简化需求
   - 记录常见错误模式

## 🐛 故障排除

### 问题: 一直重试但都失败

**可能原因**:
- API key 无效
- 网络问题
- 需求过于复杂

**解决方案**:
1. 检查 API key 是否有效
2. 检查网络连接
3. 简化需求描述
4. 查看 fix_log.json 了解具体错误

### 问题: 自愈功能没有生效

**检查**:
- 是否勾选了 "Enable Self-Healing"
- 是否设置了合理的重试次数
- 查看日志确认是否有错误发生

## 📚 更多信息

- 完整文档: `docs/SELF_HEALING_SKILL.md`
- 测试脚本: `python test_self_healing.py`
- UI 文档: `UI_README.md`

## 🔮 未来功能

Phase 2 和 Phase 3 将带来：
- AI 驱动的错误分析
- 智能修复方案生成
- 自动应用修复
- 学习历史经验

敬请期待！
