"""Handle plain text log files."""

def extract_messages_from_log_line(line):
    """Extract log message from a plain text line - returns the whole line.

    Args:
        line: A line of text from a log file

    Returns:
        str: The line with trailing newline removed
    """
    return line.rstrip('\n')