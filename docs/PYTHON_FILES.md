# 飞书项目管理系统 - Python文件说明文档

## 📁 目录结构

```
sample/
├── MCP/                          # MCP相关脚本目录
│   ├── test_claude_api.py        # Claude API连接测试
│   ├── create_story_final.py     # 创建工作项工具
│   ├── get_view_workitems.py     # 视图数据获取核心模块
│   ├── web_app_v2.py             # Web界面主程序（推荐）
│   ├── templates/                # Web界面模板
│   │   └── index.html            # 前端页面
│   └── 新建文本文档.txt           # 飞书MCP配置信息
├── docs/                         # 文档目录
│   └── PYTHON_FILES.md           # 本文档
└── start_web_v2.bat              # Web界面启动脚本
```

## 📄 Python文件详细说明

### 1. test_claude_api.py
**用途**: Claude API连接测试工具

**功能**:
- 测试Claude API的连接状态
- 验证API密钥是否有效
- 测试普通聊天补全功能
- 测试流式聊天功能

**使用场景**:
- 首次配置MCP环境时验证连接
- 排查API连接问题
- 测试不同的Claude模型

**运行方法**:
```bash
cd MCP
python test_claude_api.py
```

**配置信息**:
- API地址: `http://172.16.40.227:3000/v1/messages`
- 模型: `claude-sonnet-4-5-20250929`
- API Key: 在代码第16行配置

**输出示例**:
```
测试1: 普通聊天补全
==================================================
API响应成功!
回答: [Claude的回复内容]
Token使用情况:
  - 输入tokens: 35
  - 输出tokens: 391
```

---

### 2. create_story_final.py
**用途**: 在飞书项目管理中创建工作项（Story）

**功能**:
- 通过MCP Server API创建新的工作项
- 支持设置工作项名称
- 自动返回创建成功的工作项详情页URL

**使用场景**:
- 批量创建工作项
- 自动化工作项创建流程
- 集成到其他脚本中

**运行方法**:
```bash
cd MCP
python create_story_final.py
```

**配置信息**:
- MCP Server URL: 飞书项目管理MCP接口
- Project Key: `662ef8e0b2b6c06ce1ef28db`
- 工作项类型: `story`（需求）

**代码示例**:
```python
from create_story_final import create_workitem

# 创建工作项
result = create_workitem(
    work_item_type="story",
    story_name="新需求名称"
)
```

**输出示例**:
```
创建成功，实例地址为：
https://project.feishu.cn/662ef8e0b2b6c06ce1ef28db/story/detail/6745760107
```

---

### 3. get_view_workitems.py
**用途**: 视图工作项数据获取核心模块

**功能**:
- 从飞书MCP Server获取指定视图的工作项列表
- 解析Markdown表格格式的API响应
- 支持本地筛选功能（项目、版本、业务线）
- 提供命令行工具直接查看数据

**核心函数**:

1. **`get_view_detail(view_id, fields, page_num)`**
   - 获取指定视图的某一页数据
   - 参数:
     - `view_id`: 视图ID（如"8SReqkNvg"）
     - `fields`: 要查询的字段列表
     - `page_num`: 页码（从1开始）
   - 返回: API响应结果

2. **`parse_view_response(result)`**
   - 解析API响应，提取工作项列表
   - 支持Markdown表格格式解析
   - 返回: 工作项字典列表

3. **`parse_markdown_table(text)`**
   - 解析Markdown表格文本
   - 自动映射字段名到字段key
   - 处理JSON格式的嵌套字段

4. **`filter_workitems(workitems, project_filter, version_filter, business_filter)`**
   - 本地筛选工作项
   - 支持模糊匹配
   - 返回筛选后的列表

**使用场景**:
- 作为其他脚本的数据源模块
- 命令行快速查看工作项
- 数据导出和分析

**运行方法**:
```bash
cd MCP
python get_view_workitems.py
```

**配置信息**:
- 在脚本第221行修改 `VIEW_ID`
- 在脚本第224-226行设置筛选条件

**代码示例**:
```python
from get_view_workitems import get_view_detail, parse_view_response

# 获取第1页数据
result = get_view_detail(view_id="8SReqkNvg", page_num=1)

# 解析工作项
workitems = parse_view_response(result)

# 输出工作项数量
print(f"获取到 {len(workitems)} 个工作项")
```

---

### 4. web_app_v2.py
**用途**: Web界面主程序（推荐使用）

**功能**:
- 提供Web界面查看和筛选工作项
- 启动时自动加载所有数据（1173条记录）
- 支持完整的筛选功能（72个项目、231个版本、10个业务线）
- 服务端筛选，确保筛选对全部数据生效
- 前端分页展示

**核心功能**:

1. **数据加载**
   - `load_all_workitems()`: 启动时循环获取所有24页数据
   - 数据缓存在内存中，后续请求无需重新获取
   - 自动提取完整的筛选选项

