"""Core analysis functionality for the log analyzer."""

import os
import sys
import collections
import datetime
import json
import csv

# Maximum number of detailed ERROR/WARNING messages to display
MAX_DETAILED_MESSAGES = 1000
# Version of the log analyzer
__version__ = "1.1.0"


def extract_message_level(obj):
    """Extract message and level from a JSON object.

    Args:
        obj: A dictionary representing a JSON object

    Returns:
        tuple: (message_value, level_value) where each can be None if not found
    """
    message_value = None
    level_value = None

    if isinstance(obj, dict):
        # Look for common log message fields
        for key in ['message', 'msg', 'log', 'Message', 'Msg', 'Log']:
            if key in obj and isinstance(obj[key], str):
                message_value = obj[key]
                break

        # Look for level field
        for key in ['level', 'Level']:
            if key in obj and isinstance(obj[key], str):
                level_value = obj[key]
                break

    return message_value, level_value


def contains_error_warning(text):
    """Check if text contains ERROR or WARNING (case-insensitive).

    Args:
        text: String to check

    Returns:
        bool: True if text contains ERROR or WARNING, False otherwise
    """
    if not isinstance(text, str):
        return False
    upper_text = text.upper()
    return 'ERROR' in upper_text or 'WARNING' in upper_text


def detect_errors_warnings(lines):
    """Filter lines to find those containing ERROR or WARNING.

    Args:
        lines: Iterable of (line_num, message) tuples

    Returns:
        list: Filtered list of (line_num, message) tuples containing ERROR/WARNING
    """
    result = []
    for line_num, message in lines:
        if contains_error_warning(message):
            result.append((line_num, message))
    return result


# Try to set console output to UTF-8 on Windows for better Turkish character support
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass
    # Also reconfigure stdout and stderr to use UTF-8 encoding
    try:
        import sys
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass


# Try to import tkinter for folder selection (standard library)
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


def analyze_file(filepath, log_and_print):
    """Analyze a single file based on its extension.

    Args:
        filepath: Path to the file to analyze
        log_and_print: Function to log messages to console and file

    Returns:
        tuple: (total_lines, error_warning_lines, error_messages)
            total_lines: Total number of lines/items processed
            error_warning_lines: Number of lines containing ERROR or WARNING
            error_messages: List of (line_num, message) tuples for ERROR/WARNING lines
    """
    # Import handlers locally to avoid circular imports
    from . import csv_handler, json_handler, text_handler

    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()

    total_lines = 0
    error_warning_lines = 0
    error_messages = []  # list of (line_num, message) tuples

    try:
        if ext in ['.log', '.txt']:
            # Plain text files - line by line
            with open(filepath, 'r', encoding='utf-8') as f:
                lines_with_nums = [(line_num, line.rstrip('\n')) for line_num, line in enumerate(f, start=1)]
                error_messages = detect_errors_warnings(lines_with_nums)
                total_lines = len(lines_with_nums)
                error_warning_lines = len(error_messages)

        elif ext in ['.json', '.jsonl']:
            # JSON files (including JSON Lines)
            messages = json_handler.extract_messages_from_json_file(filepath, log_and_print)
            total_lines = len(messages)
            error_messages = detect_errors_warnings(messages)
            error_warning_lines = len(error_messages)

        elif ext == '.csv':
            # CSV files
            messages = csv_handler.extract_messages_from_csv_file(filepath, log_and_print)
            total_lines = len(messages)
            error_messages = detect_errors_warnings(messages)
            error_warning_lines = len(error_messages)

        else:
            # Unsupported format - treat as plain text but warn
            log_and_print(f"Warning: Unsupported file extension '{ext}' for {filename}, treating as plain text")
            with open(filepath, 'r', encoding='utf-8') as f:
                lines_with_nums = [(line_num, line.rstrip('\n')) for line_num, line in enumerate(f, start=1)]
                error_messages = detect_errors_warnings(lines_with_nums)
                total_lines = len(lines_with_nums)
                error_warning_lines = len(error_messages)

    except UnicodeDecodeError:
        # Try with different encoding for plain text files
        if ext in ['.log', '.txt']:
            try:
                with open(filepath, 'r', encoding='latin-1') as f:
                    for line_num, line in enumerate(f, start=1):
                        line = line.rstrip('\n')
                        total_lines += 1
                        upper_line = line.upper()
                        if 'ERROR' in upper_line or 'WARNING' in upper_line:
                            error_warning_lines += 1
                            error_messages.append((line_num, line))
            except Exception as e:
                log_and_print(f"Error reading {filepath} with latin-1 encoding: {e}")
        else:
            log_and_print(f"Error reading {filepath}: Unicode decode error")
    except Exception as e:
        log_and_print(f"Error processing {filepath}: {e}")

    return total_lines, error_warning_lines, error_messages


