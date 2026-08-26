"""Output formatting functionality for the log analyzer."""

import html
import json
import os
from typing import List, Tuple


def _display_name(filepath: str) -> str:
    """Return the final path component in a platform-independent way."""
    return os.path.basename(os.path.normpath(filepath))


def format_table_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as a readable text table."""
    if not error_messages:
        return "ERROR veya WARNING mesajı bulunamadı."

    lines = []
    lines.append(f"{'Dosya':<30} {'Satır':<8} {'Mesaj'}")
    lines.append("-" * 80)

    for filepath, line_num, message in error_messages:
        display_message = message if len(message) <= 50 else message[:47] + "..."
        rel_path = _display_name(filepath)
        lines.append(f"{rel_path:<30} {line_num:<8} {display_message}")

    return "\n".join(lines)


def format_json_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as JSON."""
    data = [
        {"file": filepath, "line": line_num, "message": message}
        for filepath, line_num, message in error_messages
    ]
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_jsonl_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as JSON Lines."""
    return "\n".join(
        json.dumps(
            {"file": filepath, "line": line_num, "message": message},
            ensure_ascii=False,
        )
        for filepath, line_num, message in error_messages
    )


def format_html_output(error_messages: List[Tuple[str, int, str]]) -> str:
    """Format error messages as an HTML table with safe escaping."""
    if not error_messages:
        return "<p>ERROR veya WARNING mesajı bulunamadı.</p>"

    html_lines = ['<table border="1" cellpadding="5" cellspacing="0">']
    html_lines.append('<thead><tr><th>Dosya</th><th>Satır</th><th>Mesaj</th></tr></thead>')
    html_lines.append('<tbody>')

    for filepath, line_num, message in error_messages:
        rel_path = html.escape(_display_name(filepath))
        escaped_message = html.escape(message)
        html_lines.append(
            f"<tr><td>{rel_path}</td><td>{line_num}</td><td>{escaped_message}</td></tr>"
        )

    html_lines.append('</tbody></table>')
    return '\n'.join(html_lines)
