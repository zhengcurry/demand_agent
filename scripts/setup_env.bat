@echo off
REM 环境配置脚本 - 从扣子迁移到 Claude (Windows)

echo ========================================
echo 三层AI Agent系统 - 环境配置
echo ========================================
echo.

REM 检查是否已设置 ANTHROPIC_API_KEY
if "%ANTHROPIC_API_KEY%"=="" (
    echo 警告: 未检测到 ANTHROPIC_API_KEY 环境变量
    echo.
    echo 请按照以下步骤设置:
    echo 1. 访问 https://console.anthropic.com/
    echo 2. 创建或获取 API Key
    echo 3. 运行: set ANTHROPIC_API_KEY=your-api-key
    echo.
    set /p api_key="请输入 ANTHROPIC_API_KEY (或按回车跳过): "
    if not "%api_key%"=="" (
        set ANTHROPIC_API_KEY=%api_key%
        echo 已设置 API Key (仅本次会话有效^)
    ) else (
        echo 未设置 API Key，程序可能无法运行
    )
) else (
    echo 已检测到 ANTHROPIC_API_KEY
)

REM 设置 WORKSPACE_PATH
set WORKSPACE_PATH=%cd%
echo 已设置 WORKSPACE_PATH: %WORKSPACE_PATH%
echo.

REM 检查 Python 版本
python --version 2>nul
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖
echo.
echo 正在检查依赖...

python -c "import anthropic" 2>nul
if errorlevel 1 (
    echo 警告: anthropic 未安装
    set /p install="是否现在安装? (y/n): "
    if /i "%install%"=="y" (
        pip install anthropic langchain-anthropic
    )
) else (
    echo 已安装 anthropic
)

python -c "import langchain_anthropic" 2>nul
if errorlevel 1 (
    echo 警告: langchain-anthropic 未安装
    set /p install="是否现在安装? (y/n): "
    if /i "%install%"=="y" (
        pip install langchain-anthropic
    )
) else (
    echo 已安装 langchain-anthropic
)

echo.
echo ========================================
echo 环境配置完成！
echo ========================================
echo.
echo 下一步:
echo 1. 运行测试: python tests\simple_test.py
echo 2. 查看文档: docs\MIGRATION_TO_CLAUDE.md
echo.
echo 环境变量 (需要在每个新会话中设置):
echo   set WORKSPACE_PATH=%WORKSPACE_PATH%
echo   set ANTHROPIC_API_KEY=your-api-key
echo.
pause
