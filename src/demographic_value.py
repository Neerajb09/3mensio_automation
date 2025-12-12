import re
from typing import Optional, Tuple, Dict, Any


class DemographicInfoExtractor:
    def __init__(self, regex_patterns=None, text: str = ""):
        default_patterns = {
            "patient_name": r"Name[s]?\s*:\s*(.*?)(?=\s*Height[s]?\s*:|\n|$)",
            "gender_primary": r"Gender[s]?\s*:\s*(Male|Female|M|F)\b(?=\s*Weight[s]?\s*:|\n|$)",
            "gender_secondary": (r"(?:Year\s*Of\s*Birth\s*\(*\s*Age\s*\)*|Year|Age)\s*:\s*" r".*?\b(Male|Female|M|F)\b.*?(?=\s*BMIs?\s*:|\n|$)"),
            "year_age": (r"(?:Year\s*Of\s*Birth\s*\(*\s*Age\s*\)*|Year|Age)\s*:\s*" r"(.*?)(?=\s*BMIs?\s*:|\n|$)"),
            "patient_initial": r"Name[s]?\s*:\s*(?:([A-Za-z])[A-Za-z]*\s+([A-Za-z])[A-Za-z]*)",
            "patient_id": r"^(?P<pid>.*?){patient_name}\b.*$",
        }

        self.regex_patterns = regex_patterns or default_patterns
        self.text = text

    def _extract_year_and_age(self, block: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        year = None
        age = None

        if not block:
            return year, age
        
        myear = re.search(r"\b(19|20)\d{2}\b", block)
        search_for_age_in = block
        if myear:
            year = myear.group(0)
            search_for_age_in = block[myear.end():]

        mage = re.search(r"\b(\d{1,3})\s*" r"(?:y|yr|yrs|year|years)?" r"(?:\s*/?\s*[mf])?",search_for_age_in,flags=re.IGNORECASE,)
        if mage:
            age = mage.group(1)
        return year, age

    def extract_info(self) -> Dict[str, Any]:
        text = self.text
        extracted_blocks: Dict[str, Optional[str]] = {}
        for key, pattern in self.regex_patterns.items():
            if key == "patient_id":
                continue
            match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
            if match:
                extracted_blocks[key] = match.group(1) if match.lastindex else match.group(0)
            else:
                extracted_blocks[key] = None
        result = {}

        patient_name = extracted_blocks.get("patient_name")
        if patient_name:
            patient_name = patient_name.strip()
        result["patient_name"] = patient_name

        gender_raw = extracted_blocks.get("gender_primary") or extracted_blocks.get("gender_secondary")
        if gender_raw:
            gender_raw = gender_raw.strip()
            gender = gender_raw.upper() if len(gender_raw) == 1 else gender_raw.capitalize()
        else:
            gender = None
        result["gender"] = gender

        year_block = extracted_blocks.get("year_age")
        year, age = self._extract_year_and_age(year_block)
        result["year"] = year
        result["age"] = age

        initials_match = re.search(self.regex_patterns["patient_initial"], text, flags=re.IGNORECASE)
        if initials_match:
            initials = "".join(g.upper() for g in initials_match.groups() if g)
        else:
            initials = None
        result["patient_initial"] = initials

        patient_id = None
        if patient_name:
            last_line = text.strip().splitlines()[-1] if text.strip() else ""
            pid_pattern = self.regex_patterns["patient_id"].format(patient_name=re.escape(patient_name))
            m_pid = re.search(pid_pattern, last_line, flags=re.IGNORECASE)
            if m_pid:
                pid = m_pid.group("pid").strip()
                patient_id = pid if pid else None
        result["patient_id"] = patient_id

        return result
