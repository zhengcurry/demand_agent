# 任务规划阶段失败 - 诊断和解决方案

## 🐛 问题描述

执行到第四步（任务规划）时报错：
```
Workflow failed: Task planning failed
```

## 🔍 可能的原因

### 1. API 调用超时
任务规划阶段需要处理大量数据（需求+架构+API规范），可能导致：
- API 调用时间过长
- 响应超时

### 2. 输入数据过大
如果前面阶段生成的数据太详细，可能导致：
- Token 数量超限
- 处理时间过长

### 3. JSON 解析问题
虽然已经修复了 markdown 代码块问题，但可能还有其他格式问题。

## 🛠️ 临时解决方案

### 方案1: 使用原版 CodeSkill（推荐）

原版 CodeSkill 更稳定，虽然没有分阶段报告，但功能完整：

```bash
cd coding
python test_simple.py
```

或使用命令行：
```bash
python main.py code "你的需求" --mode auto
```

### 方案2: 简化需求

使用更简单的需求描述，减少数据量：

```python
requirement = """
开发一个简单的API:
- 功能: 加法运算
- 技术: Python + FastAPI
"""
```

### 方案3: 增加超时时间

修改 `agents/task_planner.py`，增加 max_tokens 和超时：

```python
response = self.client.messages.create(
    model=self.model,
    max_tokens=12000,  # 增加到 12000
    temperature=self.temperature,
    messages=[{"role": "user", "content": prompt}],
    timeout=120.0  # 增加超时到 120 秒
)
```

## 🔬 诊断步骤

### 步骤1: 测试单个 Agent

```bash
cd coding

# 测试 TaskPlanner
python debug_planner.py
```

如果成功，说明 TaskPlanner 本身没问题。

### 步骤2: 测试完整流程

```bash
# 测试各阶段
python test_stages.py
```

这会逐个测试每个阶段，找出具体哪个阶段有问题。

### 步骤3: 查看详细错误

运行增强版测试，查看详细错误信息：

```bash
python test_enhanced_skill.py 2>&1 | tee test_output.log
```

然后查看日志：
```bash
cat test_output.log
```

## 📊 已知工作的配置

### 配置1: 原版 CodeSkill
- **文件**: `skills/code_skill.py`
- **特点**: 稳定，功能完整
- **缺点**: 没有分阶段报告

### 配置2: 简化需求
- **需求长度**: < 200 字
- **功能数量**: 1-3 个
- **技术栈**: 明确指定

## 🚀 推荐使用方式

### 对于生产使用

使用原版 CodeSkill：

```python
from skills.code_skill import CodeSkill
import os

skill = CodeSkill(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    project_path="./my_project"
)

result = skill.execute(
    requirement="你的需求",
    mode="auto"
)
```

### 对于学习和研究

使用增强版，但简化需求：

```python
from skills.enhanced_code_skill import EnhancedCodeSkill
import os

skill = EnhancedCodeSkill(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    project_path="./my_project"
)

# 使用简单需求
simple_requirement = """
开发一个计算器API:
- 加法功能
- Python + FastAPI
"""

result = skill.execute(
    requirement=simple_requirement,
    review_mode="auto",
    pause_for_review=False
)
```

## 🔧 正在进行的修复

我正在：
1. ✅ 添加详细的错误日志
2. 🔄 测试各个阶段独立运行
3. 🔄 优化 TaskPlanner 的输入数据
4. 🔄 增加超时和重试机制

## 📝 下一步行动

### 立即可用
```bash
# 使用原版（稳定）
cd coding
python test_simple.py
```

### 等待修复
我正在后台运行测试，找出具体问题。完成后会提供完整的修复方案。

### 手动诊断
如果你想自己诊断：

```bash
cd coding

# 1. 测试各个 Agent
python debug_test.py          # RequirementAnalyst
python debug_architect.py     # SystemArchitect
python debug_planner.py       # TaskPlanner

# 2. 测试完整流程
python test_stages.py         # 逐阶段测试

# 3. 查看生成的报告
ls test_*/docs/               # 查看已生成的报告
```

## 💡 建议

1. **短期**: 使用原版 CodeSkill，它更稳定
2. **中期**: 等待增强版的修复和优化
3. **长期**: 增强版会提供更好的可控性和报告

## 📞 需要帮助？

如果问题持续，请提供：
1. 你使用的需求描述
2. 错误信息的完整输出
3. 运行 `python test_stages.py` 的结果

我会根据具体情况提供针对性的解决方案。
