# API文档

本文档详细说明各组件的API接口。

## MCP Servers

### FilesystemMCPServer

文件系统操作服务器。

#### 初始化

```python
FilesystemMCPServer(base_path: str = None)
```

**参数**:
- `base_path`: 基础路径(默认为当前目录)

#### 方法

##### fs_read(path: str) -> Dict[str, Any]

读取文件内容。

**返回**:
```python
{
    "success": True,
    "content": "文件内容",
    "path": "/absolute/path/to/file"
}
```

##### fs_write(path: str, content: str) -> Dict[str, Any]

写入文件内容。

**返回**:
```python
{
    "success": True,
    "path": "/absolute/path/to/file",
    "bytes_written": 1234
}
```

##### fs_list(path: str = "") -> Dict[str, Any]

列出目录内容。

**返回**:
```python
{
    "success": True,
    "path": "/absolute/path",
    "items": [
        {"name": "file.txt", "type": "file", "size": 1234},
        {"name": "dir", "type": "directory", "size": None}
    ]
}
```

##### fs_create_dir(path: str) -> Dict[str, Any]

创建目录。

**返回**:
```python
{
    "success": True,
    "path": "/absolute/path/to/dir"
}
```

### GitMCPServer

Git操作服务器。

#### 初始化

```python
GitMCPServer(repo_path: str = None)
```

**参数**:
- `repo_path`: Git仓库路径(默认为当前目录)

#### 方法

##### git_init() -> Dict[str, Any]
##### git_add(files: List[str]) -> Dict[str, Any]
##### git_commit(message: str) -> Dict[str, Any]
##### git_diff() -> Dict[str, Any]
##### git_status() -> Dict[str, Any]

### CLIMCPServer

命令行执行服务器。

#### 初始化

```python
CLIMCPServer(working_dir: str = None)
```

#### 方法

##### cli_execute(command: str, timeout: int = 300) -> Dict[str, Any]

执行命令。

**返回**:
```python
{
    "success": True,
    "output": "命令输出",
    "error": "错误输出",
    "return_code": 0
}
```

### FeishuMCPServer

飞书文档操作服务器。

#### 初始化

```python
FeishuMCPServer(app_id: str = None, app_secret: str = None)
```

#### 方法

##### feishu_read_doc(url: str) -> Dict[str, Any]

读取飞书文档。

**返回**:
```python
{
    "success": True,
    "content": "文档内容",
    "doc_id": "document_id"
}
```

## Agents

### RequirementAnalyst

需求分析Agent。

#### 初始化

```python
RequirementAnalyst(api_key: str, model: str = "claude-sonnet-4-5-20250929")
```

#### 方法

##### analyze(requirement: str, source_type: str = "text") -> Dict[str, Any]

分析需求。

**返回**:
```python
{
    "success": True,
    "requirement": {
        "title": "项目标题",
        "description": "详细描述",
        "type": "web|mobile|backend|desktop|other",
        "features": [
            {
                "name": "功能名称",
                "description": "功能描述",
                "priority": "high|medium|low"
            }
        ],
        "technical_requirements": [...],
        "constraints": [...],
        "success_criteria": [...]
    }
}
```

### SystemArchitect

系统架构设计Agent。

#### 初始化

```python
SystemArchitect(api_key: str, model: str = "claude-opus-4-5-20251101")
```

#### 方法

##### design(requirement: Dict[str, Any]) -> Dict[str, Any]

设计系统架构。

**返回**:
```python
{
    "success": True,
    "architecture": {
        "overview": "架构概述",
        "tech_stack": {
            "frontend": [...],
            "backend": [...],
            "database": [...],
            "infrastructure": [...]
        },
        "directory_structure": {...},
        "data_model": [...],
        "architecture_patterns": [...],
        "security_considerations": [...],
        "scalability_considerations": [...]
    }
}
```

### APIDesigner

API设计Agent。

#### 初始化

```python
APIDesigner(api_key: str, model: str = "claude-sonnet-4-5-20250929")
```

#### 方法

##### design(requirement: Dict[str, Any], architecture: Dict[str, Any]) -> Dict[str, Any]

设计API规范。

