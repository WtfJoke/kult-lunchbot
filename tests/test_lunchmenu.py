import unittest
from menu.lunchmenu import KeywordAnalyzer, DateFormats
import datetime
from menu.kult_textractor import KultTexTractor
import os


class KeywordAnalyzerTestCase(unittest.TestCase):

    def test_analyze_relative_day_tomorrow(self):
        result = KeywordAnalyzer("kult morgen").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(False, result.is_today())
        self.assertEqual(expected_date, result.get_date())
        self.assertEqual("kult", result.triggered_word)

    def test_analyze_relative_day_yesterday(self):
        result = KeywordAnalyzer("kult gestern").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(False, result.is_today())
        self.assertEqual(expected_date, result.get_date())
        self.assertEqual("kult", result.triggered_word)

    def test_analyze_relative_day_day_after_tomorrow(self):
        result = KeywordAnalyzer("kult übermorgen").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=+2)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(False, result.is_today())
        self.assertEqual(expected_date, result.get_date())
        self.assertEqual("kult", result.triggered_word)

    def test_analyze_relative_day_day_before_tomorrow(self):
        result = KeywordAnalyzer("kult vorgestern").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=-2)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(expected_date, result.get_date())
        self.assertEqual("kult", result.triggered_word)

    def test_analyze_monday(self):
        result = KeywordAnalyzer("kult montag").analyze()
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(False, result.is_relative_day())
        self.assertEqual('Montag', result.get_day())
        self.assertEqual("kult", result.triggered_word)

    def test_analyze_monday_koelle(self):
        result = KeywordAnalyzer("kölle montag").analyze()
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(False, result.is_relative_day())
        self.assertEqual('Montag', result.get_day())
        self.assertEqual("kölle", result.triggered_word)

    def test_is_special(self):
        result = KeywordAnalyzer(":zornig:").analyze()
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_special())
        self.assertEqual(False, result.is_relative_day())


class WeeklyMenuTestCase(unittest.TestCase):

    def setUp(self):
        test_root = os.path.dirname(os.path.realpath(__file__))
        example_pdf = os.path.join(test_root, "files", "menu", "examples", "card.pdf")
        self.sample_menu = KultTexTractor.get_menu_from_pdf(example_pdf)

    def test_get_daily_menu_by_weekday_monday(self):
        current_menu = self.sample_menu.get_daily_menu_by_weekday("Montag")
        self.assertIsNotNone(current_menu)
        self.assertEqual(True, current_menu.is_complete())
        self.assertEqual(3, len(current_menu.get_menu_items()))

    def test_get_daily_menu_by_weekday_sunday(self):
        self.assertIsNone(self.sample_menu.get_daily_menu_by_weekday("Sonntag"))

    def test_get_daily_menu_by_date_06_11_17(self):
        date = datetime.date(2017, 11, 6).strftime(DateFormats.COMMON)
        current_menu = self.sample_menu.get_daily_menu_by_date(date)
        self.assertIsNotNone(current_menu)
        self.assertEqual(True, current_menu.is_complete())
        self.assertEqual(3, len(current_menu.get_menu_items()))

    def test_get_daily_menu_by_date_not_available(self):
        date = datetime.date(2017, 12, 6).strftime(DateFormats.COMMON)
        self.assertIsNone(self.sample_menu.get_daily_menu_by_date(date))

    def test_get_title_sample(self):
        self.assertEqual("KW 45 06.11. – 10.11.2017", self.sample_menu.get_title())
