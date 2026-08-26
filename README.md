# Log Analyzer

A small, dependency-free tool for finding useful information in log files without turning the terminal into a wall of noise.

Log Analyzer scans `.log`, `.txt`, `.json`, `.jsonl`, and `.csv` files, finds `ERROR` and `WARNING` events, and gives you a readable summary.

**Türkçe:** [README.tr.md](README.tr.md)

## What it does

- Reads plain-text logs (`.log`, `.txt`)
- Reads JSON and JSONL logs
- Reads CSV logs with common log columns
- Searches folders recursively
- Shows the file and line where an error or warning was found
- Limits detailed output to 1000 messages
- Saves a timestamped analyzer log
- Can open a folder picker when no directory is supplied
- Uses only the Python standard library

## Advanced analysis

Use `--advanced` for extra analysis:

- Hourly and daily error/warning trends
- Repeated-message and word-frequency analysis
- Basic anomaly detection
- Warning to error time-based associations
- Summary statistics
- ASCII timelines
- Terminal dashboard

These are basic statistical and pattern-matching features. There is no AI or machine-learning model involved.

## Installation

```bash
pip install .
```

## Usage

```bash
log-analyzer <directory>
```

Or:

```bash
python -m log_analyzer <directory>
```

Without a directory, the program can open a folder picker when Tkinter is available.

### Options

```text
--advanced
--format {default,table,json,jsonl,html}
--version
```

### Examples

```bash
log-analyzer C:\Logs\MyApp
log-analyzer C:\Logs\MyApp --advanced
log-analyzer C:\Logs\MyApp --format table
log-analyzer C:\Logs\MyApp --format json
log-analyzer C:\Logs\MyApp --format html
log-analyzer C:\Logs\MyApp --advanced --format table
```

## Supported files

| Format | Notes |
|---|---|
| `.log` | Plain text, including multiline events |
| `.txt` | Plain text |
| `.json` | JSON objects and arrays |
| `.jsonl` | JSON Lines |
| `.csv` | Automatic delimiter and header handling |

## Project structure

```text
src/log_analyzer/
├── analyzer_core.py
├── advanced_analyzer.py
├── csv_handler.py
├── json_handler.py
├── output_formatter.py
├── dashboard.py
├── timeline.py
└── __main__.py
```

## Requirements

- Python 3.7+
- No third-party runtime dependencies
- Tkinter is optional and only used for the folder picker

## Development

Run the tests with:

```bash
python -m unittest discover -s tests
```

## Limitations

Log formats differ a lot between applications. The analyzer supports several common patterns, but custom formats may need additional parsing rules. Time-based analysis also depends on recognizable timestamps.

## License

MIT
