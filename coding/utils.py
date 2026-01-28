"""
Safe print utility for Windows console
Handles emoji and Unicode characters that may cause encoding issues
"""
import sys


def safe_print(text: str, **kwargs):
    """
    Safely print text, handling encoding issues on Windows

    Args:
        text: Text to print
        **kwargs: Additional arguments for print()
    """
    try:
        print(text, **kwargs)
    except UnicodeEncodeError:
        # Remove emoji and special characters
        safe_text = text.encode('ascii', 'ignore').decode('ascii')
        print(safe_text, **kwargs)


# Emoji replacements for Windows console
EMOJI_MAP = {
    '🚀': '[START]',
    '📋': '[STEP]',
    '✅': '[OK]',
    '🏗️': '[STEP]',
    '🔌': '[STEP]',
    '📝': '[STEP]',
    '💻': '[STEP]',
    '🔍': '[STEP]',
    '🎉': '[SUCCESS]',
    '⚠️': '[WARNING]',
    '❌': '[ERROR]',
    '📊': '[INFO]',
    '📄': '[INFO]',
    '🎨': '[START]',
    '🔧': '[INFO]',
}


def format_text(text: str) -> str:
    """
    Replace emoji with ASCII equivalents for Windows console

    Args:
        text: Text with emoji

    Returns:
        Text with emoji replaced
    """
    for emoji, replacement in EMOJI_MAP.items():
        text = text.replace(emoji, replacement)
    return text


def print_safe(text: str, **kwargs):
    """
    Print with emoji replacement for Windows compatibility

    Args:
        text: Text to print
        **kwargs: Additional arguments for print()
    """
    safe_text = format_text(text)
    print(safe_text, **kwargs)
