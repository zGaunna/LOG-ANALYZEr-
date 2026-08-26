def generate_dashboard(results: dict) -> str:
    """Generate a terminal-based dashboard with KPIs."""
    lines = []
    lines.append(f"İşlenen dosya sayısı: {results.get('total_files', 0)}")
    lines.append(f"Toplam satır sayısı: {results.get('total_lines', 0)}")
    total = results.get('error_count', 0) + results.get('warning_count', 0)
    error_pct = 0 if total == 0 else round((results.get('error_count', 0) / total) * 100, 2)
    warning_pct = 0 if total == 0 else round((results.get('warning_count', 0) / total) * 100, 2)
    lines.append(f"ERROR oranı: {error_pct:.2f}%")
    lines.append(f"WARNING oranı: {warning_pct:.2f}%")
    # Severity distribution (simple bar)
    error_count = results.get('error_count', 0)
    warning_count = results.get('warning_count', 0)
    max_count = max(error_count, warning_count, 1)
    error_bar = '#' * int((error_count / max_count) * 10) if max_count > 0 else ''
    warning_bar = '#' * int((warning_count / max_count) * 10) if max_count > 0 else ''
    lines.append(f"Severite dağılımı: ERROR[{error_bar}] WARNING[{warning_bar}]")
    # Peak hour
    peak_hour = results.get('peak_hour', 'N/A')
    peak_hour_count = results.get('peak_hour_count', {'ERROR': 0, 'WARNING': 0})
    lines.append(f"Yoğun saat: {peak_hour} (ERROR: {peak_hour_count['ERROR']}, WARNING: {peak_hour_count['WARNING']})")
    # Peak day
    peak_day = results.get('peak_day', 'N/A')
    peak_day_count = results.get('peak_day_count', {'ERROR': 0, 'WARNING': 0})
    lines.append(f"Yoğun gün: {peak_day} (ERROR: {peak_day_count['ERROR']}, WARNING: {peak_day_count['WARNING']})")
    # Top words
    top_words = results.get('top_words', {})
    if top_words:
        top5 = list(top_words.items())[:5]
        words_str = ', '.join([f'{word} ({count})' for word, count in top5])
        lines.append(f"En sık kullanılan kelimeler: {words_str}")
    else:
        lines.append("En sık kullanılan kelimeler: Yok")
    # Add more KPIs as per spec: new errors, recurrence rate (placeholders for now)
    lines.append("Yeni hatalar: N/A (baseline karşılaştırması uygulanmadı)")
    lines.append("Tekrar oranı: N/A")
    return '\n'.join(lines)