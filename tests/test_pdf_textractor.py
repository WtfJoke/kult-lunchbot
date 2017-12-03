import unittest
import pdf_textractor
import os


class PdfTextTractorTestCase(unittest.TestCase):

    example_pdf = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files", "examples", "card.pdf")

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
        menus = daily_menu.get_menu_items()
        self.assertEqual(expected_monday_menu_text, menus[0].get_menu_content())
        self.assertEqual(1, menus[0].get_menu_number())
        self.assertEqual("Kl. Salat | Gratinierter Fisch mit Reis", menus[1].get_menu_content())
        self.assertEqual(2, menus[1].get_menu_number())
        self.assertEqual("Penne Arrabiata (vegetarisch)", menus[2].get_menu_content())
        self.assertEqual(3, menus[2].get_menu_number())

    def test_get_menu_tuesday_content_with_example(self):
        menu = pdf_textractor.get_menu_from_pdf(self.example_pdf)
        daily_menu = menu.get_daily_menus()[1]
        expected_monday_menu_text = "Kl. Salat | Fischfilet mit Kräuterhaube und Duftreis | Dessert"
        self.assertEqual("Dienstag", daily_menu.get_weekday())
        self.assertEqual("07.11.2017", daily_menu.get_date())
        menus = daily_menu.get_menu_items()
        self.assertEqual(expected_monday_menu_text, menus[0].get_menu_content())
        self.assertEqual(1, menus[0].get_menu_number())
        self.assertEqual("Kl. Salat | Currywurst mit Pommes", menus[1].get_menu_content())
        self.assertEqual(2, menus[1].get_menu_number())
        self.assertEqual("Spätzlepfanne mit Marktgemüse (vegetarisch)", menus[2].get_menu_content())
        self.assertEqual(3, menus[2].get_menu_number())