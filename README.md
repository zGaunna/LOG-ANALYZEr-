# Log Analyzer

A Python package that analyzes log files (.log, .txt, .json, .jsonl, .csv) to count total lines, ERROR and WARNING lines, and list error/warning messages with file and line numbers.

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
- **Advanced analysis features** (with `--advanced` flag):
  - Time series analysis (hourly/daily ERROR/WARNING trends)
  - Error pattern analysis (word frequency, message similarity grouping)
  - Anomaly detection (statistical outlier detection in log volumes)
  - Correlation analysis (WARNING→ERROR within time windows)
  - Summary statistics (percentages, time span, message length, etc.)
- **Table format output** (with `--format table`):
  - SQL-like table display: TIMESTAMP | LEVEL | MESSAGE | FILE:LINE
  - Proper column alignment and truncation for readability

## Installation

```bash
pip install .
```

## Usage

After installation, use the command:

```bash
log-analyzer <directory_to_analyze>
```

Alternatively, you can run it directly with Python:

```bash
python -m log_analyzer <directory_to_analyze>
```

If no argument is provided, a folder selection dialog will appear (if tkinter is available).

### Options

- `--advanced`: Enable advanced analysis features
- `--format {default,table}`: Output format (default: default)
- `--version`: Show program's version number and exit

### Examples

```bash
# Basic analysis
log-analyzer /path/to/logs

# With advanced analysis
log-analyzer /path/to/logs --advanced

# With table format output
log-analyzer /path/to/logs --format table

# Both advanced analysis and table format
log-analyzer /path/to/logs --advanced --format table
```

## Example Output

### Default Format
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

### Table Format (`--format table`)
```
============================================================
TABLO FORMATLI ÇIKTI
============================================================
TIMESTAMP           LEVEL   MESSAGE                                    FILE:LINE
------------------- ------- ------------------------------------------ --------------------
2024-01-01 10:00:01 ERROR   Failed to connect to database              app.log:2
2024-01-01 10:00:02 WARNING High memory usage detected                 app.log:3
2024-01-01 10:00:04 ERROR   Failed to connect to database              app.log:5
2024-01-01 10:00:05 ERROR   Timeout on query                           app.log:6
2024-01-01 10:00:07 WARNING Disk space low                             app.log:8
2024-01-01 10:00:08 ERROR   Failed to connect to database              app.log:9
...

İşlem tamamlandı. Sonuçlar [C:\path\to\analyzer_20260824_204322.log] dosyasına kaydedildi.
İşlem tamamlandı. Çıkmak için Enter tuşuna basın...
```

### Advanced Analysis (`--advanced`)
```
============================================================
GELİŞMİŞ ANALİZ SONUÇLARI
============================================================
Zaman Serisi Analizi:
  Yoğun saat: 2024-01-01 10:00 (ERROR: 3, WARNING: 2)
  Yoğun gün: 2024-01-01 (ERROR: 5, WARNING: 3)

Hata Pattern Analizi:
  Toplam ERROR: 5
  Toplam WARNING: 3
  Benzersiz ERROR mesajları: 2
  Benzersiz WARNING mesajları: 3
  En sık kullanılan kelimeler: Failed, connect, database, Timeout, Disk

Anomali Algılama:
  Anomali tespit edilmedi.

Korelasyon Analizi:
  WARNING → ERROR korelasyonu (5 dakika içinde): 2 örnek
  Örnekler:
    WARNING: 2024-01-01 10:00:02 → ERROR: 2024-01-01 10:00:04 (120 saniye)
    WARNING: 2024-01-01 10:00:07 → ERROR: 2024-01-01 10:00:08 (60 saniye)

Özet İstatistikler:
  Toplam mesaj: 8
  ERROR oranı: 62.50%
  WARNING oranı: 37.50%
  Zaman aralığı: 2024-01-01 10:00:01 - 2024-01-01 10:00:08 (0.02 saat)
  Ortalama mesaj uzunluğu: 35.25 karakter
  Saat başına mesaj: 400.00
```

## Requirements

- Python 3.x (tested with 3.12)
- Standard library only: os, sys, collections, datetime, json, csv, tkinter (optional for GUI)

## License

MIT