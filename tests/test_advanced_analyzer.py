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
        from log_analyzer.analyzer_core import LogEvent
        messages = [
            LogEvent("test.log", 1, "2024-01-01 10:00:01", "ERROR", "Failed"),
            LogEvent("test.log", 2, "2024-01-01 10:00:02", "WARNING", "High memory"),
            LogEvent("test.log", 3, "2024-01-01 10:00:03", "ERROR", "Failed again"),
            LogEvent("test.log", 4, "2024-01-01 11:00:01", "WARNING", "Something"),
        ]
        result = analyze_time_series(messages)
        self.assertEqual(result['peak_hour'], "2024-01-01 10:00")
        self.assertEqual(result['peak_hour_count']['ERROR'], 2)
        self.assertEqual(result['peak_hour_count']['WARNING'], 1)

    def test_analyze_error_patterns(self):
        from log_analyzer.analyzer_core import LogEvent
        messages = [
            LogEvent("test.log", 1, "2024-01-01 10:00:01", "ERROR", "Failed to connect"),
            LogEvent("test.log", 2, "2024-01-01 10:00:02", "ERROR", "Failed to connect"),
            LogEvent("test.log", 3, "2024-01-01 10:00:03", "WARNING", "Just a warning"),
        ]
        result = analyze_error_patterns(messages)
        self.assertEqual(result['total_errors'], 2)
        self.assertEqual(result['total_warnings'], 1)
        self.assertEqual(result['unique_error_messages'], 1)
        self.assertEqual(result['unique_warning_messages'], 1)

    def test_detect_anomalies(self):
        from log_analyzer.analyzer_core import LogEvent
        # Create a dataset with one clear outlier
        messages = []
        for i in range(10):
            messages.append(LogEvent("test.log", i+1, f"2024-01-01 {i:02d}:00:00", "ERROR", f"Message {i}"))
        # Add an outlier with high count
        for i in range(5):
            messages.append(LogEvent("test.log", i+11, f"2024-01-01 12:00:0{i}", "ERROR", f"Outlier {i}"))
        result = detect_anomalies(messages, threshold=1.0)
        # We expect at least one anomaly
        self.assertTrue(len(result['anomalies']) > 0)

    def test_analyze_correlations(self):
        from log_analyzer.analyzer_core import LogEvent
        messages = [
            LogEvent("test.log", 1, "2024-01-01 10:00:00", "WARNING", "Warning sign"),
            LogEvent("test.log", 2, "2024-01-01 10:00:01", "ERROR", "Error after warning"),
            LogEvent("test.log", 3, "2024-01-01 10:00:10", "WARNING", "Another warning"),
            LogEvent("test.log", 4, "2024-01-01 10:00:20", "ERROR", "Error too far"),
        ]
        result = analyze_correlations(messages)
        # Both warning-error pairs are within 5 minutes:
        # 10:00:00 -> 10:00:01 (1 second)
        # 10:00:10 -> 10:00:20 (10 seconds)
        self.assertEqual(result['warning_to_error_correlations'], 2)
        # Check that we get the closest matches
        correlations = result['correlation_examples']
        self.assertEqual(len(correlations), 2)
        # First correlation: 10:00:00 warning should match 10:00:01 error (closest)
        self.assertEqual(correlations[0]['warning_time'], "2024-01-01 10:00:00")
        self.assertEqual(correlations[0]['error_time'], "2024-01-01 10:00:01")
        self.assertEqual(correlations[0]['time_diff_seconds'], 1)
        # Second correlation: 10:00:10 warning should match 10:00:20 error (closest)
        self.assertEqual(correlations[1]['warning_time'], "2024-01-01 10:00:10")
        self.assertEqual(correlations[1]['error_time'], "2024-01-01 10:00:20")
        self.assertEqual(correlations[1]['time_diff_seconds'], 10)

    def test_generate_summary_statistics(self):
        from log_analyzer.analyzer_core import LogEvent
        messages = [
            LogEvent("test.log", 1, "2024-01-01 10:00:01", "ERROR", "Failed"),
            LogEvent("test.log", 2, "2024-01-01 10:00:02", "WARNING", "High memory"),
            LogEvent("test.log", 3, "2024-01-01 10:00:03", "INFO", "Info message"),
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