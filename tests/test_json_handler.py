import unittest
import os
import tempfile
from log_analyzer.json_handler import extract_messages_from_json_file

class TestJSONHandler(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_extract_messages_from_jsonl_valid(self):
        jsonl_content = '''{"timestamp": "2024-01-01 10:00:01", "level": "ERROR", "message": "First"}
{"timestamp": "2024-01-01 10:00:02", "level": "WARNING", "message": "Second"}
'''
        jsonl_path = os.path.join(self.test_dir, "test.jsonl")
        with open(jsonl_path, 'w') as f:
            f.write(jsonl_content)

        messages = extract_messages_from_json_file(jsonl_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0][1], "2024-01-01 10:00:01 ERROR: First")
        self.assertEqual(messages[1][1], "2024-01-01 10:00:02 WARNING: Second")

    def test_extract_messages_from_jsonl_with_invalid_line(self):
        jsonl_content = '''{"timestamp": "2024-01-01 10:00:01", "level": "ERROR", "message": "First"}
INVALID LINE
{"timestamp": "2024-01-01 10:00:02", "level": "WARNING", "message": "Second"}
'''
        jsonl_path = os.path.join(self.test_dir, "test.jsonl")
        with open(jsonl_path, 'w') as f:
            f.write(jsonl_content)

        messages = extract_messages_from_json_file(jsonl_path, lambda msg: print(msg))
        # Should skip the invalid line and process the valid ones
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0][1], "2024-01-01 10:00:01 ERROR: First")
        self.assertEqual(messages[1][1], "2024-01-01 10:00:02 WARNING: Second")

    def test_extract_messages_from_json_array(self):
        json_content = '''[
  {"timestamp": "2024-01-01 10:00:01", "level": "ERROR", "message": "First"},
  {"timestamp": "2024-01-01 10:00:02", "level": "WARNING", "message": "Second"}
]'''
        json_path = os.path.join(self.test_dir, "test.json")
        with open(json_path, 'w') as f:
            f.write(json_content)

        messages = extract_messages_from_json_file(json_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0][1], "2024-01-01 10:00:01 ERROR: First")
        self.assertEqual(messages[1][1], "2024-01-01 10:00:02 WARNING: Second")

    def test_extract_messages_from_json_empty(self):
        json_path = os.path.join(self.test_dir, "empty.json")
        with open(json_path, 'w') as f:
            f.write('')

        messages = extract_messages_from_json_file(json_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 0)

if __name__ == '__main__':
    unittest.main()