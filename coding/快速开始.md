# 快速开始指南

## 5分钟快速上手

### 1. 安装依赖 (30秒)

```bash
pip install anthropic requests pytest
```

### 2. 设置API密钥 (30秒)

```bash
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 3. 运行第一个示例 (3分钟)

```bash
python examples/example_code_skill.py
```

这将生成一个完整的待办事项Web应用!

## 常用命令

### 生成完整项目

```bash
python main.py code "开发一个用户登录注册功能"
```

### 仅生成设计文档

```bash
python main.py design "开发一个电商系统"
```

### 审查现有代码

```bash
python main.py review --files src/*.py
```

### 重构代码

```bash
python main.py refactor --files old_code.py --goal "提高性能"
```

## Python API使用

```python
from skills.code_skill import CodeSkill
import os

# 初始化
skill = CodeSkill(
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    project_path="./my_project"
)

# 执行
result = skill.execute(
    requirement="开发一个简单的博客系统",
    mode="auto"
)

# 检查结果
if result["success"]:
    print("✅ 成功!")
    print(f"生成文件: {result['results']['generated_files']}")
else:
    print(f"❌ 失败: {result['error']}")
```

## 目录结构说明

```
生成的项目结构:
my_project/
├── src/              # 源代码
├── tests/            # 测试文件
├── docs/             # 设计文档
│   ├── requirement.json
│   ├── architecture.json
│   ├── api_spec.json
│   └── code_review.json
└── requirements.txt  # 依赖列表
```

## 常见问题

### Q: API密钥在哪里获取?
A: 访问 https://console.anthropic.com/ 获取

### Q: 支持哪些编程语言?
A: 目前支持Python、JavaScript、TypeScript等主流语言

### Q: 生成的代码质量如何?
A: 包含自动代码审查,评分通常在80-90分

### Q: 可以用于生产环境吗?
A: 建议先审查生成的代码,然后根据需要调整

## 下一步

- 阅读 [使用指南](docs/USAGE.md) 了解详细用法
- 查看 [API文档](docs/API.md) 了解所有接口
- 运行测试: `python -m pytest tests/`

## 获取帮助

- 查看文档: `docs/`目录
- 运行示例: `examples/`目录
- 提交问题: GitHub Issues

开始你的AI驱动开发之旅吧! 🚀
