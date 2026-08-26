"""Command-line entry point for Log Analyzer."""

import argparse
import os

from . import analyzer_core, advanced_analyzer, output_formatter, dashboard, timeline


_TRANSLATIONS = {
    "İşlenen dosya sayısı:": "Files processed:",
    "Toplam satır sayısı:": "Total lines:",
    "ERROR ve WARNING geçen satır sayısı:": "ERROR/WARNING lines:",
    "ERROR ve WARNING mesajları:": "ERROR and WARNING messages:",
    "ERROR veya WARNING mesajı bulunamadı.": "No ERROR or WARNING messages found.",
    "İşlem tamamlandı.": "Analysis completed.",
    "Sonuçlar": "Results",
    "GELİŞMİŞ ANALİZ SONUÇLARI": "ADVANCED ANALYSIS RESULTS",
    "Zaman Serisi Analizi:": "Time Series Analysis:",
    "Yoğun saat:": "Peak hour:",
    "Yoğun gün:": "Peak day:",
    "Hata Pattern Analizi:": "Error Pattern Analysis:",
    "Toplam ERROR:": "Total ERROR:",
    "Toplam WARNING:": "Total WARNING:",
    "Benzersiz ERROR mesajları:": "Unique ERROR messages:",
    "Benzersiz WARNING mesajları:": "Unique WARNING messages:",
    "En sık kullanılan kelimeler:": "Most frequent words:",
    "Anomali Algılama:": "Anomaly Detection:",
    "Anomali tespit edilmedi.": "No anomalies detected.",
    "Korelasyon Analizi:": "Correlation Analysis:",
    "Örnekler:": "Examples:",
    "Özet İstatistikler:": "Summary Statistics:",
    "Toplam mesaj:": "Total messages:",
    "ERROR oranı:": "ERROR rate:",
    "WARNING oranı:": "WARNING rate:",
    "Zaman aralığı:": "Time span:",
    "Ortalama mesaj uzunluğu:": "Average message length:",
    "Saat başına mesaj:": "Messages per hour:",
    "ZAMAN ÇİZELGESİ GÖRSELLEŞTİRMESİ": "TIMELINE VISUALIZATION",
    "Köklü Olay Zincirleri:": "Root event chains:",
    "Köklü Olay Zincirleri (muhtemel kök → rezultat):": "Root event chains (possible root → result):",
    "TABLO FORMATLI ÇIKTI": "TABLE OUTPUT",
    "JSON FORMATLI ÇIKTI": "JSON OUTPUT",
    "JSONL FORMATLI ÇIKTI": "JSONL OUTPUT",
    "HTML FORMATLI ÇIKTI": "HTML OUTPUT",
    "Klasör argümanı sağlanmadı. Klasör seçici açılıyor...": "No directory was provided. Opening the folder picker...",
    "Klasör seçilmedi veya GUI kullanılamıyor. Program sonlandırılıyor.": "No folder was selected or GUI is unavailable. Exiting.",
    "Hata:": "Error:",
    "geçerli bir dizin değil": "is not a valid directory",
    "dizinine okuma izni yok": "has no read permission",
    "Beklenmeyen hata:": "Unexpected error:",
    "Çıkmak için Enter tuşuna basın...": "Press Enter to exit...",
}


