# Release Notes

## v1.2.0 - 2026-08-27

This release focuses on making Log Analyzer easier to use and more consistent for everyday log inspection.

### Highlights
- 🇹🇷 Turkish and 🇬🇧 English CLI interface.
- `--language tr|en` and `--lang` support.
- Bilingual dashboard and timeline output.
- Safer HTML output escaping.
- Cleaner terminal output and documentation.
- Timeline input validation.
- Removal of unfinished dashboard placeholders.
- Improved analyzer log cleanup behavior.

### Usage

```text
log-analyzer C:\Logs\MyApp
log-analyzer C:\Logs\MyApp --advanced
log-analyzer C:\Logs\MyApp --language en
log-analyzer C:\Logs\MyApp --lang tr --format html
```

### Notes

The analyzer remains dependency-free at runtime and uses the Python standard library. Advanced analysis is statistical and pattern-based; it does not use AI or machine learning.

## v1.1.0 - 2026-08-26

- Added advanced analysis, table output, modular handlers, shared parsing, UTF-8 support, and tests.
- Fixed CSV header detection, JSONL processing, and package import issues.

## v1.0.0 - 2026-08-24

- Initial release with CSV, JSON, JSONL, TXT and LOG analysis.
- Added recursive scanning, ERROR/WARNING detection, GUI folder selection, and CLI support.
