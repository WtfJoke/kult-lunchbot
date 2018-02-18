import unittest
import datetime
from menu.weeklymenu import WeeklyMenu


class WeeklyMenuTestCase(unittest.TestCase):

    def test_is_current_with_future_date(self):
        in_a_week_date = datetime.date.today() + datetime.timedelta(days=7)
        self.assertEqual(False, WeeklyMenu().is_current(in_a_week_date))

    def test_is_current_with_current_date(self):
        today = datetime.date.today()
        self.assertEqual(True, WeeklyMenu().is_current(today))
