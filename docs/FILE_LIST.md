# 飞书项目管理系统 - 文件清单

## 📋 完整文件列表

### 🔧 MCP工具目录 (MCP/)

#### Python脚本
| 文件名 | 用途 | 状态 |
|--------|------|------|
| `test_claude_api.py` | Claude API连接测试工具 | ✅ 保留 |
| `create_story_final.py` | 创建工作项工具 | ✅ 保留 |
| `get_view_workitems.py` | 视图数据获取核心模块 | ✅ 保留 |
| `web_app_v2.py` | Web界面主程序（推荐） | ✅ 保留 |
| ~~`web_app.py`~~ | Web界面V1（已过时） | ❌ 已删除 |
| ~~`test_filter.py`~~ | 筛选功能测试脚本 | ❌ 已删除 |

#### Web模板
| 文件名 | 用途 | 状态 |
|--------|------|------|
| `templates/index.html` | Web界面前端页面 | ✅ 保留 |

#### 文档
| 文件名 | 说明 | 状态 |
|--------|------|------|
| `WEB_README.md` | Web界面使用说明 | ✅ 保留 |
| `WEB_INTERFACE_GUIDE.md` | Web界面完整指南 | ✅ 保留 |
| `V2_IMPROVEMENTS.md` | V2版本改进说明 | ✅ 保留 |

#### 配置文件
| 文件名 | 说明 | 状态 |
|--------|------|------|
| `新建文本文档.txt` | 飞书MCP Server配置信息 | ✅ 保留 |
| `20260127-132341.jpg` | 截图文件 | ✅ 保留 |

---

### 📚 文档目录 (docs/)

| 文件名 | 说明 | 状态 |
|--------|------|------|
| `PYTHON_FILES.md` | **Python文件详细说明** ⭐ | ✅ 新建 |

---

### 🚀 启动脚本

| 文件名 | 说明 | 状态 |
|--------|------|------|
| `start_web_v2.bat` | Web界面V2启动脚本（推荐） | ✅ 保留 |
| `start_web.bat` | Web界面V1启动脚本（已过时） | ⚠️ 可删除 |

---

### 📖 主文档

| 文件名 | 说明 | 状态 |
|--------|------|------|
| `MCP_README.md` | MCP工具集总览文档 | ✅ 新建 |
| `README.md` | 三层AI Agent系统文档 | ✅ 保留 |

---

## 📊 文件统计

### 保留的文件
- **Python脚本**: 4个
- **Web模板**: 1个
- **文档**: 7个
- **配置文件**: 2个
- **启动脚本**: 1个（推荐）

### 删除的文件
- ~~`web_app.py`~~ - 已被V2替代
- ~~`test_filter.py`~~ - 测试脚本，不再需要

### 可选删除
- `start_web.bat` - V1启动脚本，建议删除

---

## 🗂️ 文件用途速查

### 想要测试API连接？
→ 运行 `MCP/test_claude_api.py`

### 想要创建工作项？
→ 运行 `MCP/create_story_final.py`

### 想要查看工作项列表（命令行）？
→ 运行 `MCP/get_view_workitems.py`

### 想要使用Web界面？
→ 双击 `start_web_v2.bat` 或运行 `MCP/web_app_v2.py`

### 想要了解Python文件详情？
→ 查看 `docs/PYTHON_FILES.md` ⭐

### 想要了解Web界面使用方法？
→ 查看 `MCP/WEB_README.md`

### 想要了解V2改进内容？
→ 查看 `MCP/V2_IMPROVEMENTS.md`

---

## 📁 推荐的目录结构

```
sample/
├── MCP/                          # MCP工具目录
│   ├── test_claude_api.py        # ✅ API测试
│   ├── create_story_final.py     # ✅ 创建工作项
│   ├── get_view_workitems.py     # ✅ 数据获取模块
│   ├── web_app_v2.py             # ✅ Web主程序
│   ├── templates/
│   │   └── index.html            # ✅ 前端页面
│   ├── WEB_README.md             # ✅ Web使用说明
│   ├── WEB_INTERFACE_GUIDE.md    # ✅ Web完整指南
│   ├── V2_IMPROVEMENTS.md        # ✅ V2改进说明
│   ├── 新建文本文档.txt           # ✅ MCP配置
│   └── 20260127-132341.jpg       # ✅ 截图
├── docs/
│   └── PYTHON_FILES.md           # ✅ Python文件说明 ⭐
├── start_web_v2.bat              # ✅ 启动脚本
├── MCP_README.md                 # ✅ MCP工具总览
└── README.md                     # ✅ 项目主文档
```

---

## 🔍 文件依赖关系

```
web_app_v2.py
    └── get_view_workitems.py
            ├── get_view_detail()
            └── parse_view_response()

create_story_final.py
    └── 独立运行

test_claude_api.py
    └── 独立运行

index.html
    └── 由 web_app_v2.py 提供服务
```

---

## 📝 维护建议

### 定期清理
- 删除不再使用的测试脚本
- 删除过时的启动脚本
- 清理临时文件

### 文档更新
- 当修改配置时，更新相关文档
- 当添加新功能时，更新PYTHON_FILES.md
- 保持版本号同步

### 备份重要文件
- `MCP/新建文本文档.txt` - MCP配置信息
- `web_app_v2.py` - 主程序
- `get_view_workitems.py` - 核心模块

---

**最后更新**: 2026-01-27
**维护者**: Claude Code
