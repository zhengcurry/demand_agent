# 通用AI开发工具集

一个**通用的AI驱动开发工具集**,可应用于任何软件开发项目。通过MCP Server提供底层能力,通过Skills提供高层工作流,实现从需求描述到代码实现的全自动化流程。

## 📚 文档导航

- **[项目概览.md](项目概览.md)** - 完整的项目介绍（推荐阅读）
- **[快速开始.md](快速开始.md)** - 快速上手指南
- **[UI快速开始.md](UI快速开始.md)** - Web UI 使用指南
- **[自愈功能快速开始.md](自愈功能快速开始.md)** - 自愈功能使用
- **[路线图.md](路线图.md)** - 功能规划和迭代计划
- **[待办事项.md](待办事项.md)** - 任务清单
- **[目录结构说明.md](目录结构说明.md)** - 完整的目录结构说明

## 核心特性

- **通用性**: 不绑定特定项目,可用于任何开发场景(Web、移动端、后端等)
- **模块化**: MCP + Agent + Skill三层架构
- **智能化**: AI驱动的需求分析、架构设计、代码生成
- **自动化**: 从需求到代码的全自动流程
- **自愈能力**: 自动错误恢复和重试机制 ⭐ 新功能
- **可扩展**: 易于添加新的MCP工具、Agent、Skill

## 架构概览

```
Layer 3: Skills (高层工作流,用户直接调用)
  /code  /design  /review  /refactor
         ↓
Layer 2: Agents (中层智能体,执行具体任务)
  需求分析 → 架构设计 → API设计 → 任务拆解 → 代码生成 → 代码审查
         ↓
Layer 1: MCP Servers (底层能力,提供原子操作)
  Feishu  Filesystem  Git  CLI
```

## 快速开始

### 方法 1: 使用 Web UI（推荐）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key（创建 .env 文件）
echo "ANTHROPIC_API_KEY=your-api-key" > .env

# 3. 启动 UI
python run_ui.py
```

详见：[UI快速开始.md](UI快速开始.md)

### 方法 2: 使用代码

```python
from skills.self_healing_skill import SelfHealingSkill

skill = SelfHealingSkill(
    api_key="your-api-key",
    project_path="./my_project",
    max_retries=3
)

result = skill.execute(requirement="你的需求描述")
```

详见：[快速开始.md](快速开始.md)

## 📁 项目结构

```
coding/
├── agents/          # AI Agent 模块
├── skills/          # 技能模块
├── mcp_servers/     # MCP 服务器
├── tests/           # 测试文件
├── debug/           # 调试脚本
├── docs/            # 英文文档
├── 文档/            # 中文文档
└── ...
```

完整结构说明：[目录结构说明.md](目录结构说明.md)

## 🎯 主要功能

### 1. Enhanced Code Skill
- 6 阶段代码生成工作流
- 从需求到代码的完整流程
- 包含测试和文档

### 2. Self-Healing Skill ⭐ 新功能
- 自动错误捕获和分类
- 智能重试机制
- 详细修复日志
- 可配置重试次数

### 3. Web UI
- 简洁直观的界面
- 多种输入方式
- 实时状态显示
- 灵活配置选项

## 📖 更多文档

- **完整文档**: 查看 [项目概览.md](项目概览.md)
- **功能规划**: 查看 [路线图.md](路线图.md)
- **开发文档**: 查看 `文档/开发文档/`
- **历史文档**: 查看 `文档/历史文档/`

## 🤝 贡献

欢迎贡献代码和文档！请查看 [待办事项.md](待办事项.md) 了解当前需要的功能。

## 📄 许可证

MIT License

---

**版本**: v1.0.0
**最后更新**: 2026-01-28
pip install -r requirements.txt
```

### 2. 配置API密钥

**方式1: 使用 .env 文件 (推荐)**

