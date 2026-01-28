#!/bin/bash
# Quick setup script for Linux/Mac

echo "============================================================"
echo "AI Development Toolkit - Quick Setup"
echo "============================================================"
echo

# Check if .env exists
if [ -f .env ]; then
    echo "[INFO] .env file already exists"
    echo
    read -p "Do you want to overwrite it? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping .env creation..."
    else
        cp .env.example .env 2>/dev/null || echo "ANTHROPIC_API_KEY=your-anthropic-api-key-here" > .env
        echo "[OK] Created .env file"
    fi
else
    # Create .env from example
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "[OK] Created .env file from .env.example"
    else
        echo "ANTHROPIC_API_KEY=your-anthropic-api-key-here" > .env
        echo "[OK] Created .env file"
    fi
fi

echo
echo "============================================================"
echo "IMPORTANT: Please edit .env file and add your API key"
echo "============================================================"
echo
echo "1. Open .env file in a text editor:"
echo "   nano .env"
echo "   # or"
echo "   vim .env"
echo
echo "2. Replace 'your-anthropic-api-key-here' with your actual API key"
echo "3. Save the file"
echo
echo "Get your API key at: https://console.anthropic.com/"
echo

# Check configuration
echo "Checking configuration..."
python3 env_config.py || python env_config.py
echo

if [ $? -eq 0 ]; then
    echo
    echo "============================================================"
    echo "[SUCCESS] Setup complete! You can now run:"
    echo "  python main.py code \"your requirement\""
    echo "============================================================"
else
    echo "[ERROR] Please configure your API key in .env file"
    exit 1
fi
