# 项目概览

## 📚 快速导航

### 🚀 快速开始
- **基础使用**: [`QUICKSTART_UI.md`](QUICKSTART_UI.md) - Web UI 快速开始
- **自愈功能**: [`SELF_HEALING_QUICKSTART.md`](SELF_HEALING_QUICKSTART.md) - 自愈功能快速开始
- **完整文档**: [`UI_README.md`](UI_README.md) - 完整的 UI 使用文档

### 📖 核心文档
- **项目说明**: [`CLAUDE.md`](CLAUDE.md) - 项目架构和使用说明
- **路线图**: [`ROADMAP.md`](ROADMAP.md) - 详细的迭代计划
- **待办事项**: [`TODO.md`](TODO.md) - 任务清单

### 🔧 功能文档
- **自愈技能**: [`docs/SELF_HEALING_SKILL.md`](docs/SELF_HEALING_SKILL.md) - 自愈功能完整文档
- **增强代码技能**: [`docs/ENHANCED_CODE_SKILL.md`](docs/ENHANCED_CODE_SKILL.md) - 核心功能文档

---

## 🎯 项目简介

**Enhanced Code Skill** 是一个 AI 驱动的代码生成系统，通过 6 阶段工作流将需求转化为高质量代码。

### 核心特性

1. **6 阶段工作流**
   - 📋 需求分析
   - 🏗️ 架构设计
   - 🔍 设计审查
   - 📝 任务规划
   - 💻 代码生成
   - ✅ 代码审查

2. **自愈功能** ⭐ 新功能
   - 自动错误捕获和分类
   - 智能重试机制
   - 详细修复日志
   - 可配置重试次数

3. **图形化界面**
   - 简洁的 Web UI
   - 实时状态显示
   - 多种输入方式
   - 灵活配置选项

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

创建 `.env` 文件：
```bash
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. 启动 UI

```bash
python run_ui.py
```

### 4. 使用

1. 在侧边栏输入 API Key
2. 勾选 "Enable Self-Healing"（推荐）
3. 输入需求描述
4. 点击"生成代码"

---

## 📁 项目结构

```
coding/
├── agents/                    # AI Agents
│   ├── requirement_analyst.py # 需求分析
│   ├── system_architect.py    # 架构设计
│   ├── api_designer.py        # API 设计
│   ├── task_planner.py        # 任务规划
│   ├── code_generator.py      # 代码生成
│   └── code_reviewer.py       # 代码审查
│
├── skills/                    # 技能模块
│   ├── enhanced_code_skill.py # 基础工作流
│   ├── self_healing_skill.py  # 自愈包装器
│   ├── error_context.py       # 错误上下文
│   └── fix_logger.py          # 修复日志
│
├── mcp_servers/               # MCP 服务器
│   ├── filesystem_server/     # 文件系统操作
│   └── git_server/            # Git 操作
│
├── docs/                      # 文档
│   ├── SELF_HEALING_SKILL.md
│   └── ENHANCED_CODE_SKILL.md
│
├── ui_app.py                  # Web UI 主程序
├── run_ui.py                  # UI 启动脚本
├── utils.py                   # 工具函数
├── env_config.py              # 环境配置
│
├── ROADMAP.md                 # 迭代路线图
├── TODO.md                    # 待办事项
└── requirements.txt           # 依赖列表
```

---

## 🎨 功能亮点

### ✅ 已实现

#### 1. Enhanced Code Skill
- 完整的 6 阶段代码生成工作流
- 支持多种项目类型
- 生成完整的项目结构
- 包含测试和文档

#### 2. Self-Healing (Phase 1)
- 7 种错误类型自动分类
- 可配置的重试机制（1-5 次）
- 详细的修复日志
- UI 集成

#### 3. Web UI
- 简洁直观的界面
- 多种输入方式（文本/文件/URL）
- 实时状态显示
- 灵活的配置选项

#### 4. 错误处理
- 改进的 JSON 解析
- 增加的 token 限制
- 详细的错误上下文

---

### 🚧 计划中

#### Self-Healing Phase 2（高优先级）
- AI 驱动的错误分析
- 智能修复建议
- 错误模式识别

#### Self-Healing Phase 3（中优先级）
- 自动应用修复
- 修复验证机制
- 学习历史经验

#### UI/UX 改进
- 实时进度显示
- 结果可视化
- 历史记录管理

#### 性能优化
- 并行执行
- 智能缓存
- 异步 API 调用

#### 功能扩展
- 多语言支持（JS/TS, Java, Go）
- 框架模板库
- 代码质量检查

详见 [`ROADMAP.md`](ROADMAP.md)

---

## 📊 使用统计

### 当前版本: v1.0.0

**功能完成度**:
- ✅ 核心工作流: 100%
- ✅ Web UI: 100%
- ✅ Self-Healing Phase 1: 100%
- 🚧 Self-Healing Phase 2: 0%
- 🚧 Self-Healing Phase 3: 0%

**代码统计**:
- Python 文件: 20+
- 代码行数: 5000+
- 文档页数: 10+

---

## 🤝 贡献指南

### 如何贡献

1. **报告问题**
   - 在 GitHub Issues 中报告 bug
   - 提供详细的错误信息和重现步骤

2. **提出建议**
   - 在 `TODO.md` 中添加功能建议
   - 在 `ROADMAP.md` 中更新计划

3. **提交代码**
   - Fork 项目
   - 创建功能分支
   - 提交 Pull Request

### 开发规范

- 遵循 PEP 8 代码风格
- 添加必要的注释和文档
- 编写单元测试
- 更新相关文档

---

## 📝 版本历史

### v1.0.0 (2026-01-28)
- ✨ 初始版本发布
- ✅ 完整的 6 阶段工作流
- ✅ Web UI
- ✅ Self-Healing Phase 1
- 📚 完整文档

### 计划版本

#### v1.1.0 (计划中)
- Self-Healing Phase 2
- UI 实时进度
- 并行执行优化

#### v1.2.0 (计划中)
- Self-Healing Phase 3
- 多语言支持
- 框架模板库

#### v2.0.0 (长期)
- 完整的自愈系统
- 企业级功能
- 云端部署支持

---

## 🔗 相关链接

- **Anthropic Claude**: https://www.anthropic.com/
- **Streamlit**: https://streamlit.io/
- **LangChain**: https://www.langchain.com/

---

## 📧 联系方式

- **问题反馈**: GitHub Issues
- **功能建议**: `TODO.md` 或 `ROADMAP.md`
- **文档改进**: Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证。

---

## 🙏 致谢

感谢以下技术和工具：
- Anthropic Claude API
- Streamlit
- LangChain
- Python 生态系统

---

**最后更新**: 2026-01-28
**维护者**: Claude Sonnet 4.5
**版本**: v1.0.0
