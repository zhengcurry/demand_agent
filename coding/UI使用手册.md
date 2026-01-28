# Enhanced Code Skill - Web UI

简单的图形化界面，用于调用 Enhanced Code Skill 的代码生成功能。

## 功能特性

- 📝 **多种输入方式**
  - 文本输入框直接输入需求
  - 上传需求文件（.txt, .md）
  - URL 输入（即将支持）

- ⚙️ **灵活配置**
  - 自定义项目目录位置
  - 选择自动/手动审查模式
  - 可选择是否在设计阶段暂停

- 📊 **实时状态展示**
  - 工作流执行状态
  - 详细的日志输出
  - 最终评分和生成文件数量

- 🚀 **6 阶段工作流**
  1. 需求分析
  2. 设计（架构 + API）
  3. 设计审查
  4. 任务规划
  5. 代码生成
  6. 代码审查

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法 1: 使用启动脚本（推荐）

```bash
python run_ui.py
```

### 方法 2: 直接运行 Streamlit

```bash
streamlit run ui_app.py
```

## 配置

### API Key

在侧边栏输入您的 Anthropic API Key，或者在 `.env` 文件中配置：

```bash
ANTHROPIC_API_KEY=your-api-key-here
```

### 项目目录

在侧边栏的 "Project Directory" 输入框中指定代码生成的目标目录。

## 使用示例

1. **启动应用**
   ```bash
   python run_ui.py
   ```

2. **输入需求**

   在主界面的文本框中输入需求，例如：
   ```
   开发一个简单的计算器API:

   功能需求:
   1. 支持加法、减法、乘法、除法
   2. 输入验证
   3. 错误处理

   技术要求:
   - 后端: Python + FastAPI
   - 返回JSON格式
   ```

3. **配置选项**
   - 在侧边栏设置项目目录
   - 选择审查模式（auto/manual）
   - 根据需要勾选"Pause for Review"

4. **生成代码**
   - 点击 "🚀 Generate Code" 按钮
   - 等待工作流完成
   - 查看生成的代码和报告

## 输出

生成的代码和报告将保存在指定的项目目录中：

```
generated_project/
├── src/              # 源代码
├── tests/            # 测试文件
├── docs/             # 文档和报告
│   ├── stage1_requirement_report.json
│   ├── stage2_design_report.json
│   ├── stage3_design_review_report.json
│   ├── stage4_task_planning_report.json
│   ├── stage5_code_generation_report.json
│   ├── stage6_code_review_report.json
│   └── complete_workflow_report.json
└── ...
```

## 注意事项

- 确保已设置 Anthropic API Key
- 工作流执行可能需要几分钟时间
- 生成的代码质量取决于需求描述的清晰度
- 建议先使用简单的需求进行测试

## 故障排除

### 问题: API Key 未设置

**解决方案**: 在侧边栏输入 API Key 或在 `.env` 文件中配置

### 问题: 工作流执行失败

**解决方案**:
- 检查 API Key 是否有效
- 查看日志输出了解具体错误
- 确保需求描述清晰完整

### 问题: 无法启动 UI

**解决方案**:
```bash
# 安装 streamlit
pip install streamlit

# 检查版本
streamlit --version
```

## 技术栈

- **UI 框架**: Streamlit
- **AI 模型**: Claude (Anthropic)
- **后端**: Python 3.8+
- **工作流**: EnhancedCodeSkill

## 更新日志

### v1.0.0 (2026-01-28)
- ✨ 初始版本
- 📝 支持文本输入和文件上传
- ⚙️ 可配置项目目录和审查模式
- 📊 实时状态展示
- 🚀 完整的 6 阶段工作流

## 许可证

与主项目相同
