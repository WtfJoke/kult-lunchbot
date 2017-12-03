import unittest
import scraper
import os


class KultScraperTestCase(unittest.TestCase):

    def test_get_pdf(self):
        menu_path = scraper.get_pdf()
        self.assertEqual(True, os.path.exists(menu_path))