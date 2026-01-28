# 使用指南

本文档详细介绍如何使用通用AI开发工具集。

## 环境设置

### 1. 安装依赖

```bash
pip install anthropic requests pytest
```

### 2. 配置API密钥

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

或在代码中直接传入:

```python
skill = CodeSkill(api_key="your-api-key")
```

## Skills详细使用

### /code Skill

完整的需求到代码工作流。

#### 基本使用

```python
from skills.code_skill import CodeSkill

skill = CodeSkill(
    api_key="your-api-key",
    project_path="./my_project"
)

result = skill.execute(
    requirement="开发一个用户登录注册功能,支持邮箱和手机号登录",
    mode="auto"
)

if result["success"]:
    print("生成的文件:")
    for file in result["results"]["generated_files"]:
        print(f"  - {file}")
```

#### 参数说明

- `requirement`: 需求描述(必需)
- `mode`: 执行模式
  - `auto`: 全自动模式,无需人工干预
  - `semi-auto`: 半自动模式,关键步骤需要确认
  - `manual`: 手动模式,每步都需要确认
- `from_feishu`: 飞书文档URL(可选)
- `project_path`: 项目路径(可选,默认当前目录)

#### 输出结果

```python
{
    "success": True,
    "results": {
        "requirement": {...},      # 结构化需求
        "architecture": {...},     # 架构设计
        "api_spec": {...},        # API规范
        "task_plan": {...},       # 任务计划
        "generated_files": [...], # 生成的文件列表
        "review": {...}           # 代码审查报告
    }
}
```

### /design Skill

仅执行设计阶段。

#### 基本使用

```python
from skills.design_skill import DesignSkill

skill = DesignSkill(api_key="your-api-key")

result = skill.execute(
    requirement="开发一个电商平台的订单管理系统"
)

if result["success"]:
    print("设计文档已保存到 docs/ 目录")
```

#### 输出文件

- `docs/requirement.json`: 结构化需求文档
- `docs/architecture.json`: 架构设计文档
- `docs/api_spec.json`: API规范(OpenAPI格式)

### /review Skill

审查现有代码。

#### 基本使用

```python
from skills.review_skill import ReviewSkill

skill = ReviewSkill(api_key="your-api-key")

# 审查指定文件
result = skill.execute(
    files=["src/main.py", "src/utils.py"],
    requirement_path="docs/requirement.json"
)

# 审查所有Python文件
result = skill.execute()

if result["success"]:
    review = result["review"]
    print(f"总体评分: {review['overall_score']}/100")
    print(f"发现问题: {len(review['issues'])}个")
```

#### 审查报告内容

```python
{
    "overall_score": 85,
    "summary": "代码整体质量良好...",
    "strengths": ["清晰的代码结构", "良好的错误处理"],
    "issues": [
        {
            "severity": "high",
            "category": "security",
            "file": "src/auth.py",
            "line": 42,
            "description": "密码未加密存储",
            "suggestion": "使用bcrypt加密密码"
        }
    ],
    "security_concerns": [...],
    "performance_concerns": [...],
    "test_coverage": {
        "score": 80,
        "missing_tests": [...]
    },
    "recommendations": [...]
}
```

### /refactor Skill

重构现有代码。

#### 基本使用

```python
from skills.refactor_skill import RefactorSkill

skill = RefactorSkill(api_key="your-api-key")

result = skill.execute(
    files=["src/legacy_module.py"],
    refactor_goal="将代码重构为面向对象设计,提高可维护性"
)

if result["success"]:
    print(f"成功重构 {result['refactored_files']} 个文件")
```

## MCP Servers使用

### Filesystem Server

```python
from mcp_servers.filesystem_server import FilesystemMCPServer

fs = FilesystemMCPServer(base_path="./project")

# 写入文件
fs.fs_write("src/main.py", "print('Hello')")

# 读取文件
result = fs.fs_read("src/main.py")
print(result["content"])

# 列出目录
result = fs.fs_list("src")
for item in result["items"]:
    print(f"{item['name']} ({item['type']})")

# 创建目录
fs.fs_create_dir("src/utils")
```

