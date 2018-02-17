import unittest

from menu.kult_textractor import KultTexTractor
import os


class KultTextTractorTestCase(unittest.TestCase):

    test_files_root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")

    example_pdf = os.path.join(test_files_root, "menu", "examples", "card.pdf")
    buggy_menu_pdf = os.path.join(test_files_root, "menu", "buggy", "buggy_menu_tue_before_menu3_monday.pdf")
    friday_no_text_pdf = os.path.join(test_files_root, "menu", "buggy", "friday_no_text_Wochenkarte-KW-6-2018-2.pdf")
    friday2_no_text_pdf =  os.path.join(test_files_root, "menu", "buggy", "friday_no_text2_Wochenkarte-KW-7-2018.pdf")

    def test_get_menu_amount_with_example(self):
        menu = KultTexTractor.get_menu_from_pdf(self.example_pdf)
        self.assertEqual(5, len(menu.get_daily_menus()))
        for daily_menu in menu.get_daily_menus():
            self.assertEqual(3, len(daily_menu.get_menu_items()))

    def test_get_menu_monday_content_with_example(self):
        menu = KultTexTractor.get_menu_from_pdf(self.example_pdf)
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
        menu = KultTexTractor.get_menu_from_pdf(self.example_pdf)
        daily_menu = menu.get_daily_menus()[1]
        expected_tuesday_menu_text = "Kl. Salat | Fischfilet mit Kräuterhaube und Duftreis | Dessert"
        self.assertEqual("Dienstag", daily_menu.get_weekday())
        self.assertEqual("07.11.2017", daily_menu.get_date())
        menus = daily_menu.get_menu_items()
        self.assertEqual(expected_tuesday_menu_text, menus[0].get_menu_content())
        self.assertEqual(1, menus[0].get_menu_number())
        self.assertEqual("Kl. Salat | Currywurst mit Pommes", menus[1].get_menu_content())
        self.assertEqual(2, menus[1].get_menu_number())
        self.assertEqual("Spätzlepfanne mit Marktgemüse (vegetarisch)", menus[2].get_menu_content())
        self.assertEqual(3, menus[2].get_menu_number())

    def test_get_buggy_menu_monday_content(self):
        menu = KultTexTractor.get_menu_from_pdf(self.buggy_menu_pdf)
        daily_menu = menu.get_daily_menus()[0]
        expected_monday_menu_text = "Kl. Salat | Lachs – Spinat-Türmchen an Reis und Spinat Sauce | Dessert"
        self.assertEqual("Montag", daily_menu.get_weekday())
        self.assertEqual("27.11.2017", daily_menu.get_date())
        menus = daily_menu.get_menu_items()
        self.assertEqual(expected_monday_menu_text, menus[0].get_menu_content())
        self.assertEqual(1, menus[0].get_menu_number())
        self.assertEqual("Kl. Salat | Pizza nach Wahl", menus[1].get_menu_content())
        self.assertEqual(2, menus[1].get_menu_number())
        self.assertEqual("Pasta al forno(vegetarisch)", menus[2].get_menu_content())
        self.assertEqual(3, menus[2].get_menu_number())

    def test_get_buggy_menu_tuesday_content(self):
        menu = KultTexTractor.get_menu_from_pdf(self.buggy_menu_pdf)
        daily_menu = menu.get_daily_menus()[1]
        # TODO menu text with price - fix me
        expected_tuesday_menu_text = "Kl. Salat | Schweinemedaillons mit Pilzrahmsauce mit Bandnudeln | Dessert  9,80"
        self.assertEqual("Dienstag", daily_menu.get_weekday())
        self.assertEqual("28.11.2017", daily_menu.get_date())
        menus = daily_menu.get_menu_items()
        self.assertEqual(expected_tuesday_menu_text, menus[0].get_menu_content())
        self.assertEqual(1, menus[0].get_menu_number())
        self.assertEqual("Kl. Salat | Fafalle an Lachsssauce", menus[1].get_menu_content())
        self.assertEqual(2, menus[1].get_menu_number())
        self.assertEqual("Herbstlicher Auflauf mit Kürbis (vegetarisch)", menus[2].get_menu_content())
        self.assertEqual(3, menus[2].get_menu_number())

    def test_get_buggy_menu_friday_no_text_content(self):
        menu = KultTexTractor.get_menu_from_pdf(self.friday_no_text_pdf)
        daily_menu = menu.get_daily_menus()[4]
        expected_tuesday_menu_text = "Kartoffel-Gemüse-Pfanne (vegetarisch)"
        menus = daily_menu.get_menu_items()
        self.assertEqual(3, menus[2].get_menu_number())
        self.assertEqual(expected_tuesday_menu_text, menus[2].get_menu_content())

    def test_get_buggy_menu_friday2_no_text_content(self):
        menu = KultTexTractor.get_menu_from_pdf(self.friday2_no_text_pdf)
        daily_menu = menu.get_daily_menus()[4]
        expected_tuesday_menu_text = "Linsencurry mit CousCous (vegetarisch)"
        menus = daily_menu.get_menu_items()
        self.assertEqual(3, menus[2].get_menu_number())
        self.assertEqual(expected_tuesday_menu_text, menus[2].get_menu_content())

