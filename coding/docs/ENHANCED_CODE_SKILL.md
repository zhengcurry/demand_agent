# Enhanced Code Skill - 完整指南

## 概述

Enhanced Code Skill 是一个**增强版的自动化开发流水线**，在原有基础上增加了：

- ✅ **分阶段执行**：6个明确的阶段，每个阶段独立可控
- 📊 **详细报告**：每个阶段都生成独立的报告文件
- 🔍 **审核检查点**：支持人工审核或自动审核
- ⏸️ **暂停/恢复**：可在设计阶段后暂停，等待人工审核
- 📈 **进度跟踪**：完整的工作流状态追踪

## 工作流程

```
输入需求
  ↓
📋 阶段1: 需求分析
  └─ 输出: stage1_requirement_report.json
  ↓
🏗️ 阶段2: 设计阶段 (架构 + API)
  └─ 输出: stage2_design_report.json
  ↓
🔍 阶段3: 设计审核 (人工/自动)
  └─ 输出: stage3_design_review_report.json
  ↓
📝 阶段4: 任务拆解
  └─ 输出: stage4_task_planning_report.json
  ↓
💻 阶段5: 代码生成
  └─ 输出: stage5_code_generation_report.json
  ↓
✅ 阶段6: 代码审查
  └─ 输出: stage6_code_review_report.json
  ↓
📄 完整报告: complete_workflow_report.json
```

## 使用方法

### 方式1: 完全自动化（推荐快速开发）

```python
from skills.enhanced_code_skill import EnhancedCodeSkill

skill = EnhancedCodeSkill(
    api_key="your-api-key",
    project_path="./my_project"
)

result = skill.execute(
    requirement="你的需求描述",
    review_mode="auto",          # 自动审核
    pause_for_review=False       # 不暂停
)

if result["success"]:
    print(f"完成! 代码质量评分: {result['final_score']}/100")
    print(f"生成文件: {len(result['generated_files'])} 个")
```

**特点**:
- 一次性执行所有6个阶段
- 自动审核设计文档
- 无需人工干预
- 适合：快速原型开发、实验性项目

### 方式2: 人工审核模式（推荐生产项目）

```python
skill = EnhancedCodeSkill(
    api_key="your-api-key",
    project_path="./my_project"
)

result = skill.execute(
    requirement="你的需求描述",
    review_mode="manual",        # 人工审核
    pause_for_review=True        # 在设计阶段后暂停
)

if result.get("status") == "paused_for_review":
    print(f"工作流已暂停，等待审核")
    print(f"检查点保存在: {result['checkpoint_path']}")

    # 人工审核设计文档...
    # 审核通过后，可以继续执行后续阶段
```

**特点**:
- 在设计完成后暂停
- 等待人工审核架构和API设计
- 审核通过后可继续执行
- 适合：生产环境项目、关键系统

### 方式3: 命令行使用

```bash
# 自动模式
python main.py enhanced-code "开发一个用户系统" --mode auto

# 人工审核模式
python main.py enhanced-code "开发一个支付系统" --mode manual --pause-for-review
```

## 生成的报告

### 1. 需求分析报告 (stage1_requirement_report.json)

```json
{
  "stage": "requirement_analysis",
  "status": "completed",
  "timestamp": "2024-01-28T10:00:00",
  "input": "原始需求描述",
  "output": {
    "type": "feature",
    "complexity": "medium",
    "estimated_tasks": 8
  },
  "summary": {
    "requirement_type": "feature",
    "complexity": "medium",
    "estimated_tasks": 8
  }
}
```

**包含信息**:
- 需求类型（功能/优化/修复等）
- 复杂度评估
- 预估任务数量

### 2. 设计报告 (stage2_design_report.json)

```json
{
  "stage": "design",
  "status": "completed",
  "timestamp": "2024-01-28T10:05:00",
  "architecture": {
    "components": [...],
    "data_models": [...],
    "tech_stack": {...}
  },
  "api_spec": {
    "endpoints": [...],
    "authentication": {...}
  },
  "summary": {
    "components": 5,
    "endpoints": 12,
    "data_models": 3
  }
}
```

**包含信息**:
- 系统架构设计
- 组件列表
- 数据模型
- API端点规范

### 3. 设计审核报告 (stage3_design_review_report.json)

```json
{
  "stage": "design_review",
  "status": "completed",
  "timestamp": "2024-01-28T10:10:00",
  "review_mode": "auto",
  "review_result": {
    "passed": true,
    "issues": [],
    "suggestions": [...]
  },
  "summary": {
    "review_passed": true,
    "total_issues": 0,
    "critical_issues": 0,
    "suggestions": 2
  }
}
```

**包含信息**:
- 审核结果（通过/失败）
- 发现的问题（按严重程度）
- 改进建议

### 4. 任务拆解报告 (stage4_task_planning_report.json)

```json
{
  "stage": "task_planning",
  "status": "completed",
  "timestamp": "2024-01-28T10:15:00",
  "task_plan": {
    "tasks": [
      {
        "id": "task-1",
        "title": "实现用户模型",
        "type": "model",
        "priority": "high"
      },
      ...
    ]
  },
  "summary": {
    "total_tasks": 8,
    "task_breakdown": {
      "model": 2,
      "api": 3,
      "service": 2,
      "test": 1
    }
  }
}
```

