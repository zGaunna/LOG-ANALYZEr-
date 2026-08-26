# Log Analyzer

Log dosyalarını hızlıca tarayıp önemli olayları anlaşılır bir şekilde görmenizi sağlayan, harici bağımlılığı olmayan küçük bir Python aracı.

Log Analyzer `.log`, `.txt`, `.json`, `.jsonl` ve `.csv` dosyalarını tarar; `ERROR` ve `WARNING` olaylarını bulur ve sonuçları dosya ile satır bilgisiyle birlikte gösterir.

**English:** [README.md](README.md)

## Ne yapıyor?

- Düz metin loglarını (`.log`, `.txt`) okur
- JSON ve JSONL loglarını okur
- Yaygın log sütunlarına sahip CSV dosyalarını okur
- Klasörleri alt klasörleriyle birlikte tarar
- Hata ve uyarının hangi dosya ve satırda olduğunu gösterir
- Ayrıntılı çıktıyı 1000 mesajla sınırlar
- Sonuçları zaman damgalı bir analyzer loguna kaydeder
- Tkinter kullanılabiliyorsa klasör seçici açabilir
- Yalnızca Python standart kütüphanesini kullanır

## Gelişmiş analiz

`--advanced` seçeneği:

- Saatlik ve günlük ERROR/WARNING yoğunluğunu
- Tekrarlanan mesaj ve kelime sıklığını
- Temel istatistiksel anomalileri
- WARNING → ERROR zaman ilişkilerini
- Özet istatistikleri
- ASCII zaman çizelgesini
- Terminal dashboard'unu

gösterir.

Bunlar temel istatistik ve pattern-matching yöntemleridir. Projede yapay zekâ veya makine öğrenmesi modeli kullanılmaz.

## Kurulum

```bash
pip install .
```

## Kullanım

```bash
log-analyzer <klasör>
```

veya:

```bash
python -m log_analyzer <klasör>
```

### Seçenekler

```text
--advanced
--format {default,table,json,jsonl,html}
--version
```

### Örnekler

```bash
log-analyzer C:\Logs\MyApp
log-analyzer C:\Logs\MyApp --advanced
log-analyzer C:\Logs\MyApp --format table
log-analyzer C:\Logs\MyApp --format json
log-analyzer C:\Logs\MyApp --format html
log-analyzer C:\Logs\MyApp --advanced --format table
```

## Desteklenen dosyalar

| Format | Açıklama |
|---|---|
| `.log` | Düz metin, çok satırlı olaylar dahil |
| `.txt` | Düz metin |
| `.json` | JSON nesneleri ve dizileri |
| `.jsonl` | JSON Lines |
| `.csv` | Otomatik ayraç ve başlık algılama |

## Gereksinimler

- Python 3.7+
- Harici çalışma zamanı bağımlılığı yoktur
- Tkinter yalnızca klasör seçici için isteğe bağlıdır

## Geliştirme

```bash
python -m unittest discover -s tests
```

## Sınırlamalar

Log formatları uygulamadan uygulamaya değişebilir. Analyzer yaygın formatları destekler, ancak özel formatlar için ek parsing kuralları gerekebilir. Zaman tabanlı analizler de tanınabilir timestamp bilgisine bağlıdır.

## Lisans

MIT
