"""
Safe print utility for Windows console
Handles emoji and Unicode characters that may cause encoding issues
"""
import sys
import json


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


def clean_json_response(content: str) -> str:
    """
    Clean JSON response by removing markdown code blocks and extra text

    Args:
        content: Raw response content that may contain markdown

    Returns:
        Cleaned JSON string
    """
    content = content.strip()

    # Remove markdown code blocks
    if content.startswith("```json"):
        content = content[7:]
    elif content.startswith("```"):
        content = content[3:]

    if content.endswith("```"):
        content = content[:-3]

    content = content.strip()

    # Try to find JSON object boundaries
    # Look for the first { and last }
    start_idx = content.find('{')
    end_idx = content.rfind('}')

    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        content = content[start_idx:end_idx + 1]

    return content.strip()


def parse_json_response(content: str) -> dict:
    """
    Parse JSON response, handling markdown code blocks and extra text

    Args:
        content: Raw response content

    Returns:
        Parsed JSON dict

    Raises:
        json.JSONDecodeError: If JSON parsing fails
    """
    cleaned = clean_json_response(content)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Try to provide more helpful error information
        error_pos = e.pos if hasattr(e, 'pos') else 0
        context_start = max(0, error_pos - 100)
        context_end = min(len(cleaned), error_pos + 100)
        context = cleaned[context_start:context_end]

        raise json.JSONDecodeError(
            f"{e.msg}. Context around error: ...{context}...",
            e.doc,
            e.pos
        )
