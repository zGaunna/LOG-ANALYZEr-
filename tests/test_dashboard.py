# -*- coding: utf-8 -*-
def test_dashboard_empty_results():
    from src.log_analyzer.dashboard import generate_dashboard
    results = {
        'total_files': 0,
        'total_lines': 0,
        'error_count': 0,
        'warning_count': 0,
        'hourly_counts': {},
        'daily_counts': {},
        'top_words': {},
        'common_error_patterns': [],
        'anomalies': [],
        'correlations': [],
        'cause_chains': [],
        'time_span': None,
        'average_message_length': 0,
        'messages_per_hour': 0
    }
    output = generate_dashboard(results)
    assert "İşlenen dosya sayısı: 0" in output
    assert "Toplam satır sayısı: 0" in output
    assert "ERROR oranı: 0.00%" in output
    assert "WARNING oranı: 0.00%" in output