import unittest
from log_analyzer.advanced_analyzer import (
    analyze_time_series,
    analyze_error_patterns,
    detect_anomalies,
    analyze_correlations,
    generate_summary_statistics
)

class TestAdvancedAnalyzer(unittest.TestCase):

    def test_analyze_time_series(self):
        messages = [
            ("2024-01-01 10:00:01", "ERROR", "Failed"),
            ("2024-01-01 10:00:02", "WARNING", "High memory"),
            ("2024-01-01 10:00:03", "ERROR", "Failed again"),
            ("2024-01-01 11:00:01", "WARNING", "Something"),
        ]
        result = analyze_time_series(messages)
        self.assertEqual(result['peak_hour'], "2024-01-01 10:00")
        self.assertEqual(result['peak_hour_count']['ERROR'], 2)
        self.assertEqual(result['peak_hour_count']['WARNING'], 1)

    def test_analyze_error_patterns(self):
        messages = [
            ("2024-01-01 10:00:01", "ERROR", "Failed to connect"),
            ("2024-01-01 10:00:02", "ERROR", "Failed to connect"),
            ("2024-01-01 10:00:03", "WARNING", "Just a warning"),
        ]
        result = analyze_error_patterns(messages)
        self.assertEqual(result['total_errors'], 2)
        self.assertEqual(result['total_warnings'], 1)
        self.assertEqual(result['unique_error_messages'], 1)
        self.assertEqual(result['unique_warning_messages'], 1)

    def test_detect_anomalies(self):
        # Create a dataset with one clear outlier
        messages = []
        for i in range(10):
            messages.append((f"2024-01-01 {i:02d}:00:00", "ERROR", f"Message {i}"))
        # Add an outlier with high count
        for i in range(5):
            messages.append((f"2024-01-01 12:00:0{i}", "ERROR", f"Outlier {i}"))
        result = detect_anomalies(messages, threshold=1.0)
        # We expect at least one anomaly
        self.assertTrue(len(result['anomalies']) > 0)

    def test_analyze_correlations(self):
        messages = [
            ("2024-01-01 10:00:00", "WARNING", "Warning sign"),
            ("2024-01-01 10:00:01", "ERROR", "Error after warning"),
            ("2024-01-01 10:00:10", "WARNING", "Another warning"),
            ("2024-01-01 10:00:20", "ERROR", "Error too far"),
        ]
        result = analyze_correlations(messages)
        # Only the first pair is within 5 minutes (60 seconds)
        self.assertEqual(result['warning_to_error_correlations'], 1)

    def test_generate_summary_statistics(self):
        messages = [
            ("2024-01-01 10:00:01", "ERROR", "Failed"),
            ("2024-01-01 10:00:02", "WARNING", "High memory"),
            ("2024-01-01 10:00:03", "INFO", "Info message"),
        ]
        result = generate_summary_statistics(messages)
        self.assertEqual(result['total_messages'], 3)
        self.assertEqual(result['error_count'], 1)
        self.assertEqual(result['warning_count'], 1)
        self.assertEqual(result['info_count'], 1)
        self.assertAlmostEqual(result['error_percentage'], 33.33, places=2)
        self.assertAlmostEqual(result['warning_percentage'], 33.33, places=2)

if __name__ == '__main__':
    unittest.main()