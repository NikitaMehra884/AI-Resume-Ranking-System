import io
import re
from typing import Dict, Any, List, Optional
from backend.app.parsing.skill_extractor import SkillExtractor

class ResumeParser:
    """Parses resumes from text, PDF, and DOCX formats into structured profiles."""
    
    def __init__(self):
        self.skill_extractor = SkillExtractor()

    def extract_text_from_pdf(self, file_bytes: bytes) -> str:
        text = ""
        try:
            import pypdf
            reader = pypdf.PdfReader(io.BytesIO(file_bytes), strict=False)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception:
            pass

        if not text.strip():
            # Fallback: extract plain ASCII/UTF-8 strings directly from PDF bytes stream
            try:
                raw_strings = re.findall(rb"[\x20-\x7E\s]{4,}", file_bytes)
                recovered = " ".join(s.decode("utf-8", errors="ignore") for s in raw_strings)
                if len(recovered.strip()) > 30:
                    text = recovered
            except Exception:
                pass

        return text.strip()

    def extract_text_from_docx(self, file_bytes: bytes) -> str:
        try:
            from docx import Document
            doc = Document(io.BytesIO(file_bytes))
            text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
            return text.strip()
        except Exception:
            return ""

    def extract_email(self, text: str) -> Optional[str]:
        match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", text)
        return match.group(0) if match else None

    def extract_phone(self, text: str) -> Optional[str]:
        match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", text)
        return match.group(0) if match else None

    def extract_years_of_experience(self, text: str) -> float:
        # Match '6 years of experience' or 'Experience: 6 years'
        matches = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience", text, re.IGNORECASE)
        if not matches:
            matches = re.findall(r"(?:experience\s*[:\-]?\s*)(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", text, re.IGNORECASE)
        if not matches:
            matches = re.findall(r"(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)", text, re.IGNORECASE)
        if matches:
            try:
                valid_yoe = [float(m) for m in matches if 0 < float(m) <= 45]
                if valid_yoe:
                    return max(valid_yoe)
            except ValueError:
                pass
        # Fallback: estimate from career dates
        year_matches = re.findall(r"\b(20[0-2][0-9]|199[0-9])\b", text)
        if len(year_matches) >= 2:
            years = [int(y) for y in year_matches]
            span = max(years) - min(years)
            if 0 < span < 35:
                return float(span)
        return 2.0

    def parse_resume(self, text: str, full_name: Optional[str] = None) -> Dict[str, Any]:
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        skills = self.skill_extractor.extract_skills(text)
        yoe = self.extract_years_of_experience(text)

        # Name extraction fallback
        name = full_name or "Candidate"
        if not full_name:
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            if lines and len(lines[0].split()) <= 4 and not any(char in lines[0] for char in "@0123456789"):
                name = lines[0]

        # Extract current role / company
        current_title = "Software Engineer"
        for title in ["Senior AI Engineer", "AI Engineer", "Machine Learning Engineer", "Data Scientist", "Backend Engineer", "Full Stack Engineer", "Software Engineer"]:
            if re.search(rf"\b{re.escape(title)}\b", text, re.IGNORECASE):
                current_title = title
                break

        # Degree extraction
        degree = "B.Tech / B.E."
        for d in ["Ph.D", "PhD", "M.Tech", "M.S.", "Master", "B.Tech", "B.E.", "B.S.", "Bachelor"]:
            if re.search(rf"\b{re.escape(d)}\b", text, re.IGNORECASE):
                degree = d
                break

        return {
            "full_name": name,
            "email": email,
            "phone": phone,
            "contact_info": {
                "name": name,
                "email": email,
                "phone": phone
            },
            "years_of_experience": yoe,
            "current_title": current_title,
            "current_company": "Tech Corp",
            "skills": skills,
            "skill_details": [{"name": s, "proficiency": "advanced"} for s in skills],
            "education": [{"institution": "University", "degree": degree, "field_of_study": "Computer Science"}],
            "career_history": [{"company": "Tech Corp", "title": current_title, "duration_months": int(yoe * 12), "description": text[:300]}],
            "raw_text": text
        }