### Git Server

```python
from mcp_servers.git_server import GitMCPServer

git = GitMCPServer(repo_path="./project")

# 初始化仓库
git.git_init()

# 添加文件
git.git_add(["src/main.py"])

# 提交
git.git_commit("Initial commit")

# 查看状态
result = git.git_status()
print(result["output"])
```

### CLI Server

```python
from mcp_servers.cli_server import CLIMCPServer

cli = CLIMCPServer(working_dir="./project")

# 执行命令
result = cli.cli_execute("python --version")
print(result["output"])

# 运行测试
result = cli.cli_run_tests("pytest tests/")

# 构建项目
result = cli.cli_build("python setup.py build")
```

## Agents使用

### Requirement Analyst

```python
from agents.requirement_analyst import RequirementAnalyst

analyst = RequirementAnalyst(api_key="your-api-key")

result = analyst.analyze(
    requirement="开发一个博客系统,支持文章发布、评论、标签"
)

if result["success"]:
    req = result["requirement"]
    print(f"项目类型: {req['type']}")
    print(f"功能数量: {len(req['features'])}")
```

### System Architect

```python
from agents.system_architect import SystemArchitect

architect = SystemArchitect(api_key="your-api-key")

result = architect.design(requirement)

if result["success"]:
    arch = result["architecture"]
    print(f"技术栈: {arch['tech_stack']}")
```

### Code Generator

```python
from agents.code_generator import CodeGenerator

generator = CodeGenerator(api_key="your-api-key")

task = {
    "title": "实现用户认证",
    "description": "实现JWT认证功能",
    "files_to_create": [...]
}

result = generator.generate(task, context)

if result["success"]:
    for file_info in result["code"]["files"]:
        print(f"生成: {file_info['path']}")
```

## 最佳实践

### 1. 需求描述

提供清晰、详细的需求描述:

```python
requirement = """
开发一个任务管理系统,包含以下功能:

1. 用户管理
   - 用户注册、登录
   - 用户权限管理(管理员、普通用户)

2. 任务管理
   - 创建、编辑、删除任务
   - 任务状态跟踪(待办、进行中、已完成)
   - 任务优先级设置

3. 团队协作
   - 任务分配
   - 评论功能
   - 通知提醒

技术要求:
- 后端: Python + FastAPI
- 数据库: PostgreSQL
- 前端: React
"""
```

### 2. 分阶段执行

对于大型项目,建议分阶段执行:

```python
# 阶段1: 设计
design_skill = DesignSkill(api_key="your-api-key")
design_result = design_skill.execute(requirement)

# 审查设计文档...

# 阶段2: 代码生成
code_skill = CodeSkill(api_key="your-api-key")
code_result = code_skill.execute(requirement, mode="semi-auto")

# 阶段3: 代码审查
review_skill = ReviewSkill(api_key="your-api-key")
review_result = review_skill.execute()
```

### 3. 代码审查

生成代码后,务必进行审查:

```python
review_skill = ReviewSkill(api_key="your-api-key")
result = review_skill.execute(
    requirement_path="docs/requirement.json"
)

# 检查关键问题
review = result["review"]
critical_issues = [
    i for i in review["issues"]
    if i["severity"] == "critical"
]

if critical_issues:
    print("发现严重问题,需要修复!")
    for issue in critical_issues:
        print(f"  - {issue['description']}")
```

## 故障排除

### API密钥错误

```
Error: Invalid API key
```

解决方案: 检查环境变量或传入的API密钥是否正确。

### 生成代码失败

```
Error: Failed to generate code
```

解决方案:
1. 检查需求描述是否清晰
2. 尝试简化需求
3. 使用`mode="semi-auto"`逐步执行

### 文件写入失败

```
Error: Failed to write file
```

解决方案:
1. 检查目录权限
2. 确保目标目录存在
3. 检查磁盘空间

## 更多示例

查看 `examples/` 目录获取更多使用示例。
