# API Reference

## log_analyzer.analyzer_core

### extract_message_level(obj)
Extract message and level from a JSON object.

**Args:**
    obj: A dictionary representing a JSON object

**Returns:**
    tuple: (message_value, level_value) where each can be None if not found

### contains_error_warning(text)
Check if text contains ERROR or WARNING (case-insensitive).

**Args:**
    text: String to check

**Returns:**
    bool: True if text contains ERROR or WARNING, False otherwise

### detect_errors_warnings(lines)
Filter lines to find those containing ERROR or WARNING.

**Args:**
    lines: Iterable of (line_num, message) tuples

**Returns:**
    list: Filtered list of (line_num, message) tuples containing ERROR/WARNING

### parse_log_message(message)
Parse a log message to extract timestamp, level, and content.

**Args:**
        message: Raw log message string

    Returns:
        tuple: (timestamp, level, content) where each can be "Unknown" if not found

### analyze_file(filepath, log_and_print)
Analyze a single file based on its extension.

**Args:**
        filepath: Path to the file to analyze
        log_and_print: Function to log messages to console and file

    Returns:
        tuple: (total_lines, error_warning_lines, error_messages)
            total_lines: Total number of lines/items processed
            error_warning_lines: Number of lines containing ERROR or WARNING
            error_messages: List of (line_num, message) tuples for ERROR/WARNING lines

### analyze_logs(directory, log_and_print)
Analyze all supported files in directory recursively.

**Args:**
        directory: Path to the directory to analyze
        log_and_print: Function to log messages to console and file

    Returns:
        tuple: (total_lines, error_warning_lines, all_error_messages)
            total_lines: Total number of lines/items processed across all files
            error_warning_lines: Number of lines containing ERROR or WARNING across all files
            all_error_messages: List of (filepath, line_num, message) tuples for all ERROR/WARNING lines

### wait_for_exit()
Wait for user to press a key before exiting, keeping console window open.

Waits for Enter in interactive terminals or any key in non-interactive contexts.

### select_folder_gui()
Open folder selection dialog using tkinter.

**Returns:**
        str or None: Selected folder path, or None if no folder selected or GUI unavailable

### main()
Main entry point for the log analyzer.

### cleanup_old_logs(keep_count=5)
Cleanup old log files, keeping only the most recent ones.

**Args:**
        keep_count: Number of recent log files to keep (default: 5)

## log_analyzer.csv_handler

### extract_messages_from_csv_file(filepath, log_and_print)
Extract messages from CSV file.

**Args:**
        filepath: Path to the CSV file
        log_and_print: Function to log messages to console and file

    Returns:
        list: List of (line_num, message) tuples extracted from the file

## log_analyzer.json_handler

### extract_message_level(obj)
Extract message and level from a JSON object.

**Args:**
        obj: A dictionary representing a JSON object

    Returns:
        tuple: (message_value, level_value) where each can be None if not found

### extract_messages_from_json_file(filepath, log_and_print)
Extract messages from JSON file (JSON Lines or JSON array).

**Args:**
        filepath: Path to the JSON file
        log_and_print: Function to log messages to console and file

    Returns:
        list: List of (line_num, message) tuples extracted from the file

## log_analyzer.text_handler

### extract_messages_from_log_line(line)
Extract log message from a plain text line - returns the whole line.

**Args:**
        line: A line of text from a log file

    Returns:
        str: The line with trailing newline removed

## log_analyzer.advanced_analyzer

### analyze_time_series(messages)
Analyze ERROR/WARNING messages over time.

**Args:**
        messages: List of (timestamp, level, message) tuples

    Returns:
        Dictionary with time series analysis results

### analyze_error_patterns(messages)
Analyze patterns in error messages.

**Args:**
        messages: List of (timestamp, level, message) tuples

    Returns:
        Dictionary with error pattern analysis

### detect_anomalies(messages, threshold=2.0)
Detect anomalous log volumes using statistical methods.

**Args:**
        messages: List of (timestamp, level, message) tuples
        threshold: Number of standard deviations for anomaly detection

    Returns:
        Dictionary with anomaly detection results

### analyze_correlations(messages)
Analyze correlations between events and errors.

**Args:**
        messages: List of (timestamp, level, message) tuples

    Returns:
        Dictionary with correlation analysis

### generate_summary_statistics(messages)
Generate summary statistics from log messages.

**Args:**
        messages: List of (timestamp, level, message) tuples

    Returns:
        Dictionary with summary statistics

## log_analyzer.output_formatter

### format_table_output(messages, filters=None)
Format messages as a SQL-like table.

**Args:**
        messages: List of (filepath, line_num, message) tuples
        filters: Optional dict with filters like {'level': 'ERROR', 'time_range': ('start', 'end')}

    Returns:
        Formatted table string

### format_summary_output(total_lines, error_warning_lines, all_error_messages, files_processed)
Format summary output.

**Args:**
        total_lines: Total lines processed
        error_warning_lines: Number of ERROR/WARNING lines
        all_error_messages: List of error/warning messages
        files_processed: Number of files processed

    Returns:
        Formatted summary string

## log_analyzer.__main__

### main()
Main entry point for the log analyzer when run as a script or module.