def _translate(text, language):
    if language != "en":
        return text
    for source, target in sorted(_TRANSLATIONS.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(source, target)
    text = text.replace("Seçilen klasör:", "Selected directory:")
    text = text.replace("Log dosyası:", "Analyzer log:")
    text = text.replace("İşlem tamamlandı. Sonuçlar [", "Analysis completed. Results saved to [")
    text = text.replace("dosyasına kaydedildi.", "file.")
    text = text.replace(" saniye)", " seconds)")
    text = text.replace(" saat)", " hours)")
    text = text.replace(" karakter", " characters")
    return text


def main():
    parser = argparse.ArgumentParser(
        description="Analyze log files for ERROR and WARNING messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n  log-analyzer <directory>\n  log-analyzer <directory> --advanced\n  log-analyzer <directory> --format json --language en",
    )
    parser.add_argument("directory", nargs="?", help="Directory to analyze")
    parser.add_argument("--advanced", action="store_true", help="Enable advanced analysis")
    parser.add_argument("--format", choices=["default", "table", "json", "jsonl", "html"], default="default", help="Output format")
    parser.add_argument("--language", "--lang", choices=["tr", "en"], default="tr", help="Interface language (tr or en)")
    parser.add_argument("--version", action="version", version=f"Log Analyzer {analyzer_core.__version__}")
    args = parser.parse_args()
    language = args.language

    script_dir = os.path.dirname(os.path.abspath(__file__))
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_path = os.path.join(script_dir, f"analyzer_{timestamp}.log")
    analyzer_core.cleanup_old_logs(keep_count=5)

    log_file = None
    try:
        log_file = open(log_file_path, "w", encoding="utf-8")
    except OSError as exc:
        print(_translate(f"Hata: Analyzer logu oluşturulamadı: {exc}", language))

    def log_and_print(message):
        rendered = _translate(str(message), language)
        print(rendered)
        if log_file is not None:
            log_file.write(rendered + "\n")
            log_file.flush()

    try:
        directory = args.directory
        if directory:
            if not os.path.isdir(directory):
                log_and_print(f"Hata: {directory} geçerli bir dizin değil")
                return
            if not os.access(directory, os.R_OK):
                log_and_print(f"Hata: {directory} dizinine okuma izni yok")
                return
        else:
            log_and_print("Klasör argümanı sağlanmadı. Klasör seçici açılıyor...")
            directory = analyzer_core.select_folder_gui()
            if directory is None:
                log_and_print("Klasör seçilmedi veya GUI kullanılamıyor. Program sonlandırılıyor.")
                return
            log_and_print(f"Seçilen klasör: {directory}")

        log_and_print(f"Log dosyası: {log_file_path}")
        total_lines, error_warning_lines, all_error_messages, files_processed = analyzer_core.analyze_logs(directory, log_and_print)

        if args.format != "default":
            labels = {"table": "TABLO FORMATLI ÇIKTI", "json": "JSON FORMATLI ÇIKTI", "jsonl": "JSONL FORMATLI ÇIKTI", "html": "HTML FORMATLI ÇIKTI"}
            log_and_print("\n" + "=" * 60)
            log_and_print(labels[args.format])
            log_and_print("=" * 60)
            formatter = getattr(output_formatter, f"format_{args.format}_output")
            log_and_print(formatter(all_error_messages))

        if args.advanced and all_error_messages:
            log_and_print("\n" + "=" * 60)
            log_and_print("GELİŞMİŞ ANALİZ SONUÇLARI")
            log_and_print("=" * 60)

            events = []
            for filepath, line_num, message in all_error_messages:
                ts, level, _ = analyzer_core.parse_log_message(message)
                events.append(analyzer_core.LogEvent(filepath, line_num, ts, level, message))

            time_series = advanced_analyzer.analyze_time_series(events)
            log_and_print("Zaman Serisi Analizi:")
            log_and_print(f"  Yoğun saat: {time_series['peak_hour']} (ERROR: {time_series['peak_hour_count']['ERROR']}, WARNING: {time_series['peak_hour_count']['WARNING']})")
            log_and_print(f"  Yoğun gün: {time_series['peak_day']} (ERROR: {time_series['peak_day_count']['ERROR']}, WARNING: {time_series['peak_day_count']['WARNING']})")

            patterns = advanced_analyzer.analyze_error_patterns(events)
            log_and_print("\nHata Pattern Analizi:")
            log_and_print(f"  Toplam ERROR: {patterns['total_errors']}")
            log_and_print(f"  Toplam WARNING: {patterns['total_warnings']}")
            log_and_print(f"  Benzersiz ERROR mesajları: {patterns['unique_error_messages']}")
            log_and_print(f"  Benzersiz WARNING mesajları: {patterns['unique_warning_messages']}")
            if patterns.get("top_words"):
                log_and_print(f"  En sık kullanılan kelimeler: {', '.join(list(patterns['top_words'].keys())[:5])}")

            anomalies = advanced_analyzer.detect_anomalies(events)
            log_and_print("\nAnomali Algılama:")
            if anomalies.get("anomalies"):
                for anomaly in anomalies["anomalies"][:3]:
                    log_and_print(f"  {anomaly['hour']}: {anomaly['count']} mesaj (z-score: {anomaly['z_score']}, {anomaly['type']})")
            else:
                log_and_print("  Anomali tespit edilmedi.")

            correlations = advanced_analyzer.analyze_correlations(events)
            log_and_print("\nKorelasyon Analizi:")
            log_and_print(f"  WARNING → ERROR korelasyonu (5 dakika içinde): {correlations['warning_to_error_correlations']} örnek")
            if correlations.get("correlation_examples"):
                log_and_print("  Örnekler:")
                for example in correlations["correlation_examples"][:3]:
                    log_and_print(f"    WARNING: {example['warning_time']} → ERROR: {example['error_time']} ({example['time_diff_seconds']} saniye)")

            stats = advanced_analyzer.generate_summary_statistics(events)
            log_and_print("\nÖzet İstatistikler:")
            log_and_print(f"  Toplam mesaj: {stats['total_messages']}")
            log_and_print(f"  ERROR oranı: {stats['error_percentage']}%")
            log_and_print(f"  WARNING oranı: {stats['warning_percentage']}%")
            if stats.get("time_span"):
                log_and_print(f"  Zaman aralığı: {stats['time_span']['start']} - {stats['time_span']['end']} ({stats['time_span']['duration_hours']} saat)")
            log_and_print(f"  Ortalama mesaj uzunluğu: {stats['average_message_length']} karakter")
            if stats.get("messages_per_hour"):
                log_and_print(f"  Saat başına mesaj: {stats['messages_per_hour']}")

            try:
                chains = advanced_analyzer.detect_cause_chain(events)
            except AttributeError:
                chains = []
            if chains:
                log_and_print("\nKöklü Olay Zincirleri (muhtemel kök → rezultat):")
                for idx, info in enumerate(chains[:3], 1):
                    root = info['root']
                    log_and_print(f"  {idx}. Kök: [{root.filepath}:{root.line_number}] {root.timestamp} {root.level} {root.message[:100]}")
                    log_and_print("     Zincir: " + " → ".join(ev.level for ev in info['chain']))
            else:
                log_and_print("\nKöklü Olay Zincirleri: Tespit edilmedi.")

            log_and_print("\n" + "=" * 60)
            log_and_print("ZAMAN ÇİZELGESİ GÖRSELLEŞTİRMESİ")
            log_and_print("=" * 60)
            log_and_print(timeline.format_timeline(time_series.get("hourly", {}), time_series.get("daily", {}), "hourly", language))
            log_and_print("")
            log_and_print(timeline.format_timeline(time_series.get("hourly", {}), time_series.get("daily", {}), "daily", language))

            results = {
                "total_files": files_processed, "total_lines": total_lines,
                "error_count": patterns["total_errors"], "warning_count": patterns["total_warnings"],
                "hourly_counts": time_series.get("hourly", {}), "daily_counts": time_series.get("daily", {}),
                "top_words": patterns.get("top_words", {}), "anomalies": anomalies.get("anomalies", []),
                "correlations": correlations.get("correlation_examples", []), "peak_hour": time_series["peak_hour"],
                "peak_hour_count": time_series["peak_hour_count"], "peak_day": time_series["peak_day"],
                "peak_day_count": time_series["peak_day_count"],
            }
            log_and_print("\n" + "=" * 60)
            log_and_print("İSTATİSTİKSEL DASHBOARD")
            log_and_print("=" * 60)
            log_and_print(dashboard.generate_dashboard(results, language))

        log_and_print(f"İşlem tamamlandı. Sonuçlar [{log_file_path}] dosyasına kaydedildi.")
    except Exception as exc:
        log_and_print(f"Beklenmeyen hata: {exc}")
    finally:
        if log_file is not None:
            log_file.close()
        analyzer_core.wait_for_exit()


if __name__ == "__main__":
    main()
