from text_extraction_from_pdf import textExtractionFromPDF
from hospital_info import HospitalInfoExtractor
from demographic_value import DemographicInfoExtractor
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class main:
    def __init__(self, reprt_path):
        self.report_path = reprt_path
    
    def info_extraction(self):
        text = textExtractionFromPDF().extract_first_page_text(self.report_path)
        Hospital_info = HospitalInfoExtractor(text=text)
        demographic = DemographicInfoExtractor(text=text)
        demo_info=demographic.extract_info()
        info = Hospital_info.extract_info()
        info.update(demo_info)
        return info

a = main("/nuvodata/User_data/neeraj/3mensio_automation/dataset/3.3mensio report_31%_R G_Dr. Rohit Mathur_MDM_Jodhpur_corelab.pdf")
info = a.info_extraction()
for key, value in info.items():
    print(key, ":", value)
