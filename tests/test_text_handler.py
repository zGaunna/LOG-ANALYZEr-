import unittest
import os
import tempfile
from log_analyzer.text_handler import extract_messages_from_log_line

class TestTextHandler(unittest.TestCase):

    def test_extract_messages_from_log_line(self):
        line = "2024-01-01 10:00:01 ERROR Failed to connect\n"
        result = extract_messages_from_log_line(line)
        self.assertEqual(result, "2024-01-01 10:00:01 ERROR Failed to connect")

        line2 = "Just a message\n"
        result2 = extract_messages_from_log_line(line2)
        self.assertEqual(result2, "Just a message")

        line3 = ""
        result3 = extract_messages_from_log_line(line3)
        self.assertEqual(result3, "")

if __name__ == '__main__':
    unittest.main()