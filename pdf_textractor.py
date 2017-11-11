from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import os


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    try:
        with StringIO() as string_writer, open(path, 'rb') as pdf_file:
            device = create_text_converter(resource_manager, string_writer)
            interpreter = PDFPageInterpreter(resource_manager, device)

            for page in PDFPage.get_pages(pdf_file, maxpages=1):
                interpreter.process_page(page)

            pdf_text = string_writer.getvalue()
    finally:
        device.close()
    return pdf_text


def create_text_converter(resource_manager, string_writer):
    codec = 'utf-8'
    return TextConverter(resource_manager, string_writer, codec=codec, laparams=LAParams())


pdf = os.path.join('menu', 'card.pdf')
text = convert_pdf_to_txt(pdf)
print(text)