from pdfminer.converter import PDFConverter
from pdfminer import utils


class CustomTextConverter(PDFConverter):

    def __init__(self, rsrcmgr, outfp, codec='utf-8', pageno=1, laparams=None,
                 showpageno=False, imagewriter=None):
        PDFConverter.__init__(self, rsrcmgr, outfp, codec=codec, pageno=pageno, laparams=laparams)
        self.showpageno = showpageno
        self.imagewriter = imagewriter
        return

    def write_text(self, text):
        self.outfp.write(text.encode(self.codec, 'ignore'))
        return

    def append_to_list(self, text):
        self.outfp.write(text)
        return

    def receive_layout(self, ltpage):
        for i in ltpage:
            for j in i:
                text = j.get_text()
                if text.strip():
                    self.append_to_list('bbox|' + utils.bbox2str(j.bbox) + '|' + text)
        if self.showpageno:
            self.append_to_list('Page %s\n' % ltpage.pageid)
        self.append_to_list('*\n')
        return

    # No need to render image or draw paths, when only interested in text
    def render_image(self, name, stream):
        if self.imagewriter is None:
            return
        PDFConverter.render_image(self, name, stream)
        return

    def paint_path(self, gstate, stroke, fill, evenodd, path):
        return ''
