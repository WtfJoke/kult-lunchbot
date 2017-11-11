import scraper
import pdf_textractor


# starter method
if __name__ == "__main__":
    pdf = scraper.get_pdf()
    text = pdf_textractor.get_menu_text(pdf)
    print(text)