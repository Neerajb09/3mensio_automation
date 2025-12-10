import pdfplumber
import re

class HospitalInfoExtractor:
    def __init__(self, regex_patterns = {
    "hospital_name": r"Hospital:\s*(.+)",
    "creation_date": r"Creation Date:\s*(.+)",
    "created_by": r"Created By:\s*(.+)",
    "doctor_name": r"Physician:\s*(.+)",
    "city": r"City:\s*(.+)",
    "country": r"Country:\s*(.+)"
}):
        self.regex_patterns = regex_patterns

    def extract_info(self, report_path):
        extracted_info = {}
        first_page_text = self._extract_first_page_text(report_path)

        for field, pattern in self.regex_patterns.items():
            match = re.search(pattern, first_page_text, re.IGNORECASE)
            extracted_info[field] = match.group(1).strip() if match else None

        return extracted_info

    def _extract_first_page_text(self, report_path):
        with pdfplumber.open(report_path) as pdf:
            first_page = pdf.pages[0]
            return first_page.extract_text() or ""

# Example usage:

extractor = HospitalInfoExtractor()
info = extractor.extract_info("/nuvodata/User_data/neeraj/3mensio_automation/dataset/3.3mensio report_31%_R G_Dr. Rohit Mathur_MDM_Jodhpur_corelab.pdf")
print(info)