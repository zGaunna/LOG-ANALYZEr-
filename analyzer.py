import os
import sys
import collections
import datetime
import json
import csv

# Maximum number of detailed ERROR/WARNING messages to display
MAX_DETAILED_MESSAGES = 1000
# Version of the log analyzer
__version__ = "1.0.0"


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

# Try to import tkinter for folder selection (standard library)
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


def extract_messages_from_log_line(line):
    """Extract log message from a plain text line - returns the whole line.

    Args:
        line: A line of text from a log file

    Returns:
        str: The line with trailing newline removed
    """
    return line.rstrip('\n')


def extract_messages_from_json_file(filepath, log_and_print):
    """Extract messages from JSON file (JSON Lines or JSON array).

    Args:
        filepath: Path to the JSON file
        log_and_print: Function to log messages to console and file

    Returns:
        list: List of (line_num, message) tuples extracted from the file
    """
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Try to parse as JSON Lines (each line is a JSON object)
            line_num = 0
            for line in f:
                line_num += 1
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    # Extract string values from JSON object
                    if isinstance(data, dict):
                        # Extract message and level using helper function
                        message_value, level_value = extract_message_level(data)
                        if message_value is not None:
                            if level_value is not None:
                                # Combine level and message for checking
                                combined = f"{level_value}: {message_value}"
                                messages.append((line_num, combined))
                            else:
                                messages.append((line_num, message_value))
                        else:
                            # No common message field found, convert whole object to string
                            messages.append((line_num, json.dumps(data, ensure_ascii=False)))
                    elif isinstance(data, str):
                        messages.append((line_num, data))
                    else:
                        messages.append((line_num, json.dumps(data, ensure_ascii=False)))
                except json.JSONDecodeError:
                    # Not valid JSON Lines, try to parse whole file as JSON array
                    f.seek(0)
                    content = f.read()
                    # Strip whitespace
                    content = content.strip()
                    if not content:
                        return messages

                    # Check if it's a JSON array
                    if content.startswith('[') and content.endswith(']'):
                        # Use JSONDecoder to parse array elements one by one for exact line numbers
                        decoder = json.JSONDecoder()
                        pos = 1  # Skip the '['
                        array_len = len(content)
                        while pos < array_len - 1:
                            # Skip whitespace
                            while pos < array_len and content[pos] in ' \t\n\r':
                                pos += 1
                            if pos >= array_len - 1 or content[pos] == ']':
                                break
                            try:
                                obj, end = decoder.raw_decode(content, pos)
                                # Calculate line number: count newlines up to position
                                line_no = content[:pos].count('\n') + 1
                                # Process the object
                                if isinstance(obj, dict):
                                    message_value, level_value = extract_message_level(obj)
                                    if message_value is not None:
                                        if level_value is not None:
                                            combined = f"{level_value}: {message_value}"
                                            messages.append((line_no, combined))
                                        else:
                                            messages.append((line_no, message_value))
                                    else:
                                        # No common message field found
                                        messages.append((line_no, json.dumps(obj, ensure_ascii=False)))
                                elif isinstance(obj, str):
                                    messages.append((line_no, obj))
                                else:
                                    messages.append((line_no, json.dumps(obj, ensure_ascii=False)))
                                # Update position
                                pos = end
                                # Skip whitespace after object
                                while pos < array_len and content[pos] in ' \t\n\r':
                                    pos += 1
                                # Skip comma if present
                                if pos < array_len and content[pos] == ',':
                                    pos += 1
                            except json.JSONDecodeError:
                                # If we can't decode an element, break
                                break
                    else:
                        # Not an array, try to parse as a single JSON value
                        decoder = json.JSONDecoder()
                        try:
                            obj, end = decoder.raw_decode(content, 0)
                            line_no = 1  # Approximate as line 1 for single values
                            # Process the object
                            if isinstance(obj, dict):
                                message_value, level_value = extract_message_level(obj)
                                if message_value is not None:
                                    if level_value is not None:
                                        combined = f"{level_value}: {message_value}"
                                        messages.append((line_no, combined))
                                    else:
                                        messages.append((line_no, message_value))
                                else:
                                    messages.append((line_no, json.dumps(obj, ensure_ascii=False)))
                            elif isinstance(obj, str):
                                messages.append((line_no, obj))
                            else:
                                messages.append((line_no, json.dumps(obj, ensure_ascii=False)))
                        except json.JSONDecodeError as e:
                            log_and_print(f"Error parsing JSON file {filepath}: {e}")
    except Exception as e:
        log_and_print(f"Error reading JSON file {filepath}: {e}")
    return messages


def extract_messages_from_csv_file(filepath, log_and_print):
    """Extract messages from CSV file.

    Args:
        filepath: Path to the CSV file
        log_and_print: Function to log messages to console and file

    Returns:
        list: List of (line_num, message) tuples extracted from the file
    """
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Try to detect delimiter with increased sample size for better accuracy
            sample = f.read(4096)  # Increased from 1024 to 4096 bytes
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except Exception:
                delimiter = ','  # fallback

            reader = csv.reader(f, delimiter=delimiter)
            headers = None
            for row_num, row in enumerate(reader, start=1):
                if not row:  # empty row
                    continue

                if headers is None:
                    # First row might be headers
                    potential_headers = [cell.strip().lower() for cell in row]
                    # Use exact matches for log-related columns to avoid false positives
                    log_related_keywords = {'message', 'msg', 'log', 'level', 'timestamp', 'time', 'date'}
                    log_related_cols = [i for i, h in enumerate(potential_headers)
                                      if h in log_related_keywords]
                    # Require at least 2 log-related columns to treat as header
                    if len(log_related_cols) >= 2:
                        headers = potential_headers
                        # Use the first log-related column for message, and look for level column
                        msg_col = log_related_cols[0]
                        level_col = None
                        for key in ['level', 'Level']:
                            if key in headers:
                                level_col = headers.index(key)
                                break
                        continue  # skip header row
                    else:
                        # No obvious header, treat first row as data
                        headers = None
                        # fall through to process this row as data

                # Extract message from row
                if headers is None:
                    # No headers, concatenate all cells
                    message = ' '.join(str(cell) for cell in row if cell is not None)
                    if message.strip():
                        messages.append((row_num, message))
                else:
                    # Use headers to find message column
                    msg_value = None
                    # Look for common column names
                    for key in ['message', 'msg', 'log']:
                        if key in headers:
                            col_idx = headers.index(key)
                            if col_idx < len(row):
                                msg_value = row[col_idx]
                            break

                    # Look for level column
                    level_value = None
                    for key in ['level', 'Level']:
                        if key in headers:
                            level_idx = headers.index(key)
                            if level_idx < len(row):
                                level_value = row[level_idx]
                            break

                    if msg_value is None and headers:
                        # Fallback: concatenate all cells
                        msg_value = ' '.join(str(cell) for cell in row if cell is not None)

                    # Combine level and message if both present
                    if msg_value and msg_value.strip():
                        if level_value and level_value.strip():
                            combined = f"{level_value}: {msg_value}"
                            messages.append((row_num, combined))
                        else:
                            messages.append((row_num, msg_value))
    except Exception as e:
        log_and_print(f"Error reading CSV file {filepath}: {e}")
    return messages


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
            messages = extract_messages_from_json_file(filepath, log_and_print)
            total_lines = len(messages)
            error_messages = detect_errors_warnings(messages)
            error_warning_lines = len(error_messages)

        elif ext == '.csv':
            # CSV files
            messages = extract_messages_from_csv_file(filepath, log_and_print)
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