import unittest
import os
import tempfile
from log_analyzer.csv_handler import extract_messages_from_csv_file

class TestCSVHandler(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.test_dir)

    def test_extract_messages_from_csv_with_header(self):
        csv_content = """timestamp,level,message
2024-01-01 10:00:01,ERROR,Failed to connect
2024-01-01 10:00:02,WARNING,High memory
"""
        csv_path = os.path.join(self.test_dir, "test.csv")
        with open(csv_path, 'w') as f:
            f.write(csv_content)

        messages = extract_messages_from_csv_file(csv_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0][1], "2024-01-01 10:00:01 ERROR: Failed to connect")
        self.assertEqual(messages[1][1], "2024-01-01 10:00:02 WARNING: High memory")

    def test_extract_messages_from_csv_without_header(self):
        csv_content = """2024-01-01 10:00:01,ERROR,Failed to connect
2024-01-01 10:00:02,WARNING,High memory
"""
        csv_path = os.path.join(self.test_dir, "test.csv")
        with open(csv_path, 'w') as f:
            f.write(csv_content)

        messages = extract_messages_from_csv_file(csv_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 2)
        self.assertIn("2024-01-01 10:00:01 ERROR: Failed to connect", messages[0][1])
        self.assertIn("2024-01-01 10:00:02 WARNING: High memory", messages[1][1])

    def test_extract_messages_from_csv_false_positive(self):
        # This CSV has no header-like row, but contains the word "level" in data
        csv_content = """2024-01-01,upgradelevel,Some message
2024-01-01,ERROR,Failed to connect
"""
        csv_path = os.path.join(self.test_dir, "test.csv")
        with open(csv_path, 'w') as f:
            f.write(csv_content)

        messages = extract_messages_from_csv_file(csv_path, lambda msg: print(msg))
        # Should treat first row as data, not header
        self.assertEqual(len(messages), 2)
        self.assertIn("upgradelevel", messages[0][1])
        self.assertIn("ERROR: Failed to connect", messages[1][1])

    def test_extract_messages_from_csv_empty_file(self):
        csv_path = os.path.join(self.test_dir, "empty.csv")
        with open(csv_path, 'w') as f:
            pass

        messages = extract_messages_from_csv_file(csv_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 0)

    def test_extract_messages_from_csv_only_header(self):
        csv_content = """timestamp,level,message
"""
        csv_path = os.path.join(self.test_dir, "header_only.csv")
        with open(csv_path, 'w') as f:
            f.write(csv_content)

        messages = extract_messages_from_csv_file(csv_path, lambda msg: print(msg))
        self.assertEqual(len(messages), 0)

if __name__ == '__main__':
    unittest.main()