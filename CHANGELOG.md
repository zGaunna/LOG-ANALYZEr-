# Changelog

All notable changes to this project are documented here.

## [1.2.0] - 2026-08-27

### Added
- Turkish and English CLI interface with `--language tr|en` and `--lang` alias.
- Bilingual terminal dashboard and timeline output.
- JSON, JSONL and HTML output options documented and exposed consistently.
- Cleaner, more human-readable README documentation in Turkish and English.

### Improved
- HTML output now safely escapes file names and messages.
- Timeline rejects unsupported granularity values instead of silently choosing daily mode.
- Dashboard no longer displays unfinished placeholder KPIs.
- Log cleanup is executed before creating a new analyzer log and keeps the newest five files.
- Common log severity aliases such as `WARN`, `severity`, and `loglevel` are recognized more consistently.
- Windows console UTF-8 handling remains dependency-free.

### Documentation
- Added `README.tr.md`.
- Updated installation, CLI options, supported formats, limitations, and development instructions.

## [1.1.0] - 2026-08-26

### Added
- Advanced analysis features (time series, pattern detection, anomaly detection, correlation analysis)
- Table format output
- Modular package structure with separate CSV, JSON, and text handlers
- Shared log message parsing
- UTF-8 console and log output
- Test suite structure

### Fixed
- CSV header detection false positives
- JSON Lines parsing early termination
- Module/script import issues
- Duplicate analyzer entry point

## [1.0.0] - 2026-08-24

### Added
- Initial release with CSV, JSON, and plain text log support
- ERROR/WARNING counting and message listing
- Recursive directory scanning
- GUI folder selection
- Timestamped analyzer log output
- Command-line interface