```bash
# 复制示例文件
copy .env.example .env  # Windows
# 或
cp .env.example .env    # Linux/Mac

# 编辑 .env 文件，填入你的API密钥
# ANTHROPIC_API_KEY=sk-ant-api03-你的实际密钥
```

**方式2: 设置环境变量**

```bash
# Windows (CMD)
set ANTHROPIC_API_KEY=your-api-key

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your-api-key"

# Linux/Mac
export ANTHROPIC_API_KEY="your-api-key"
```

**获取API密钥**: https://console.anthropic.com/

详细配置说明请查看 [API_KEY_SETUP.md](API_KEY_SETUP.md)

### 3. 验证配置

```bash
python test_system.py
```

如果看到 `[SUCCESS] All tests passed!` 说明配置成功。

### 4. 开始使用

```bash
pip install anthropic requests
```

### 设置环境变量

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 使用示例

```python
from skills.code_skill import CodeSkill

# 初始化
skill = CodeSkill(
    api_key="your-api-key",
    project_path="./my_project"
)

# 执行完整的代码生成工作流
result = skill.execute(
    requirement="开发一个用户登录注册功能",
    mode="auto"
)

if result["success"]:
    print("✅ 代码生成成功!")
    print(f"生成文件: {result['results']['generated_files']}")
```

## 可用的Skills

### /code - 完整开发工作流

从需求到代码的完整流程:

```python
from skills.code_skill import CodeSkill

skill = CodeSkill(api_key="your-api-key")
result = skill.execute("开发一个移动端登录注册功能")
```

**输出**:
- 生成的源代码文件
- 单元测试
- 设计文档
- 代码审查报告

### /design - 设计阶段

仅执行设计阶段(需求分析 + 架构设计 + API设计):

```python
from skills.design_skill import DesignSkill

skill = DesignSkill(api_key="your-api-key")
result = skill.execute("开发一个用户管理系统")
```

**输出**:
- 需求文档
- 架构文档
- API规范(OpenAPI)

### /review - 代码审查

审查现有代码:

```python
from skills.review_skill import ReviewSkill

skill = ReviewSkill(api_key="your-api-key")
result = skill.execute(
    files=["src/main.py", "src/utils.py"],
    requirement_path="docs/requirement.json"
)
```

**输出**:
- 代码审查报告
- 问题列表(按严重程度分类)
- 改进建议

### /refactor - 代码重构

重构现有代码:

```python
from skills.refactor_skill import RefactorSkill

skill = RefactorSkill(api_key="your-api-key")
result = skill.execute(
    files=["src/legacy.py"],
    refactor_goal="提高代码可读性和性能"
)
```

**输出**:
- 重构后的代码文件
- 重构摘要

## 项目结构

```
coding/
├── mcp_servers/          # MCP服务器实现
│   ├── filesystem_server/
│   ├── git_server/
│   ├── cli_server/
│   └── feishu_server/
├── agents/               # Agent实现
│   ├── requirement_analyst.py
│   ├── system_architect.py
│   ├── api_designer.py
│   ├── task_planner.py
│   ├── code_generator.py
│   └── code_reviewer.py
├── skills/               # Skills实现
│   ├── code_skill.py
│   ├── design_skill.py
│   ├── review_skill.py
│   └── refactor_skill.py
├── config/               # 配置文件
│   ├── agents/
│   ├── skills/
│   └── mcp/
└── tests/                # 测试文件
    ├── test_mcp/
    ├── test_agents/
    └── test_skills/
```

## 运行测试

```bash
# 测试MCP Servers
python -m pytest tests/test_mcp/

# 测试所有组件
python -m pytest tests/
```

## 技术栈

- **AI模型**: Claude Sonnet 4.5, Claude Opus 4.5
- **语言**: Python 3.8+
- **依赖**: anthropic, requests

## 文档

- [使用指南](docs/USAGE.md)
- [API文档](docs/API.md)
- [开发指南](docs/DEVELOPMENT.md)

## 许可证

MIT License
