# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - 2026-08-26
### Added
- Advanced analysis features (time series, pattern detection, anomaly detection, correlation analysis)
- Table format output with SQL-like display
- Modular package structure with separate handlers for CSV, JSON, text logs
- Shared log message parsing function for consistent timestamp/level extraction
- Proper UTF-8 encoding support for Turkish characters in console and log files
- Comprehensive test suite structure

### Fixed
- CSV header detection false positives (now requires exact match of ≥2 log-related columns)
- JSON Lines parsing early termination (continues processing after invalid lines)
- Import issues when running as module vs script
- Duplicate analyzer.py file in src/log_analyzer/

### Changed
- Restructured project to standard Python package layout
- Moved test files to tests/ directory
- Enhanced console output to properly display Turkish characters
- Used shared parsing function in table formatter and advanced analysis

## [1.0.0] - 2026-08-24
### Added
- Initial release of Log Analyzer with CSV, JSON, and plain text log support
- ERROR/WARNING counting and message listing
- Recursive directory scanning
- GUI folder selection (tkinter)
- Log file output with timestamp
- Command line interface with help and version information

## [Unreleased]

### Fixed
- Korelasyon analizi: analyze_correlations fonksiyonu artık her WARNING için zaman damgasına göre sıralı error_times listesini kullanarak, en yakın (minimum pozitif zaman farkı) ERROR'u bulur. Bu, çoklu dosya işleme veya dosyalar kronolojik olmayan sırada işlenirse daha doğru korelasyon sonuçları sağlar.
