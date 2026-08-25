import json

def test_parse(content):
    print('Testing content:', repr(content))
    stripped = content.strip()
    if stripped.startswith('[') and stripped.endswith(']'):
        print('  Is array')
        decoder = json.JSONDecoder()
        pos = 1  # Skip the '['
        array_len = len(stripped)
        messages = []
        while pos < array_len - 1:
            # Skip whitespace
            while pos < array_len and stripped[pos] in ' \t\n\r':
                pos += 1
            if pos >= array_len - 1 or stripped[pos] == ']':
                print('  Breaking, pos=', pos, 'array_len-1=', array_len-1)
                break
            try:
                obj, end = decoder.raw_decode(stripped, pos)
                print('  Decoded object at pos', pos, '->', obj, 'end=', end)
                line_no = stripped[:pos].count('\n') + 1
                print('  Line no:', line_no)
                if isinstance(obj, dict):
                    message_value = None
                    for key in ['message', 'msg', 'log', 'Message', 'Msg', 'Log']:
                        if key in obj and isinstance(obj[key], str):
                            message_value = obj[key]
                            break
                    level_value = None
                    for key in ['level', 'Level']:
                        if key in obj and isinstance(obj[key], str):
                            level_value = obj[key]
                            break
                    if message_value is not None:
                        if level_value is not None:
                            combined = f'{level_value}: {message_value}'
                            messages.append((line_no, combined))
                        else:
                            messages.append((line_no, message_value))
                    else:
                        messages.append((line_no, json.dumps(obj, ensure_ascii=False)))
                elif isinstance(obj, str):
                    messages.append((line_no, obj))
                else:
                    messages.append((line_no, json.dumps(obj, ensure_ascii=False)))
                pos = end
                while pos < array_len and stripped[pos] in ' \t\n\r':
                    pos += 1
                if pos < array_len and stripped[pos] == ',':
                    pos += 1
            except json.JSONDecodeError as e:
                print('  JSONDecodeError:', e)
                break
        print('  Messages:', messages)
    else:
        print('  Not an array')

# Test compact array
test_parse('[{"message": "ERROR: test1", "level": "ERROR"}, {"message": "WARNING: test2", "level": "WARNING"}]')
# Test pretty-printed array
test_parse('[\n  {"message": "ERROR: test1", "level": "ERROR"},\n  {"message": "WARNING: test2", "level": "WARNING"}\n]')
# Test with trailing newline
test_parse('[{"message": "ERROR: test1", "level": "ERROR"}, {"message": "WARNING: test2", "level": "WARNING"}]\n')
