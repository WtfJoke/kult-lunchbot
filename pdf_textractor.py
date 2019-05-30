from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTFigure, LTTextLine
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


class PositionedText:
    def __init__(self, text, bbox):
        self.text = text
        self.bbox = bbox
        self.x_min = self.bbox[0]
        self.y_min = self.bbox[1]
        self.x_max = self.bbox[2]
        self.y_max = self.bbox[3]

    def __repr__(self):
        return str(self.bbox) + " " + self.text


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    device = None
    positioned_texts = []
    try:
        with open(path, 'rb') as pdf_file:
            device = create_text_converter(resource_manager)
            interpreter = PDFPageInterpreter(resource_manager, device)

            for page in PDFPage.get_pages(pdf_file, maxpages=1):
                interpreter.process_page(page)
                layout = device.get_result()
                positioned_texts.extend(parse_layout(layout))
    finally:
        if device:
            device.close()
    return sorted(positioned_texts, key=lambda text: text.y_min, reverse=True)


def convert_pdf_to_txt_lines(path):
    positioned_texts = convert_pdf_to_txt(path)
    return positioned_texts


def create_text_converter(resource_manager):
    return PDFPageAggregator(resource_manager, laparams=LAParams(char_margin=4))


def parse_layout(layout):
    positioned_texts = []
    for textbox in layout:
        if isinstance(textbox, LTTextBox):
            parse_textboxes(positioned_texts, textbox)
        elif isinstance(textbox, LTFigure):
            parse_layout(textbox)
    return positioned_texts


def parse_textboxes(positioned_texts, textbox):
    for line in textbox:
        if isinstance(line, LTTextLine):
            text = line.get_text()
            if text.strip():
                positioned_texts.append(PositionedText(text, line.bbox))


if __name__ == "__main__":
    import scraper

    pdf = scraper.get_pdf()
    print(convert_pdf_to_txt(pdf))
