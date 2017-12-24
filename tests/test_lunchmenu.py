import unittest
from lunchmenu import KeywordAnalyzer, DateFormats, WeeklyMenu
import datetime


class KeywordAnalyzerTestCase(unittest.TestCase):

    def test_analyze_relative_day_tomorrow(self):
        result = KeywordAnalyzer("kult morgen").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(False, result.is_today())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_relative_day_yesterday(self):
        result = KeywordAnalyzer("kult gestern").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(False, result.is_today())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_relative_day_day_after_tomorrow(self):
        result = KeywordAnalyzer("kult übermorgen").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=+2)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(False, result.is_today())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_relative_day_day_before_tomorrow(self):
        result = KeywordAnalyzer("kult vorgestern").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=-2)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_monday(self):
        result = KeywordAnalyzer("kult montag").analyze()
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(False, result.is_relative_day())
        self.assertEqual('Montag', result.get_day())
