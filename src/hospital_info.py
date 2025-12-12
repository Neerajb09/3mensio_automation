import re
from text_extraction_from_pdf import textExtractionFromPDF

class HospitalInfoExtractor:
    def __init__(self, regex_patterns = {
    "hospital_name": r"Hospital:\s*(.+)",
    "creation_date": r"Creation Date:\s*(.*?)\s*Physician",
    "created_by": r"Created By:\s*(.*?)\s*Hospital",
    "doctor_name": r"Physician:\s*(.+)",
    "city": r"City:\s*(.+)",
    "country": r"Country:\s*(.+)"
}, text =''):
        self.regex_patterns = regex_patterns
        self.text = text

    def extract_info(self):
        extracted_info = {}
        first_page_text = self.text

        for field, pattern in self.regex_patterns.items():
            match = re.search(pattern, first_page_text, re.IGNORECASE)
            extracted_info[field] = match.group(1).strip() if match else None

        return extracted_info