2. **API接口**
   - `GET /`: 主页面
   - `GET /api/workitems`: 获取工作项列表（支持筛选和分页）
   - `GET /api/filter_options`: 获取筛选选项
   - `GET /api/reload`: 重新加载数据

3. **服务端筛选**
   - `filter_workitems_server()`: 在全部数据上进行筛选
   - 支持项目、版本、业务线三个维度
   - 支持模糊匹配

**使用场景**:
- 日常查看和管理工作项
- 多维度筛选和分析
- 团队协作查看项目进度

**运行方法**:
```bash
# 方式1: 直接运行
cd MCP
python web_app_v2.py

# 方式2: 使用启动脚本
双击 start_web_v2.bat
```

**访问地址**:
- 本地: http://127.0.0.1:5000
- 局域网: http://172.16.42.73:5000

**配置信息**:
- 第16行: `VIEW_ID = "8SReqkNvg"` - 视图ID
- 第17行: `PROJECT_KEY = "662ef8e0b2b6c06ce1ef28db"` - 项目Key
- 第19行: `TOTAL_PAGES = 24` - 总页数

**启动输出**:
```
================================================================================
正在加载所有工作项数据...
================================================================================
正在获取第 1/24 页...
  ✓ 第 1 页: 50 条记录
正在获取第 2/24 页...
  ✓ 第 2 页: 50 条记录
...
================================================================================
✅ 数据加载完成!
   总记录数: 1173
   项目数: 72
   版本数: 231
   业务线数: 10
================================================================================

访问地址: http://127.0.0.1:5000
```

**API使用示例**:
```bash
# 获取所有工作项（第1页）
curl "http://127.0.0.1:5000/api/workitems?page=1"

# 筛选YF-KA产品线的工作项
curl "http://127.0.0.1:5000/api/workitems?business=YF-KA产品线"

# 组合筛选
curl "http://127.0.0.1:5000/api/workitems?business=自研芯片平台预研业务线&version=V3版本"

# 获取筛选选项
curl "http://127.0.0.1:5000/api/filter_options"

# 重新加载数据
curl "http://127.0.0.1:5000/api/reload"
```

---

## 🔗 文件依赖关系

```
web_app_v2.py
    └── get_view_workitems.py
            ├── get_view_detail()      # 获取视图数据
            └── parse_view_response()  # 解析响应

create_story_final.py
    └── 独立运行，无依赖

test_claude_api.py
    └── 独立运行，无依赖
```

## 📊 数据流程图

```
飞书MCP Server
    ↓
get_view_workitems.py (获取和解析数据)
    ↓
web_app_v2.py (缓存、筛选、API服务)
    ↓
index.html (前端展示)
    ↓
用户浏览器
```

## 🚀 快速开始

### 1. 测试API连接
```bash
cd MCP
python test_claude_api.py
```

### 2. 创建工作项
```bash
cd MCP
python create_story_final.py
```

### 3. 查看工作项列表（命令行）
```bash
cd MCP
python get_view_workitems.py
```

### 4. 启动Web界面（推荐）
```bash
# Windows
双击 start_web_v2.bat

# 或命令行
cd MCP
python web_app_v2.py
```

然后访问: http://127.0.0.1:5000

## 🔧 配置说明

### MCP Server配置
所有脚本使用的MCP Server配置信息存储在 `MCP/新建文本文档.txt` 中：
- MCP Server URL
- MCP Key
- Project Key
- User Key

### 修改视图ID
如需查看不同的视图，修改以下文件：
- `get_view_workitems.py` 第221行
- `web_app_v2.py` 第16行

### 修改API地址
如需使用不同的Claude API地址，修改：
- `test_claude_api.py` 第15-16行

## 📝 注意事项

1. **首次启动时间**: `web_app_v2.py` 首次启动需要15-20秒加载所有数据
2. **内存占用**: 1173条记录缓存在内存中，约2-3MB
3. **数据更新**: 数据在启动时加载，如需更新请重启服务或调用 `/api/reload`
4. **API限流**: 加载数据时每页间隔0.5秒，避免触发API限流

## 🆘 故障排除

### 问题1: API连接失败
- 运行 `test_claude_api.py` 检查连接
- 检查API地址和密钥是否正确
- 确认网络连接正常

### 问题2: Web界面无法访问
- 检查端口5000是否被占用
- 确认防火墙设置
- 查看控制台错误信息

### 问题3: 数据加载失败
- 检查MCP Server配置
- 确认视图ID正确
- 查看错误日志

## 📚 相关文档

- `WEB_README.md` - Web界面使用说明
- `WEB_INTERFACE_GUIDE.md` - Web界面完整指南
- `V2_IMPROVEMENTS.md` - V2版本改进说明

## 📞 技术支持

如有问题，请查看：
1. 控制台输出的错误信息
2. 相关文档说明
3. MCP Server配置是否正确

---

**最后更新**: 2026-01-27
**版本**: V2.0
