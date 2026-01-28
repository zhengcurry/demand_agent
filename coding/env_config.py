"""
Environment configuration loader
Loads API keys and other sensitive configuration from .env file
"""
import os
from pathlib import Path
from typing import Optional


def load_env_file(env_path: str = ".env") -> dict:
    """
    Load environment variables from .env file

    Args:
        env_path: Path to .env file

    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    env_file = Path(env_path)

    if not env_file.exists():
        return env_vars

    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue

                # Parse KEY=VALUE
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]

                    env_vars[key] = value
                    # Also set in os.environ
                    os.environ[key] = value
    except Exception as e:
        print(f"Warning: Failed to load .env file: {e}")

    return env_vars


def get_api_key() -> Optional[str]:
    """
    Get Anthropic API key from environment

    Returns:
        API key or None if not found
    """
    # First try to load from .env file
    load_env_file()

    # Then get from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("\n" + "="*60)
        print("WARNING: ANTHROPIC_API_KEY not set!")
        print("="*60)
        print("\nPlease set API key using one of these methods:\n")
        print("Method 1: Create .env file (Recommended)")
        print("  1. Copy .env.example to .env")
        print("  2. Edit .env file and add your API key:")
        print("     ANTHROPIC_API_KEY=your-actual-api-key")
        print()
        print("Method 2: Set environment variable")
        print("  Windows (CMD):")
        print("    set ANTHROPIC_API_KEY=your-actual-api-key")
        print("  Windows (PowerShell):")
        print("    $env:ANTHROPIC_API_KEY=\"your-actual-api-key\"")
        print("  Linux/Mac:")
        print("    export ANTHROPIC_API_KEY=\"your-actual-api-key\"")
        print()
        print("Method 3: Pass directly in code")
        print("  skill = CodeSkill(api_key='your-actual-api-key')")
        print("\n" + "="*60)
        print("Get API key at: https://console.anthropic.com/")
        print("="*60 + "\n")

    return api_key


def check_environment() -> bool:
    """
    Check if environment is properly configured

    Returns:
        True if configured, False otherwise
    """
    api_key = get_api_key()
    return api_key is not None and len(api_key) > 0


if __name__ == "__main__":
    # Test configuration
    if check_environment():
        print("[OK] Environment configured correctly!")
        print(f"API key is set (length: {len(os.getenv('ANTHROPIC_API_KEY'))} characters)")
    else:
        print("[ERROR] Environment not configured. Please follow the instructions above.")