**返回**:
```python
{
    "success": True,
    "api_spec": {
        "openapi": "3.0.0",
        "info": {...},
        "paths": {...},
        "components": {...}
    }
}
```

### TaskPlanner

任务规划Agent。

#### 初始化

```python
TaskPlanner(api_key: str, model: str = "claude-sonnet-4-5-20250929")
```

#### 方法

##### plan(requirement: Dict, architecture: Dict, api_spec: Dict) -> Dict[str, Any]

规划任务。

**返回**:
```python
{
    "success": True,
    "task_plan": {
        "tasks": [
            {
                "id": "task_001",
                "title": "任务标题",
                "description": "任务描述",
                "type": "setup|backend|frontend|database|testing|documentation",
                "priority": 1,
                "dependencies": [...],
                "estimated_complexity": "low|medium|high",
                "files_to_create": [...],
                "acceptance_criteria": [...]
            }
        ]
    }
}
```

##### get_next_task(task_plan: Dict, completed_tasks: List[str]) -> Dict[str, Any]

获取下一个可执行任务。

### CodeGenerator

代码生成Agent。

#### 初始化

```python
CodeGenerator(api_key: str, model: str = "claude-sonnet-4-5-20250929")
```

#### 方法

##### generate(task: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]

生成代码。

**返回**:
```python
{
    "success": True,
    "code": {
        "files": [
            {
                "path": "src/main.py",
                "content": "代码内容",
                "language": "python"
            }
        ],
        "tests": [...],
        "dependencies": [...],
        "setup_instructions": [...]
    }
}
```

##### fix_code(code: Dict, error: str, attempt: int) -> Dict[str, Any]

修复代码错误。

### CodeReviewer

代码审查Agent。

#### 初始化

```python
CodeReviewer(api_key: str, model: str = "claude-opus-4-5-20251101")
```

#### 方法

##### review(code: Dict[str, Any], requirement: Dict[str, Any]) -> Dict[str, Any]

审查代码。

**返回**:
```python
{
    "success": True,
    "review": {
        "overall_score": 85,
        "summary": "审查摘要",
        "strengths": [...],
        "issues": [
            {
                "severity": "critical|high|medium|low",
                "category": "security|performance|maintainability|style|correctness",
                "file": "path/to/file",
                "line": 42,
                "description": "问题描述",
                "suggestion": "修复建议"
            }
        ],
        "security_concerns": [...],
        "performance_concerns": [...],
        "best_practices": [...],
        "test_coverage": {...},
        "recommendations": [...],
        "approved": true
    }
}
```

## Skills

### CodeSkill

完整代码生成工作流。

#### 初始化

```python
CodeSkill(api_key: str, project_path: str = None)
```

#### 方法

##### execute(requirement: str, mode: str = "auto", from_feishu: str = None) -> Dict[str, Any]

执行工作流。

**参数**:
- `requirement`: 需求描述
- `mode`: 执行模式(auto/semi-auto/manual)
- `from_feishu`: 飞书文档URL

**返回**:
```python
{
    "success": True,
    "results": {
        "requirement": {...},
        "architecture": {...},
        "api_spec": {...},
        "task_plan": {...},
        "generated_files": [...],
        "review": {...}
    }
}
```

### DesignSkill

设计阶段工作流。

#### 初始化

```python
DesignSkill(api_key: str, project_path: str = None)
```

#### 方法

##### execute(requirement: str) -> Dict[str, Any]

执行设计工作流。

### ReviewSkill

代码审查工作流。

#### 初始化

```python
ReviewSkill(api_key: str, project_path: str = None)
```

#### 方法

##### execute(files: List[str] = None, requirement_path: str = None) -> Dict[str, Any]

执行审查工作流。

### RefactorSkill

代码重构工作流。

#### 初始化

```python
RefactorSkill(api_key: str, project_path: str = None)
```

#### 方法

##### execute(files: List[str], refactor_goal: str) -> Dict[str, Any]

执行重构工作流。

**参数**:
- `files`: 要重构的文件列表
- `refactor_goal`: 重构目标

**返回**:
```python
{
    "success": True,
    "refactored_files": [...],
    "total_files": 5
}
```
