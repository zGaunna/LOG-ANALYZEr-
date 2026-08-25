"""Handle CSV log files."""

import csv
import os


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

                    # Look for timestamp column
                    timestamp_value = None
                    for key in ['timestamp', 'time', 'date']:
                        if key in headers:
                            col_idx = headers.index(key)
                            if col_idx < len(row):
                                timestamp_value = row[col_idx]
                            break

                    if msg_value is None and headers:
                        # Fallback: concatenate all cells
                        msg_value = ' '.join(str(cell) for cell in row if cell is not None)

                    # Combine level and message if both present
                    if msg_value and msg_value.strip():
                        if level_value and level_value.strip():
                            combined = f"{level_value}: {msg_value}"
                            # Include timestamp if available for better context
                            if timestamp_value and timestamp_value.strip():
                                combined = f"{timestamp_value} {combined}"
                            messages.append((row_num, combined))
                        else:
                            # Include timestamp if available even if only msg or level is present
                            if timestamp_value and timestamp_value.strip():
                                if msg_value and msg_value.strip():
                                    messages.append((row_num, f"{timestamp_value} {msg_value}"))
                                elif level_value and level_value.strip():
                                    messages.append((row_num, f"{timestamp_value} {level_value}"))
                                else:
                                    messages.append((row_num, msg_value or level_value))
                            else:
                                messages.append((row_num, msg_value))
                    else:
                        # No msg_value, but maybe we have level or timestamp
                        if level_value and level_value.strip():
                            if timestamp_value and timestamp_value.strip():
                                messages.append((row_num, f"{timestamp_value} {level_value}"))
                            else:
                                messages.append((row_num, level_value))
                        elif timestamp_value and timestamp_value.strip():
                            messages.append((row_num, timestamp_value))
                        else:
                            messages.append((row_num, msg_value or level_value or ""))
    except Exception as e:
        log_and_print(f"Error reading CSV file {filepath}: {e}")
    return messages