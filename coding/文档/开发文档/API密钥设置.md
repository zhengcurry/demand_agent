# API密钥配置指南

## 问题：运行时提示"ANTHROPIC_API_KEY 未设置"

这是因为程序需要Anthropic API密钥才能调用Claude模型。以下是三种配置方式：

---

## ✅ 方式1: 使用 .env 文件 (推荐)

这是最简单、最安全的方式。

### 步骤：

1. **复制示例文件**
   ```bash
   copy .env.example .env
   ```
   或在Linux/Mac上：
   ```bash
   cp .env.example .env
   ```

2. **编辑 .env 文件**

   打开 `.env` 文件，将内容修改为：
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-你的实际密钥
   ```

3. **保存并运行**
   ```bash
   python main.py code "开发一个登录功能"
   ```

### 优点：
- ✅ 密钥不会被提交到Git（.env已在.gitignore中）
- ✅ 不需要每次都设置环境变量
- ✅ 团队成员可以各自配置自己的密钥

---

## 方式2: 设置环境变量

### Windows (CMD)
```cmd
set ANTHROPIC_API_KEY=sk-ant-api03-你的实际密钥
python main.py code "开发一个登录功能"
```

### Windows (PowerShell)
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-api03-你的实际密钥"
python main.py code "开发一个登录功能"
```

### Linux/Mac (Bash/Zsh)
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-你的实际密钥"
python main.py code "开发一个登录功能"
```

### 永久设置（可选）

**Windows:**
1. 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
2. 在"用户变量"中新建：
   - 变量名: `ANTHROPIC_API_KEY`
   - 变量值: `sk-ant-api03-你的实际密钥`

**Linux/Mac:**
在 `~/.bashrc` 或 `~/.zshrc` 中添加：
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-你的实际密钥"
```
然后运行：
```bash
source ~/.bashrc  # 或 source ~/.zshrc
```

---

## 方式3: 在代码中直接传入

如果你是通过Python API使用，可以直接传入密钥：

```python
from skills.code_skill import CodeSkill

skill = CodeSkill(api_key="sk-ant-api03-你的实际密钥")
result = skill.execute("开发一个登录功能")
```

⚠️ **注意**: 这种方式不推荐，因为密钥可能被意外提交到代码仓库。

---

## 如何获取API密钥？

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 登录或注册账号
3. 进入 API Keys 页面
4. 点击 "Create Key" 创建新密钥
5. 复制密钥（格式类似：`sk-ant-api03-xxxxx...`）

---

## 验证配置是否成功

运行以下命令检查配置：

```bash
python env_config.py
```

如果配置正确，会显示：
```
✅ 环境配置正确!
API密钥已设置 (长度: 108 字符)
```

如果配置错误，会显示详细的设置说明。

---

## 常见问题

### Q1: 我已经设置了环境变量，为什么还是提示未设置？

**A:** 可能的原因：
1. 环境变量只在当前终端会话有效，关闭终端后失效
2. 使用IDE运行时，IDE可能没有加载环境变量
3. 变量名拼写错误（必须是 `ANTHROPIC_API_KEY`）

**解决方案**: 使用 `.env` 文件方式（方式1）

### Q2: .env 文件放在哪里？

**A:** 放在项目根目录，即 `main.py` 所在的目录：
```
coding/
├── .env          ← 这里
├── .env.example
├── main.py
├── ...
```

### Q3: 密钥会被泄露吗？

**A:** 不会，只要：
1. 不要将 `.env` 文件提交到Git（已在.gitignore中排除）
2. 不要在代码中硬编码密钥
3. 不要在公开场合分享密钥

### Q4: 可以使用其他名称的环境变量吗？

**A:** 不可以，程序固定读取 `ANTHROPIC_API_KEY` 这个变量名。

---

## 安全建议

1. ✅ 使用 `.env` 文件存储密钥
2. ✅ 确保 `.env` 在 `.gitignore` 中
3. ✅ 不要在代码中硬编码密钥
4. ✅ 定期轮换API密钥
5. ✅ 不要在公开仓库中提交密钥
6. ❌ 不要将密钥分享给他人
7. ❌ 不要在截图中暴露密钥

---

## 下一步

配置完成后，可以：

1. 运行示例程序：
   ```bash
   python examples/example_code_skill.py
   ```

2. 使用命令行工具：
   ```bash
   python main.py code "开发一个待办事项应用"
   ```

3. 阅读使用文档：
   - [快速开始](QUICKSTART.md)
   - [使用指南](docs/USAGE.md)
