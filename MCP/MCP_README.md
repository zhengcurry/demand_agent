# 飞书项目管理系统 - MCP集成工具

> 基于飞书MCP (Model Context Protocol) Server的项目管理工具集

## 📖 项目简介

这是一个独立的工具集，用于通过飞书MCP Server管理和查看飞书项目中的工作项。提供了命令行工具和现代化的Web界面。

## ✨ 主要功能

- ✅ **工作项查看**: 查看视图中的所有工作项（1175条记录）
- ✅ **多维度筛选**: 支持按项目、版本、业务线筛选
- ✅ **详情查看**: 点击工作项查看描述、文档URL、交付物清单 ⭐ 新增
- ✅ **工作项创建**: 通过脚本快速创建新的工作项
- ✅ **Web界面**: 现代化的Web界面，支持分页和实时筛选
- ✅ **API测试**: 测试Claude API连接状态

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- Flask (Web界面需要)
- requests库

### 2. 安装依赖

```bash
pip install flask requests
```

### 3. 启动Web界面（推荐）

**Windows用户**:
```bash
双击 start_web_v2.bat
```

**命令行启动**:
```bash
cd MCP
python web_app_v2.py
```

然后在浏览器中访问: http://127.0.0.1:5000

⚠️ **注意**: 首次启动需要15-20秒加载所有数据（1175条记录）

## 📁 项目结构

```
sample/
├── MCP/                          # MCP工具目录
│   ├── test_claude_api.py        # API连接测试
│   ├── create_story_final.py     # 创建工作项
│   ├── get_view_workitems.py     # 数据获取核心模块
│   ├── web_app_v2.py             # Web界面主程序
│   ├── templates/                # Web模板
│   │   └── index.html            # 前端页面
│   ├── WEB_README.md             # Web使用说明
│   ├── WEB_INTERFACE_GUIDE.md    # Web完整指南
│   ├── DETAIL_VIEW_GUIDE.md      # 详情查看功能说明 ⭐
│   └── V2_IMPROVEMENTS.md        # V2改进说明
├── docs/                         # 文档目录
│   └── PYTHON_FILES.md           # Python文件详细说明
├── start_web_v2.bat              # Web启动脚本
└── MCP_README.md                 # 本文档
```

## 📊 数据统计

- **总工作项数**: 1175条
- **项目数**: 72个
- **版本数**: 232个
- **业务线数**: 10个
- **总页数**: 24页

## 🎯 核心功能

### 1. Web界面

**特性**:
- 现代化UI设计
- 三个筛选维度（项目、版本、业务线）
- 完整的筛选选项（从全部1175条数据中提取）
- 服务端筛选（筛选对全部数据生效）
- 点击查看详情（描述、文档URL、交付物清单）⭐ 新增
- 分页浏览
- 优先级颜色标识

**访问地址**:
- 本地: http://127.0.0.1:5000
- 局域网: http://172.16.42.73:5000

**界面功能**:
1. **筛选区域**: 三个下拉选择框
2. **统计信息**: 显示当前页、总页数、筛选结果数
3. **数据表格**: 8个字段展示，点击行查看详情 ⭐
4. **详情模态框**: 显示完整的描述、文档URL、交付物清单 ⭐
5. **分页控制**: 上一页/下一页按钮

**优先级颜色**:
- 🔴 **重要且紧急**: 红色徽章
- 🟡 **重要但不紧急**: 黄色徽章
- 🔵 **紧急但不重要**: 蓝色徽章
- ⚪ **不紧急不重要**: 灰色徽章

### 2. 命令行工具

**test_claude_api.py** - API连接测试:
```bash
cd MCP
python test_claude_api.py
```

**create_story_final.py** - 创建工作项:
```bash
cd MCP
python create_story_final.py
```

**get_view_workitems.py** - 查看工作项列表:
```bash
cd MCP
python get_view_workitems.py
```

## 🔧 配置说明

### MCP Server配置

配置信息存储在 `MCP/新建文本文档.txt`:
- MCP Server URL: `https://project.feishu.cn/mcp_server/v1`
- MCP Key: `m-e468e82b-0313-445b-bf87-f0e3f9a5723f`
- Project Key: `662ef8e0b2b6c06ce1ef28db`
- User Key: `7371651783610875905`

### 视图ID配置

默认视图ID: `8SReqkNvg`

修改位置:
- `get_view_workitems.py` 第221行
- `web_app_v2.py` 第16行

### Claude API配置

- API地址: `http://172.16.40.227:3000/v1/messages`
- 模型: `claude-sonnet-4-5-20250929`

修改位置:
- `test_claude_api.py` 第15-17行

## 📚 文档说明

| 文档 | 说明 |
|------|------|
| `docs/PYTHON_FILES.md` | **Python文件详细说明** ⭐ |
| `MCP/WEB_README.md` | Web界面使用说明 |
| `MCP/WEB_INTERFACE_GUIDE.md` | Web界面完整指南 |
| `MCP/DETAIL_VIEW_GUIDE.md` | **详情查看功能说明** ⭐ 新增 |
| `MCP/V2_IMPROVEMENTS.md` | V2版本改进说明 |

