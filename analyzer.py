import os
import sys
import collections
import datetime
import json
import csv

# Try to set console output to UTF-8 on Windows for better Turkish character support
if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleOutputCP(65001)
    except:
        pass

# Try to import tkinter for folder selection (standard library)
try:
    import tkinter as tk
    from tkinter import filedialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

def extract_messages_from_log_line(line):
    """Extract log message from a plain text line - returns the whole line."""
    return line.rstrip('\n')

def extract_messages_from_json_file(filepath, log_and_print):
    """Extract messages from JSON file (JSON Lines or JSON array)."""
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
                        # Look for common log message fields
                        message_value = None
                        for key in ['message', 'msg', 'log', 'Message', 'Msg', 'Log']:
                            if key in data and isinstance(data[key], str):
                                message_value = data[key]
                                break
                        # Look for level field
                        level_value = None
                        for key in ['level', 'Level']:
                            if key in data and isinstance(data[key], str):
                                level_value = data[key]
                                break
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
                    try:
                        data = json.load(f)
                        if isinstance(data, list):
                            for i, item in enumerate(data):
                                if isinstance(item, dict):
                                    for key in ['message', 'msg', 'log', 'Message', 'Msg', 'Log']:
                                        if key in item and isinstance(item[key], str):
                                            messages.append((i+1, item[key]))
                                            break
                                    else:
                                        messages.append((i+1, json.dumps(item, ensure_ascii=False)))
                                elif isinstance(item, str):
                                    messages.append((i+1, item))
                                else:
                                    messages.append((i+1, json.dumps(item, ensure_ascii=False)))
                        elif isinstance(data, dict):
                            for key in ['message', 'msg', 'log', 'Message', 'Msg', 'Log']:
                                if key in data and isinstance(data[key], str):
                                    messages.append((1, data[key]))
                                    break
                            else:
                                messages.append((1, json.dumps(data, ensure_ascii=False)))
                        elif isinstance(data, str):
                            messages.append((1, data))
                        else:
                            messages.append((1, json.dumps(data, ensure_ascii=False)))
                    except json.JSONDecodeError as e:
                        log_and_print(f"Error parsing JSON file {filepath}: {e}")
    except Exception as e:
        log_and_print(f"Error reading JSON file {filepath}: {e}")
    return messages

def extract_messages_from_csv_file(filepath, log_and_print):
    """Extract messages from CSV file."""
    messages = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Try to detect delimiter
            sample = f.read(1024)
            f.seek(0)
            sniffer = csv.Sniffer()
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except:
                delimiter = ','  # fallback

            reader = csv.reader(f, delimiter=delimiter)
            headers = None
            for row_num, row in enumerate(reader, start=1):
                if not row:  # empty row
                    continue

                if headers is None:
                    # First row might be headers
                    headers = [cell.strip().lower() for cell in row]
                    # Check if this looks like a header row with log-related columns
                    log_related_cols = [i for i, h in enumerate(headers)
                                      if any(keyword in h for keyword in ['message', 'msg', 'log', 'level'])]
                    if log_related_cols:
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
                        row_num = 1  # reset row numbering

                # Extract message from row
                if headers is None:
                    # No headers, concatenate all cells
                    message = ' '.join(str(cell) for cell in row if cell)
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
                        msg_value = ' '.join(str(cell) for cell in row if cell)

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
    """Analyze a single file based on its extension."""
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()

    total_lines = 0
    error_warning_lines = 0
    error_messages = []  # list of (line_num, message) tuples

    try:
        if ext in ['.log', '.txt']:
            # Plain text files - line by line
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    line = line.rstrip('\n')
                    total_lines += 1
                    upper_line = line.upper()
                    if 'ERROR' in upper_line or 'WARNING' in upper_line:
                        error_warning_lines += 1
                        error_messages.append((line_num, line))

        elif ext in ['.json', '.jsonl']:
            # JSON files (including JSON Lines)
            messages = extract_messages_from_json_file(filepath, log_and_print)
            total_lines = len(messages)
            for line_num, message in messages:
                upper_message = message.upper()
                if 'ERROR' in upper_message or 'WARNING' in upper_message:
                    error_warning_lines += 1
                    error_messages.append((line_num, message))

        elif ext == '.csv':
            # CSV files
            messages = extract_messages_from_csv_file(filepath, log_and_print)
            total_lines = len(messages)
            for line_num, message in messages:
                upper_message = message.upper()
                if 'ERROR' in upper_message or 'WARNING' in upper_message:
                    error_warning_lines += 1
                    error_messages.append((line_num, message))

        else:
            # Unsupported format - treat as plain text but warn
            log_and_print(f"Warning: Unsupported file extension '{ext}' for {filename}, treating as plain text")
            with open(filepath, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    line = line.rstrip('\n')
                    total_lines += 1
                    upper_line = line.upper()
                    if 'ERROR' in upper_line or 'WARNING' in upper_line:
                        error_warning_lines += 1
                        error_messages.append((line_num, line))

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
    """Analyze all supported files in directory recursively."""
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
    MAX_DETAILED_MESSAGES = 1000
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
    """Wait for user to press a key before exiting, keeping console window open."""
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
    """Open folder selection dialog using tkinter."""
    if not TKINTER_AVAILABLE:
        print("GUI destekleme (tkinter) kullanılamıyor.")
        return None

    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        root.attributes('-topmost', True)  # Bring to front
        folder_path = filedialog.askdirectory(
            title="Lütfen analiz edilecek klasörü seçin",
            mustexist=True
        )
        root.destroy()
        return folder_path if folder_path else None
    except Exception as e:
        print(f"Klasör seçici açılırken hata: {e}")
        return None

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