def analyze_logs(directory, log_and_print):
    """Analyze all supported files in directory recursively.

    Args:
        directory: Path to the directory to analyze
        log_and_print: Function to log messages to console and file

    Returns:
        tuple: (total_lines, error_warning_lines, all_error_messages)
            total_lines: Total number of lines/items processed across all files
            error_warning_lines: Number of lines containing ERROR or WARNING across all files
            all_error_messages: List of (filepath, line_num, message) tuples for all ERROR/WARNING lines
    """
    total_lines = 0
    error_warning_lines = 0
    all_error_messages = []  # list of (filepath, line_num, message)
    supported_extensions = {'.log', '.txt', '.json', '.jsonl', '.csv'}
    files_processed = 0

    # Walk through directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            if ext in supported_extensions:
                files_processed += 1
                file_total_lines, file_error_warning, file_error_messages = analyze_file(filepath, log_and_print)

                total_lines += file_total_lines
                error_warning_lines += file_error_warning

                # Store error messages with file info
                for line_num, message in file_error_messages:
                    all_error_messages.append((filepath, line_num, message))
            else:
                # Skip unsupported files silently (or optionally log)
                pass

    # Limit detailed output to avoid flooding console
    if len(all_error_messages) > MAX_DETAILED_MESSAGES:
        log_and_print(f"Note: Showing first {MAX_DETAILED_MESSAGES} of {len(all_error_messages)} ERROR/WARNING messages")
        displayed_messages = all_error_messages[:MAX_DETAILED_MESSAGES]
    else:
        displayed_messages = all_error_messages

    log_and_print(f"İşlenen dosya sayısı: {files_processed}")
    log_and_print(f"Toplam satır sayısı: {total_lines}")
    log_and_print(f"ERROR ve WARNING geçen satır sayısı: {error_warning_lines}")

    if displayed_messages:
        log_and_print("ERROR ve WARNING mesajları:")
        for filepath, line_num, message in displayed_messages:
            rel_path = os.path.relpath(filepath, directory)
            log_and_print(f"  [{rel_path}:{line_num}] {message}")
    else:
        log_and_print("ERROR veya WARNING mesajı bulunamadı.")

    return total_lines, error_warning_lines, all_error_messages


def parse_log_message(message: str) -> tuple:
    """Parse a log message to extract timestamp, level, and content.

    Args:
        message: Raw log message string

    Returns:
        tuple: (timestamp, level, content) where each can be "Unknown" if not found
    """
    import re

    # Default values
    timestamp = "Unknown"
    level = "Unknown"
    msg_content = message

    # Check if message already has level: message format (contains ': ')
    if ': ' in message and message.count(': ') >= 1:
        parts = message.split(': ', 1)
        potential_level = parts[0].strip()
        if potential_level in ['ERROR', 'WARNING', 'INFO', 'DEBUG']:
            level = potential_level
            msg_content = parts[1].strip()
            # Try to extract timestamp from beginning
            if ' ' in msg_content and len(msg_content.split(' ')[0]) == 10:  # YYYY-MM-DD format
                date_part = msg_content.split(' ')[0]
                time_part = msg_content.split(' ')[1] if len(msg_content.split(' ')) > 1 else ""
                if re.match(r'\d{4}-\d{2}-\d{2}', date_part) and re.match(r'\d{2}:\d{2}:\d{2}', time_part):
                    timestamp = f"{date_part} {time_part}"
                    msg_content = ' '.join(msg_content.split(' ')[2:]) if len(msg_content.split(' ')) > 2 else ""
        else:
            # Try to find timestamp at start for messages with ': ' but non-standard level
            timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', message)
            if timestamp_match:
                timestamp = timestamp_match.group(1)
                remaining = message[timestamp_match.end():].strip()
                if remaining.startswith('ERROR ') or remaining.startswith('WARNING ') or remaining.startswith('INFO ') or remaining.startswith('DEBUG '):
                    level_part, msg_part = remaining.split(' ', 1)
                    level = level_part
                    msg_content = msg_part
                else:
                    msg_content = remaining

    # Try to find timestamp at start for messages without ': ' (standard format: "TIMESTAMP LEVEL message")
    timestamp_match = re.match(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})', message)
    if timestamp_match:
        timestamp = timestamp_match.group(1)
        remaining = message[timestamp_match.end():].strip()
        if remaining.startswith('ERROR ') or remaining.startswith('WARNING ') or remaining.startswith('INFO ') or remaining.startswith('DEBUG '):
            level_part, msg_part = remaining.split(' ', 1)
            level = level_part
            msg_content = msg_part
        else:
            msg_content = remaining

    return timestamp, level, msg_content


