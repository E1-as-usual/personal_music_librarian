INVALID_CHARS = '<>:"/\\|?*'
RESERVED_NAMES = {
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9',
}


def sanitize_segment(value: str | None, fallback: str = 'Unknown') -> str:
    text = (value or fallback).strip()

    for char in INVALID_CHARS:
        text = text.replace(char, '_')

    text = ' '.join(text.split())
    text = text.rstrip(' .')

    if not text:
        text = fallback

    if text.upper() in RESERVED_NAMES:
        text = f'_{text}'

    return text[:120]
