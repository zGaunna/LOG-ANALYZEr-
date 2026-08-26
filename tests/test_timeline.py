def test_timeline_empty_data():
    from src.log_analyzer.timeline import format_timeline
    # Test with empty data
    output = format_timeline({}, {}, 'hourly')
    assert "Veri yok" in output
    output = format_timeline({}, {}, 'daily')
    assert "Veri yok" in output

def test_timeline_hourly_with_data():
    from src.log_analyzer.timeline import format_timeline
    hourly_counts = {
        '2026-08-26 10:00': {'ERROR': 5, 'WARNING': 3},
        '2026-08-26 11:00': {'ERROR': 2, 'WARNING': 8},
        '2026-08-26 12:00': {'ERROR': 0, 'WARNING': 0}
    }
    daily_counts = {}
    output = format_timeline(hourly_counts, daily_counts, 'hourly')
    assert "Saatlik ERROR/WARNING Dağılımı" in output
    assert "2026-08-26 10:00:" in output
    assert "E:" in output and "W:" in output

def test_timeline_daily_with_data():
    from src.log_analyzer.timeline import format_timeline
    hourly_counts = {}
    daily_counts = {
        '2026-08-25': {'ERROR': 10, 'WARNING': 5},
        '2026-08-26': {'ERROR': 3, 'WARNING': 7}
    }
    output = format_timeline(hourly_counts, daily_counts, 'daily')
    assert "Günlük ERROR/WARNING Dağılımı" in output
    assert "2026-08-25:" in output
    assert "E:" in output and "W:" in output