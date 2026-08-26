"""Dependency-free Turkish/English translations for the command-line UI."""

MESSAGES = {
    "tr": {
        "description": "Log dosyalarını analiz eder ve ERROR/WARNING olaylarını özetler.",
        "advanced": "Gelişmiş analizi etkinleştir",
        "language": "Arayüz dili",
        "picker": "Klasör seçilmedi. Klasör seçici açılıyor...",
        "cancelled": "Klasör seçilmedi veya GUI kullanılamıyor. Program sonlandırılıyor.",
        "invalid": "Hata: {value} geçerli bir dizin değil.",
        "permission": "Hata: {value} dizinine okuma izni yok.",
        "selected": "Seçilen klasör: {value}",
        "done": "İşlem tamamlandı. Sonuçlar {value} dosyasına kaydedildi.",
        "unexpected": "Beklenmeyen hata: {value}",
        "advanced_title": "GELİŞMİŞ ANALİZ SONUÇLARI",
        "time_series": "Zaman Serisi Analizi:",
        "patterns": "Hata Pattern Analizi:",
        "anomalies": "Anomali Algılama:",
        "correlations": "Korelasyon Analizi:",
        "statistics": "Özet İstatistikler:",
        "timeline": "ZAMAN ÇİZELGESİ",
        "no_anomalies": "  Anomali tespit edilmedi.",
        "table": "TABLO FORMATLI",
        "json": "JSON FORMATLI",
        "jsonl": "JSONL FORMATLI",
        "html": "HTML FORMATLI",
    },
    "en": {
        "description": "Analyze log files and summarize ERROR/WARNING events.",
        "advanced": "Enable advanced analysis",
        "language": "Interface language",
        "picker": "No directory was provided. Opening the folder picker...",
        "cancelled": "No folder was selected or GUI is unavailable. Exiting.",
        "invalid": "Error: {value} is not a valid directory.",
        "permission": "Error: no read permission for {value}.",
        "selected": "Selected directory: {value}",
        "done": "Done. Results were saved to {value}.",
        "unexpected": "Unexpected error: {value}",
        "advanced_title": "ADVANCED ANALYSIS RESULTS",
        "time_series": "Time Series Analysis:",
        "patterns": "Error Pattern Analysis:",
        "anomalies": "Anomaly Detection:",
        "correlations": "Correlation Analysis:",
        "statistics": "Summary Statistics:",
        "timeline": "TIMELINE",
        "no_anomalies": "  No anomalies detected.",
        "table": "TABLE",
        "json": "JSON",
        "jsonl": "JSONL",
        "html": "HTML",
    },
}


def normalize_language(language):
    return "en" if str(language).lower() not in MESSAGES else str(language).lower()


def tr(language, key, **kwargs):
    language = normalize_language(language)
    text = MESSAGES[language].get(key, MESSAGES["en"].get(key, key))
    return text.format(**kwargs)
