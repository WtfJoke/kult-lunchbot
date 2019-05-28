
from io import StringIO

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    device = None
    try:
        with StringIO() as string_writer, open(path, 'rb') as pdf_file:
            device = create_text_converter(resource_manager, string_writer)
            interpreter = PDFPageInterpreter(resource_manager, device)

            for page in PDFPage.get_pages(pdf_file, maxpages=1):
                interpreter.process_page(page)
                layout = device.get_result()
                parse_layout(layout)

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
    return PDFPageAggregator(resource_manager, laparams=LAParams(char_margin=4))


def parse_layout(layout):
    for lt_obj in layout:
        if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
            text = lt_obj.get_text()
            if text.strip():
                print(lt_obj.bbox)
                print(text)
        elif isinstance(lt_obj, LTFigure):
            parse_layout(lt_obj)


if __name__ == "__main__":
    import scraper
    pdf = scraper.get_pdf()
    print(convert_pdf_to_txt(pdf))
    #import os
    #print(convert_pdf_to_txt(os.path.join('tests', 'files', 'menu', 'buggy', 'friday_no_text_Wochenkarte-KW-6-2018-2.pdf')))


