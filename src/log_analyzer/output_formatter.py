"""Format output for the log analyzer."""

from . import analyzer_core


def format_table_output(messages: list, filters: dict = None) -> str:
    """Format messages as a SQL-like table.

    Args:
        messages: List of (filepath, line_num, message) tuples
        filters: Optional dict with filters like {'level': 'ERROR', 'time_range': ('start', 'end')}

    Returns:
        Formatted table string
    """
    if not messages:
        return "No ERROR or WARNING messages found."

    # Parse messages to extract components using the shared parser
    parsed_messages = []
    for filepath, line_num, message in messages:
        timestamp, level, msg_content = analyzer_core.parse_log_message(message)

        parsed_messages.append({
            'timestamp': timestamp,
            'level': level,
            'message': msg_content,
            'filepath': filepath,
            'line_num': line_num
        })

    # Apply filters if provided
    if filters:
        filtered_messages = parsed_messages
        if 'level' in filters and filters['level']:
            filtered_messages = [m for m in filtered_messages if m['level'] == filters['level']]
        # Additional filters can be added here
        parsed_messages = filtered_messages

    if not parsed_messages:
        return "No messages match the specified filters."

    # Calculate column widths
    timestamp_width = max(len('TIMESTAMP'), max(len(m['timestamp']) for m in parsed_messages))
    level_width = max(len('LEVEL'), max(len(m['level']) for m in parsed_messages))
    message_width = max(len('MESSAGE'), max(len(m['message']) for m in parsed_messages))
    # Limit message width to prevent extremely wide tables
    message_width = min(message_width, 50)

    # Create header
    header = f"{'TIMESTAMP':<{timestamp_width}} {'LEVEL':<{level_width}} {'MESSAGE':<{message_width}} {'FILE:LINE'}"
    separator = f"{'-' * timestamp_width} {'-' * level_width} {'-' * message_width} {'-' * 20}"

    # Create rows
    rows = []
    for msg in parsed_messages:
        # Truncate message if too long
        display_message = msg['message']
        if len(display_message) > message_width:
            display_message = display_message[:message_width-3] + "..."

        file_line = f"{msg['filepath']}:{msg['line_num']}"
        if len(file_line) > 20:
            # Truncate filepath if needed
            parts = msg['filepath'].split('/')
            if len(parts) > 3:
                file_line = ".../" + '/'.join(parts[-3:]) + f":{msg['line_num']}"
            else:
                file_line = file_line[:20]

        row = f"{msg['timestamp']:<{timestamp_width}} {msg['level']:<{level_width}} {display_message:<{message_width}} {file_line}"
        rows.append(row)

    # Combine everything
    table_lines = [header, separator] + rows
    return '\n'.join(table_lines)


def format_summary_output(total_lines: int, error_warning_lines: int,
                         all_error_messages: list, files_processed: int) -> str:
    """Format summary output.

    Args:
        total_lines: Total lines processed
        error_warning_lines: Number of ERROR/WARNING lines
        all_error_messages: List of error/warning messages
        files_processed: Number of files processed

    Returns:
        Formatted summary string
    """
    lines = []
    lines.append(f"İşlenen dosya sayısı: {files_processed}")
    lines.append(f"Toplam satır sayısı: {total_lines}")
    lines.append(f"ERROR ve WARNING geçen satır sayısı: {error_warning_lines}")

    if all_error_messages:
        # Limit output to prevent flooding
        MAX_DETAILED_MESSAGES = 1000
        if len(all_error_messages) > MAX_DETAILED_MESSAGES:
            lines.append(f"Note: Showing first {MAX_DETAILED_MESSAGES} of {len(all_error_messages)} ERROR/WARNING messages")
            displayed_messages = all_error_messages[:MAX_DETAILED_MESSAGES]
        else:
            displayed_messages = all_error_messages

        lines.append("ERROR ve WARNING mesajları:")
        for filepath, line_num, message in displayed_messages:
            # Try to make output more readable
            rel_path = filepath  # In real implementation, this would be relative to scan dir
            lines.append(f"  [{rel_path}:{line_num}] {message}")
    else:
        lines.append("ERROR veya WARNING mesajı bulunamadı.")

    return '\n'.join(lines)