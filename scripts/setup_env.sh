#!/bin/bash
# 环境配置脚本 - 从扣子迁移到 Claude

echo "========================================"
echo "三层AI Agent系统 - 环境配置"
echo "========================================"
echo ""

# 检查是否已设置 ANTHROPIC_API_KEY
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️  未检测到 ANTHROPIC_API_KEY 环境变量"
    echo ""
    echo "请按照以下步骤设置："
    echo "1. 访问 https://console.anthropic.com/"
    echo "2. 创建或获取 API Key"
    echo "3. 运行: export ANTHROPIC_API_KEY='your-api-key'"
    echo ""
    read -p "是否现在输入 API Key? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -sp "请输入 ANTHROPIC_API_KEY: " api_key
        echo ""
        export ANTHROPIC_API_KEY="$api_key"
        echo "✅ API Key 已设置（仅本次会话有效）"
    else
        echo "❌ 未设置 API Key，程序无法运行"
        exit 1
    fi
else
    echo "✅ 检测到 ANTHROPIC_API_KEY"
fi

# 设置 WORKSPACE_PATH
export WORKSPACE_PATH=$(pwd)
echo "✅ WORKSPACE_PATH 已设置为: $WORKSPACE_PATH"
echo ""

# 检查 Python 版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

# 检查依赖
echo ""
echo "正在检查依赖..."

if python3 -c "import anthropic" 2>/dev/null; then
    echo "✅ anthropic 已安装"
else
    echo "⚠️  anthropic 未安装"
    read -p "是否现在安装? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install anthropic langchain-anthropic
    fi
fi

if python3 -c "import langchain_anthropic" 2>/dev/null; then
    echo "✅ langchain-anthropic 已安装"
else
    echo "⚠️  langchain-anthropic 未安装"
    read -p "是否现在安装? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install langchain-anthropic
    fi
fi

echo ""
echo "========================================"
echo "环境配置完成！"
echo "========================================"
echo ""
echo "下一步："
echo "1. 运行测试: python tests/simple_test.py"
echo "2. 查看文档: docs/MIGRATION_TO_CLAUDE.md"
echo ""
echo "环境变量（需要在每个新会话中设置）："
echo "  export WORKSPACE_PATH=$WORKSPACE_PATH"
echo "  export ANTHROPIC_API_KEY='your-api-key'"
echo ""
