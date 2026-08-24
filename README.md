# Log Analyzer

A Python script that analyzes log files (.log, .txt, .json, .jsonl, .csv) to count total lines, ERROR and WARNING lines, and list error/warning messages with file and line numbers.

## Features

- Parses plain text logs (.log, .txt)
- Parses JSON logs (JSON Lines or JSON array) extracting message and level fields
- Parses CSV logs with headers, extracting message and level columns
- Recursively walks directories
- Outputs summary: files processed, total lines, ERROR/WARNING count
- Lists ERROR and WARNING messages with file:line context
- Limits detailed output to 1000 messages to avoid flooding console
- Saves its own output to a timestamped log file in the script directory
- Double-click friendly: if no directory argument provided, opens a folder selection dialog (tkinter)
- Waits for user input before closing when launched by double-click
- Uses only Python standard library (no external dependencies)

## Usage

```bash
python analyzer.py <directory_to_analyze>
```

If no argument is provided, a folder selection dialog will appear (if tkinter is available).

## Example Output

```
Log dosyası: C:\path\to\analyzer_20260824_204322.log
İşlenen dosya sayısı: 1
Toplam satır sayısı: 10
ERROR ve WARNING geçen satır sayısı: 6
ERROR ve WARNING mesajları:
  [app.log:2] 2024-01-01 10:00:01 ERROR Failed to connect to database
  [app.log:3] 2024-01-01 10:00:02 WARNING High memory usage detected
  [app.log:5] 2024-01-01 10:00:04 ERROR Failed to connect to database
  [app.log:6] 2024-01-01 10:00:05 ERROR Timeout on query
  [app.log:8] 2024-01-01 10:00:07 WARNING Disk space low
  [app.log:9] 2024-01-01 10:00:08 ERROR Failed to connect to database
İşlem tamamlandı. Sonuçlar [C:\path\to\analyzer_20260824_204322.log] dosyasına kaydedildi.
İşlem tamamlandı. Çıkmak için Enter tuşuna basın...
```

## Requirements

- Python 3.x (tested with 3.12)
- Standard library only: os, sys, collections, datetime, json, csv, tkinter (optional for GUI)

## License

MIT