def cleanup_old_logs(keep_count=5):
    """Cleanup old log files, keeping only the most recent ones.

    Args:
        keep_count: Number of recent log files to keep (default: 5)
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Find all analyzer_*.log files
        log_files = []
        for f in os.listdir(script_dir):
            if f.startswith('analyzer_') and f.endswith('.log'):
                log_files.append(f)

        # Sort by modification time (oldest first)
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(script_dir, x)))

        # Remove excess files
        if len(log_files) > keep_count:
            files_to_remove = log_files[:-keep_count]
            for f in files_to_remove:
                try:
                    os.remove(os.path.join(script_dir, f))
                except OSError:
                    # Ignore errors during cleanup
                    pass
    except Exception:
        # If cleanup fails, continue without it
        pass


def wait_for_exit():
    """Wait for user to press a key before exiting, keeping console window open.

    Waits for Enter in interactive terminals or any key in non-interactive contexts.
    """
    try:
        if sys.stdin.isatty():
            # Interactive terminal (e.g., command prompt)
            input("İşlem tamamlandı. Çıkmak için Enter tuşuna basın...")
        else:
            # Likely launched by double-click (no stdin tty)
            print("İşlem tamamlandı. Çıkmak için bir tuşa basın...")
            # Wait for a single key press
            sys.stdin.read(1)
    except:
        # If anything goes wrong, just continue to exit
        pass


def select_folder_gui():
    """Open folder selection dialog using tkinter.

    Returns:
        str or None: Selected folder path, or None if no folder selected or GUI unavailable
    """
    if not TKINTER_AVAILABLE:
        print("GUI destekleme (tkinter) kullanılamıyor.")
        return None

    root = tk.Tk()
    root.withdraw()  # Hide the main window
    root.attributes('-topmost', True)  # Bring to front
    try:
        folder_path = filedialog.askdirectory(
            title="Lütfen analiz edilecek klasörü seçin",
            mustexist=True
        )
        return folder_path if folder_path else None
    except Exception as e:
        print(f"Klasör seçici açılırken hata: {e}")
        return None
    finally:
        root.destroy()


def main():
    # Determine script directory for log file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = os.path.join(script_dir, f"analyzer_{timestamp}.log")

    # Cleanup old log files before creating new one
    cleanup_old_logs(keep_count=5)

    # Open log file
    log_file = None
    try:
        log_file = open(log_file_path, 'w', encoding='utf-8')
    except Exception as e:
        print(f"Failed to create log file: {e}")
        # Fallback: only console output
        log_file = None

    # Function to print to console and log file
    def log_and_print(message):
        print(message)
        if log_file is not None:
            log_file.write(message + '\n')
            log_file.flush()

    try:
        # Check if directory argument provided
        if len(sys.argv) == 2:
            directory = sys.argv[1]
            if not os.path.isdir(directory):
                log_and_print(f"Hata: {directory} geçerli bir dizin değil")
                return
        else:
            # No argument - try to use GUI folder selection
            log_and_print("Klasör argümanı sağlanmadı. Klasör seçici açılıyor...")
            directory = select_folder_gui()
            if directory is None:
                log_and_print("Klasör seçilmedi veya GUI kullanılamıyor. Program sonlandırılıyor.")
                return
            log_and_print(f"Seçilen klasör: {directory}")

        log_and_print(f"Log dosyası: {log_file_path}")
        analyze_logs(directory, log_and_print)
        log_and_print(f"İşlem tamamlandı. Sonuçlar [{log_file_path}] dosyasına kaydedildi.")
    except Exception as e:
        log_and_print(f"Beklenmeyen hata: {e}")
    finally:
        if log_file is not None:
            log_file.close()
        wait_for_exit()


if __name__ == "__main__":
    main()