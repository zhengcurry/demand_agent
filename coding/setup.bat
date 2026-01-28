@echo off
REM Quick setup script for Windows
echo ============================================================
echo AI Development Toolkit - Quick Setup
echo ============================================================
echo.

REM Check if .env exists
if exist .env (
    echo [INFO] .env file already exists
    echo.
    choice /C YN /M "Do you want to overwrite it"
    if errorlevel 2 goto :check_key
)

REM Create .env from example
if exist .env.example (
    copy .env.example .env >nul
    echo [OK] Created .env file from .env.example
) else (
    echo ANTHROPIC_API_KEY=your-anthropic-api-key-here > .env
    echo [OK] Created .env file
)

echo.
echo ============================================================
echo IMPORTANT: Please edit .env file and add your API key
echo ============================================================
echo.
echo 1. Open .env file in a text editor
echo 2. Replace 'your-anthropic-api-key-here' with your actual API key
echo 3. Save the file
echo.
echo Get your API key at: https://console.anthropic.com/
echo.

:check_key
echo Checking configuration...
python env_config.py
echo.

if errorlevel 1 (
    echo [ERROR] Please configure your API key in .env file
    pause
    exit /b 1
)

echo.
echo ============================================================
echo [SUCCESS] Setup complete! You can now run:
echo   python main.py code "your requirement"
echo ============================================================
pause
