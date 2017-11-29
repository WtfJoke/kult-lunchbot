import unittest
from lunchmenu import KeywordAnalyzer, DateFormats
import datetime


class KeywordAnalyzerTestCase(unittest.TestCase):

    def test_analyze_relative_day_tomorrow(self):
        result = KeywordAnalyzer("essen morgen").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_relative_day_yesterday(self):
        result = KeywordAnalyzer("essen gestern").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=-1)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_relative_day_day_after_tomorrow(self):
        result = KeywordAnalyzer("essen übermorgen").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=+2)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(expected_date, result.get_date())

    def test_analyze_relative_day_day_before_tomorrow(self):
        result = KeywordAnalyzer("essen vorgestern").analyze()
        expected_date = (datetime.date.today() + datetime.timedelta(days=-2)).strftime(DateFormats.COMMON)
        self.assertEqual(True, result.is_triggered())
        self.assertEqual(True, result.is_relative_day())
        self.assertEqual(expected_date, result.get_date())