## 🔍 使用示例

### 示例1: 查看所有工作项
1. 启动Web界面: `双击 start_web_v2.bat`
2. 浏览器访问: http://127.0.0.1:5000
3. 页面自动显示第1页的50条记录
4. 统计信息显示总共1173条

### 示例2: 查看工作项详情 ⭐ 新增
1. 在工作项列表中，鼠标悬停在任意行上
2. 行背景变为浅蓝色，显示"查看详情"提示
3. 点击该行，弹出详情模态框
4. 查看完整的描述、需求文档URL、交付物清单
5. 点击"关闭"或模态框外部区域关闭详情

### 示例3: 筛选特定业务线
1. 在"所属业务线"下拉框选择"YF-KA产品线"
2. 点击"应用筛选"按钮
3. 显示所有YF-KA产品线的工作项（约120条）
4. 可以翻页查看所有结果

### 示例4: 组合筛选
1. 选择"所属业务线": "自研芯片平台预研业务线"
2. 选择"规划版本": "标定集成V3版本"
3. 点击"应用筛选"
4. 显示同时满足两个条件的工作项

### 示例5: 创建工作项
```bash
cd MCP
python create_story_final.py
```

输出示例:
```
创建成功，实例地址为：
https://project.feishu.cn/662ef8e0b2b6c06ce1ef28db/story/detail/6745760107
```

## ⚡ 性能优化

1. **数据缓存**: 启动时加载所有数据到内存（约2-3MB）
2. **请求间隔**: 每页间隔0.5秒，避免API限流
3. **按需分页**: 前端只请求当前页数据，减少传输量

## 🆘 故障排除

### 问题1: Web界面无法访问
**解决方案**:
- 检查端口5000是否被占用
- 确认防火墙设置
- 查看控制台错误信息

### 问题2: 数据加载失败
**解决方案**:
- 检查MCP Server配置是否正确
- 确认网络连接正常
- 验证视图ID是否正确
- 查看错误日志

### 问题3: 筛选不生效
**解决方案**:
- 确认使用的是 `web_app_v2.py`（不是web_app.py）
- 点击"应用筛选"按钮
- 检查筛选条件是否有效
- 查看浏览器控制台是否有错误

### 问题4: API连接失败
**解决方案**:
- 运行 `test_claude_api.py` 检查连接
- 检查API地址和密钥是否正确
- 确认网络连接正常

## 📝 注意事项

1. **首次启动时间**: Web界面首次启动需要15-20秒加载所有数据
2. **内存占用**: 约2-3MB用于缓存1175条记录
3. **数据更新**: 数据在启动时加载，如需更新请重启服务或访问 `/api/reload`
4. **浏览器兼容**: 推荐使用Chrome、Edge、Firefox等现代浏览器
5. **API限流**: 加载数据时每页间隔0.5秒，避免触发限流
6. **详情字段**: 详情模态框显示description、wiki、field_4972f5三个字段 ⭐

## 🔄 版本历史

### V2.1 (2026-01-27)
- ✅ 新增工作项详情查看功能 ⭐
- ✅ 支持查看描述、需求文档URL、交付物清单
- ✅ 添加模态框展示详情
- ✅ 优化交互体验（行悬停高亮、点击查看）
- ✅ 新增详情API接口 `/api/workitem/<work_item_id>`
- ✅ 更新数据统计（1175条记录，232个版本）

### V2.0 (2026-01-27)
- ✅ 改进筛选功能，支持全量数据筛选
- ✅ 启动时加载所有1173条记录
- ✅ 完整的筛选选项（72个项目、231个版本、10个业务线）
- ✅ 服务端筛选，确保准确性
- ✅ 优化分页显示
- ✅ 删除过时文件（web_app.py, test_filter.py）

### V1.0 (2026-01-27)
- ✅ 基础Web界面
- ✅ 命令行工具
- ✅ 工作项创建功能
- ✅ API测试工具

## 🎨 技术栈

- **后端**: Flask (Python)
- **前端**: HTML + CSS + JavaScript (原生)
- **API**: 飞书MCP Server
- **数据格式**: JSON, Markdown表格

## 📞 技术支持

如有问题，请：
1. 查看 `docs/PYTHON_FILES.md` 了解各文件用途
2. 检查控制台输出的错误信息
3. 验证MCP Server配置信息
4. 查看相关文档

## 📄 许可证

本项目仅供内部使用。

---

**最后更新**: 2026-01-27
**版本**: V2.1
**维护者**: Claude Code

**快速链接**:
- [Python文件详细说明](../docs/PYTHON_FILES.md) ⭐
- [Web界面使用说明](WEB_README.md)
- [详情查看功能说明](DETAIL_VIEW_GUIDE.md) ⭐ 新增
- [V2改进说明](V2_IMPROVEMENTS.md)
