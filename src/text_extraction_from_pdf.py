import pdfplumber

class textExtractionFromPDF:
    def __init__(self):
        pass

    def extract_first_page_text(self, report_path):
        with pdfplumber.open(report_path) as pdf:
            first_page = pdf.pages[0]
            return first_page.extract_text() or ""
        
    def extract_text_from_second_page(self, report_path):
        text = ''
        with pdfplumber.open(report_path) as pdf:
            if len(pdf.pages) > 1:
                for i in range(1,len(pdf.pages)):
                    second_page = pdf.pages[i]
                    text += second_page.extract_text() or ""
        return second_page.extract_text() or ""