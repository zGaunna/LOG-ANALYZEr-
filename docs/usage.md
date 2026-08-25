# Usage Guide

## Command Line Interface

The log analyzer can be run directly with Python:

```bash
python analyzer.py <directory_to_analyze>
```

Or, after installation, via the command:

```bash
log-analyzer <directory_to_analyze>
```

### Arguments

- `directory` (optional): Path to the directory containing log files to analyze.
  If not provided, a folder selection dialog will appear (if tkinter is available).

### Options

- `--advanced`: Enable advanced analysis features (time series, pattern detection, etc.)
- `--format {default,table}`: Specify ilin format. 
  - `default`: Standard console output
  - `table`: SQL-like table format
- `--version`: Show the program's version and exit.

## Examples

### Basic Usage

Analyze a directory for ERROR and WARNING messages:

```bash
python analyzer.py /var/log/myapp
```

### Advanced Analysis

Enable time series, pattern detection, and other advanced features:

```bash
python analyzer.py /var/log/myapp --advanced
```

### Table Format Output

Get output in a formatted table for easier reading:

```bash
python analyzer.py /var/log/myapp --format table
```

### Combined Options

Use both advanced analysis and table format:

```bash
python analyzer.py /var/log/myapp --advanced --format table
```

## Output Formats

### Default Output

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

When combined with either format, advanced analysis provides additional insights:

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

## Supported Log Formats

- Plain text: `.log`, `.txt`
- JSON: `.json`, `.jsonl` (JSON Lines)
- CSV: `.csv` (with automatic header detection)

## Requirements

- Python 3.7 or higher
- Only Python standard library modules are used (no external dependencies)
- Tkinter is optional for the GUI folder selection dialog

## License

MIT License - see the LICENSE file for details.