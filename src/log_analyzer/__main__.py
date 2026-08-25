"""Main entry point for the log analyzer."""

import argparse
import sys
import os

# Try relative import first (when used as module), fall back to absolute (when run directly)
try:
    from . import analyzer_core, advanced_analyzer, output_formatter
except ImportError:
    from log_analyzer import analyzer_core, advanced_analyzer, output_formatter


def main():
    """Main entry point for the log analyzer."""
    parser = argparse.ArgumentParser(
        description="Analyze log files for ERROR and WARNING messages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m log_analyzer /path/to/logs
  python -m log_analyzer /path/to/logs --advanced
  python -m log_analyzer /path/to/logs --format table
  python -m log_analyzer /path/to/logs --advanced --format table
        """
    )

    parser.add_argument(
        'directory',
        nargs='?',
        help='Directory to analyze (if not provided, opens folder selection dialog)'
    )

    parser.add_argument(
        '--advanced',
        action='store_true',
        help='Enable advanced analysis features'
    )

    parser.add_argument(
        '--format',
        choices=['default', 'table'],
        default='default',
        help='Output format (default: default)'
    )

    parser.add_argument(
        '--version',
        action='version',
        version=f'Log Analyzer {analyzer_core.__version__}'
    )

    args = parser.parse_args()

    # Determine script directory for log file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = os.path.join(script_dir, f"analyzer_{timestamp}.log")

    # Open log file
    log_file = None
    try:
        log_file = open(log_file_path, 'w', encoding='utf-8')
    except Exception as e:
        print(f"Failed to create log file: {e}")
        # Fallback: only console output
        log_file = None

    # Function to print to console and log file
    def log_and_print(message):
        print(message)
        if log_file is not None:
            log_file.write(message + '\n')
            log_file.flush()

    try:
        # Check if directory argument provided
        if args.directory:
            directory = args.directory
            if not os.path.isdir(directory):
                log_and_print(f"Hata: {directory} geçerli bir dizin değil")
                return
            # Check read permission
            if not os.access(directory, os.R_OK):
                log_and_print(f"Hata: {directory} dizinine okuma izni yok")
                return
        else:
            # No argument - try to use GUI folder selection
            log_and_print("Klasör argümanı sağlanmadı. Klasör seçici açılıyor...")
            directory = analyzer_core.select_folder_gui()
            if directory is None:
                log_and_print("Klasör seçilmedi veya GUI kullanılamıyor. Program sonlandırılıyor.")
                return
            log_and_print(f"Seçilen klasör: {directory}")

        log_and_print(f"Log dosyası: {log_file_path}")

        # Perform analysis
        total_lines, error_warning_lines, all_error_messages = analyzer_core.analyze_logs(directory, log_and_print)

        # Output based on format choice
        if args.format == 'table':
            # For table format, we use the table formatter
            log_and_print("\n" + "="*60)
            log_and_print("TABLO FORMATLI ÇIKTI")
            log_and_print("="*60)

            table_output = output_formatter.format_table_output(all_error_messages)
            log_and_print(table_output)
        else:
            # Default format - already printed by analyze_logs
            pass

        # Advanced analysis if requested
        if args.advanced and all_error_messages:
            log_and_print("\n" + "="*60)
            log_and_print("GELİŞMİŞ ANALİZ SONUÇLARI")
            log_and_print("="*60)

            # Parse messages for advanced analysis: (timestamp, level, message)
            parsed_for_advanced = []
            for filepath, line_num, message in all_error_messages:
                timestamp, level, content = analyzer_core.parse_log_message(message)
                # We use the original message for analysis, but we have parsed timestamp and level
                parsed_for_advanced.append((timestamp, level, message))

            # Time series analysis
            time_series = analyzer_core.analyze_time_series(parsed_for_advanced)
            log_and_print("Zaman Serisi Analizi:")
            log_and_print(f"  Yoğun saat: {time_series['peak_hour']} (ERROR: {time_series['peak_hour_count']['ERROR']}, WARNING: {time_series['peak_hour_count']['WARNING']})")
            log_and_print(f"  Yoğun gün: {time_series['peak_day']} (ERROR: {time_series['peak_day_count']['ERROR']}, WARNING: {time_series['peak_day_count']['WARNING']})")

            # Error pattern analysis
            error_patterns = analyzer_core.analyze_error_patterns(parsed_for_advanced)
            log_and_print("\nHata Pattern Analizi:")
            log_and_print(f"  Toplam ERROR: {error_patterns['total_errors']}")
            log_and_print(f"  Toplam WARNING: {error_patterns['total_warnings']}")
            log_and_print(f"  Benzersiz ERROR mesajları: {error_patterns['unique_error_messages']}")
            log_and_print(f"  Benzersiz WARNING mesajları: {error_patterns['unique_warning_messages']}")
            if error_patterns['top_words']:
                log_and_print(f"  En sık kullanılan kelimeler: {', '.join(list(error_patterns['top_words'].keys())[:5])}")

            # Anomaly detection
            anomalies = analyzer_core.detect_anomalies(parsed_for_advanced)
            log_and_print("\nAnomali Algılama:")
            if anomalies['anomalies']:
                for anomaly in anomalies['anomalies'][:3]:  # Show top 3
                    log_and_print(f"  {anomaly['hour']}: {anomaly['count']} mesaj (z-score: {anomaly['z_score']}, {anomaly['type']})")
            else:
                log_and_print("  Anomali tespit edilmedi.")

            # Correlation analysis
            correlations = analyzer_core.analyze_correlations(parsed_for_advanced)
            log_and_print("\nKorelasyon Analizi:")
            log_and_print(f"  WARNING → ERROR korelasyonu (5 dakika içinde): {correlations['warning_to_error_correlations']} örnek")
            if correlations['correlation_examples']:
                log_and_print("  Örnekler:")
                for example in correlations['correlation_examples'][:3]:
                    log_and_print(f"    WARNING: {example['warning_time']} → ERROR: {example['error_time']} ({example['time_diff_seconds']} saniye)")

            # Summary statistics
            stats = analyzer_core.generate_summary_statistics(parsed_for_advanced)
            log_and_print("\nÖzet İstatistikler:")
            log_and_print(f"  Toplam mesaj: {stats['total_messages']}")
            log_and_print(f"  ERROR oranı: {stats['error_percentage']}%")
            log_and_print(f"  WARNING oranı: {stats['warning_percentage']}%")
            if stats['time_span']:
                log_and_print(f"  Zaman aralığı: {stats['time_span']['start']} - {stats['time_span']['end']} ({stats['time_span']['duration_hours']} saat)")
            log_and_print(f"  Ortalama mesaj uzunluğu: {stats['average_message_length']} karakter")
            if stats['messages_per_hour']:
                log_and_print(f"  Saat başına mesaj: {stats['messages_per_hour']}")

        log_and_print(f"İşlem tamamlandı. Sonuçlar [{log_file_path}] dosyasına kaydedildi.")

    except Exception as e:
        log_and_print(f"Beklenmeyen hata: {e}")
    finally:
        if log_file is not None:
            log_file.close()
        analyzer_core.wait_for_exit()


if __name__ == "__main__":
    main()