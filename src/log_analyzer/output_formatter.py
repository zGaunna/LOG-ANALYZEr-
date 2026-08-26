"""Output formatting functionality for the log analyzer."""

import json
from typing import List, Tuple


def format_table_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as a table."""
    if not error_messages:
        return "ERROR veya WARNING mesajı bulunamadı."

    # Header
    lines = []
    lines.append(f"{'Dosya':<30} {'Satır':<8} {'Mesaj'}")
    lines.append("-" * 80)

    # Data rows
    for filepath, line_num, message in error_messages:
        # Truncate long messages for table display
        display_message = message if len(message) <= 50 else message[:47] + "..."
        rel_path = filepath.split('/')[-1] if '/' in filepath else filepath.split('\\')[-1]  # Handle both path separators
        lines.append(f"{rel_path:<30} {line_num:<8} {display_message}")

    return '\n'.join(lines)


def format_json_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as JSON."""
    data = []
    for filepath, line_num, message in error_messages:
        data.append({
            "file": filepath,
            "line": line_num,
            "message": message
        })

    return json.dumps(data, indent=2, ensure_ascii=False)


def format_jsonl_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as JSON Lines (each line is a JSON object)."""
    lines = []
    for filepath, line_num, message in error_messages:
        obj = {
            "file": filepath,
            "line": line_num,
            "message": message
        }
        lines.append(json.dumps(obj, ensure_ascii=False))

    return '\n'.join(lines)


def format_html_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as an HTML table."""
    if not error_messages:
        return "<p>ERROR veya WARNING mesajı bulunamadı.</p>"

    html = ['<table border="1" cellpadding="5" cellspacing="0">']
    html.append('<thead><tr><th>Dosya</th><th>Satır</th><th>Mesaj</th></tr></thead>')
    html.append('<tbody>')
    for filepath, line_num, message in error_messages:
        # Escape HTML special characters in message
        escaped_message = message.replace('&', '&').replace('<', '<').replace('>', '>')
        rel_path = filepath.split('/')[-1] if '/' in filepath else filepath.split('\\')[-1]
        html.append(f'<tr><td>{rel_path}</td><td>{line_num}</td><td>{escaped_message}</td></tr>')
    html.append('</tbody></table>')

    return '\n'.join(html)