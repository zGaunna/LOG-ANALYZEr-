# Release Notes

## v1.0.0 (Unreleased)
### Added
- Advanced analysis features (time series, pattern detection, anomaly detection, correlation analysis)
- Table format output with SQL-like display
- Modular package structure with separate handlers for CSV, JSON, text logs
- Shared log message parsing function for consistent timestamp/level extraction
- Proper UTF-8 encoding support for Turkish characters in console and log files
- Comprehensive test suite structure
- Permission checking for directory access
- Log file cleanup mechanism (keeps 5 most recent logs)

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

## v0.1.0 (Initial)
### Added
- Basic log analysis for CSV, JSON, and plain text files
- ERROR/WARNING counting and message listing
- Recursive directory scanning
- GUI folder selection (tkinter)
- Log file output with timestamp
- Command line interface with help and version information