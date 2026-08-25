"""Handle JSON and JSON Lines log files."""

import json


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
            valid_lines_found = 0
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
                    valid_lines_found += 1
                except json.JSONDecodeError:
                    # Log warning about invalid line but continue processing
                    log_and_print(f"Warning: Skipping invalid JSON line {line_num} in {filepath}")
                    continue

            # Only attempt JSON array parsing if no valid JSON Lines were found
            if valid_lines_found == 0:
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
                                # No common message field found
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