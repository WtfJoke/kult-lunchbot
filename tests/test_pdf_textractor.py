import unittest
import pdf_textractor
import os


class PdfTextTractorTestCase(unittest.TestCase):

    example_pdf = os.path.join(os.getcwd(), "files", "examples", "card.pdf")

    def test_get_menu_amount_with_example(self):
        menu = pdf_textractor.get_menu_from_pdf(self.example_pdf)
        self.assertEqual(5, len(menu.get_daily_menus()))
        for daily_menu in menu.get_daily_menus():
            self.assertEqual(3, len(daily_menu.get_menu_items()))

    def test_get_menu_monday_content_with_example(self):
        menu = pdf_textractor.get_menu_from_pdf(self.example_pdf)
        daily_menu = menu.get_daily_menus()[0]
        expected_monday_menu_text = "Kl. Salat | Hähnchenbrust, dazu Gemüse & Wedges | Dessert"
        self.assertEqual("Montag", daily_menu.get_weekday())
        self.assertEqual("06.11.2017", daily_menu.get_date())
        self.assertEqual(expected_monday_menu_text, daily_menu.get_menu_items()[0].get_menu_content())
