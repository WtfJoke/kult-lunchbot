import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    device = None
    try:
        with StringIO() as string_writer, open(path, 'rb') as pdf_file:
            device = create_text_converter(resource_manager, string_writer)
            interpreter = PDFPageInterpreter(resource_manager, device)

            for page in PDFPage.get_pages(pdf_file, maxpages=1):
                interpreter.process_page(page)

            pdf_text = string_writer.getvalue()
    finally:
        if device:
            device.close()
    return pdf_text


def convert_pdf_to_txt_lines(path):
    text = convert_pdf_to_txt(path)
    text_lines = list(filter(None, text.split('\n')))  # filter empty values
    return text_lines


def create_text_converter(resource_manager, string_writer):
    codec = 'utf-8'
    return TextConverter(resource_manager, string_writer, codec=codec, laparams=LAParams())


if __name__ == "__main__":
    print(convert_pdf_to_txt(os.path.join('tests', 'files', 'menu', 'buggy', 'friday_no_text_Wochenkarte-KW-6-2018-2.pdf')))