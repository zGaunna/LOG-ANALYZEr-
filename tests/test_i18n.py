import unittest

from log_analyzer.i18n import normalize_language, tr


class TestI18n(unittest.TestCase):
    def test_supported_languages(self):
        self.assertEqual(normalize_language("tr"), "tr")
        self.assertEqual(normalize_language("en"), "en")

    def test_unknown_language_falls_back_to_english(self):
        self.assertEqual(normalize_language("de"), "en")

    def test_translation(self):
        self.assertEqual(tr("tr", "language"), "Arayüz dili")
        self.assertEqual(tr("en", "language"), "Interface language")


if __name__ == "__main__":
    unittest.main()
