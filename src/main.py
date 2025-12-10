from text_extraction_from_pdf import textExtractionFromPDF
from hospital_info import HospitalInfoExtractor

class main:
    def __init__(self, reprt_path):
        self.report_path = reprt_path
        pass
    def info_extraction(self):
        text = textExtractionFromPDF().extract_first_page_text(self.report_path)
        extractor = HospitalInfoExtractor(text=text)
        info = extractor.extract_info()
        return info

a = main("/nuvodata/User_data/neeraj/3mensio_automation/dataset/3.3mensio report_31%_R G_Dr. Rohit Mathur_MDM_Jodhpur_corelab.pdf")
info = a.info_extraction()
print(info)