**包含信息**:
- 详细任务列表
- 任务类型分布
- 优先级排序

### 5. 代码生成报告 (stage5_code_generation_report.json)

```json
{
  "stage": "code_generation",
  "status": "completed",
  "timestamp": "2024-01-28T10:30:00",
  "generated_files": [
    "src/models/user.py",
    "src/api/auth.py",
    "tests/test_auth.py",
    ...
  ],
  "summary": {
    "total_tasks": 8,
    "completed_tasks": 8,
    "failed_tasks": 0,
    "total_files": 15,
    "success_rate": "100.0%"
  }
}
```

**包含信息**:
- 生成的文件列表
- 任务完成情况
- 成功率统计

### 6. 代码审查报告 (stage6_code_review_report.json)

```json
{
  "stage": "code_review",
  "status": "completed",
  "timestamp": "2024-01-28T10:40:00",
  "review": {
    "overall_score": 85,
    "issues": [
      {
        "severity": "medium",
        "file": "src/api/auth.py",
        "line": 42,
        "message": "Missing error handling"
      }
    ],
    "suggestions": [...]
  },
  "summary": {
    "overall_score": 85,
    "total_issues": 3,
    "critical_issues": 0,
    "quality_level": "Good"
  }
}
```

**包含信息**:
- 整体代码质量评分
- 发现的问题列表
- 改进建议
- 质量等级

### 7. 完整工作流报告 (complete_workflow_report.json)

```json
{
  "workflow_status": "completed",
  "timestamp": "2024-01-28T10:40:00",
  "stages_completed": [
    "stage1",
    "stage2",
    "stage3",
    "stage4",
    "stage5",
    "stage6"
  ],
  "reports": {
    "stage1_requirement": {...},
    "stage2_design": {...},
    "stage3_design_review": {...},
    "stage4_task_planning": {...},
    "stage5_code_generation": {...},
    "stage6_code_review": {...}
  }
}
```

**包含信息**:
- 工作流整体状态
- 所有阶段的完整报告

## 质量评分标准

- **90-100**: Excellent (优秀) - 生产就绪
- **80-89**: Good (良好) - 小幅改进后可用
- **70-79**: Acceptable (可接受) - 需要一些改进
- **60-69**: Needs Improvement (需改进) - 有明显问题
- **<60**: Poor (较差) - 需要重构

## 实际使用场景

### 场景1: 快速原型开发

```python
# 完全自动化，快速验证想法
skill = EnhancedCodeSkill(api_key=api_key, project_path="./prototype")
result = skill.execute(
    requirement="开发一个简单的待办事项应用",
    review_mode="auto",
    pause_for_review=False
)
```

### 场景2: 生产项目开发

```python
# 在设计阶段暂停，人工审核后继续
skill = EnhancedCodeSkill(api_key=api_key, project_path="./production_app")
result = skill.execute(
    requirement="开发一个电商支付系统",
    review_mode="manual",
    pause_for_review=True
)

# 审核设计文档...
# 确认无误后继续
```

### 场景3: 学习和研究

```python
# 执行完整流程，学习每个阶段的输出
skill = EnhancedCodeSkill(api_key=api_key, project_path="./learning")
result = skill.execute(
    requirement="开发一个RESTful API",
    review_mode="auto",
    pause_for_review=False
)

# 查看所有报告，学习设计和实现过程
```

## 运行示例

```bash
cd coding

# 运行交互式示例
python examples/example_enhanced_code_skill.py

# 选项:
# 1 - 完全自动化工作流
# 2 - 带人工审核检查点
# 3 - 查看详细报告
# all - 运行所有示例
```

## 与原版的区别

| 特性 | 原版 CodeSkill | Enhanced CodeSkill |
|------|---------------|-------------------|
| 阶段报告 | 仅最终报告 | 每阶段独立报告 |
| 审核检查点 | 无 | 支持暂停等待审核 |
| 审核模式 | 仅自动 | 自动/人工可选 |
| 进度跟踪 | 基本 | 详细的状态追踪 |
| 报告格式 | 简单JSON | 结构化+摘要 |
| 工作流控制 | 一次性执行 | 可暂停/恢复 |

## 最佳实践

1. **原型开发**: 使用 `auto` + `pause_for_review=False`
2. **生产项目**: 使用 `manual` + `pause_for_review=True`
3. **团队协作**: 使用人工审核模式，设计阶段团队评审
4. **持续集成**: 使用自动审核模式，集成到CI/CD流程
5. **学习研究**: 查看所有阶段报告，理解完整流程

## 故障排查

### 问题: 设计审核未通过

```python
# 查看审核报告
import json
with open('docs/stage3_design_review_report.json') as f:
    report = json.load(f)
    print(report['review_result']['issues'])
```

### 问题: 代码质量评分低

```python
# 查看代码审查报告
with open('docs/stage6_code_review_report.json') as f:
    report = json.load(f)
    for issue in report['review']['issues']:
        print(f"{issue['severity']}: {issue['message']}")
```

## 未来扩展

- [ ] 支持从检查点恢复
- [ ] 集成代码格式化工具
- [ ] 支持多轮迭代优化
- [ ] 集成静态代码分析
- [ ] 支持自定义审核规则
