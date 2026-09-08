import re
from typing import Dict, Any, List
from backend.app.parsing.skill_extractor import SkillExtractor

class JDParser:
    """Extracts structured requirements from raw Job Descriptions."""
    
    def __init__(self):
        self.skill_extractor = SkillExtractor()

    def extract_experience(self, text: str) -> float:
        text_clean = text.replace("–", "-").replace("—", "-")
        # Matches patterns like "5-9 years", "5+ years", "minimum 3 years"
        match = re.search(r"(\d+)\s*(?:-|to)\s*(\d+)\s*(?:years|yrs)", text_clean, re.IGNORECASE)
        if match:
            return float(match.group(1))
        match_min = re.search(r"(?:minimum|at least)\s*(\d+)\s*(?:years|yrs)", text_clean, re.IGNORECASE)
        if match_min:
            return float(match_min.group(1))
        match_plus = re.search(r"(\d+)\+\s*(?:years|yrs)", text_clean, re.IGNORECASE)
        if match_plus:
            return float(match_plus.group(1))
        return 2.0

    def parse_jd(self, text: str, title: str = "Software Role") -> Dict[str, Any]:
        all_skills = self.skill_extractor.extract_skills(text)
        min_exp = self.extract_experience(text)

        # Distinguish REQUIRED from PREFERRED (Phase 7)
        required_keywords = ["must have", "mandatory", "required", "requirements", "essential", "things you absolutely need", "must"]
        preferred_keywords = ["nice to have", "preferred", "bonus", "plus", "like you to have"]

        req_skills = []
        pref_skills = []

        text_lower = text.lower()
        req_section = ""
        pref_section = ""

        # Check section headings
        for kw in required_keywords:
            if kw in text_lower:
                parts = text_lower.split(kw, 1)
                req_section = parts[1][:1000]
                break

        for kw in preferred_keywords:
            if kw in text_lower:
                parts = text_lower.split(kw, 1)
                pref_section = parts[1][:1000]
                break

        if req_section:
            req_skills = self.skill_extractor.extract_skills(req_section)
        if pref_section:
            pref_skills = self.skill_extractor.extract_skills(pref_section)

        # Fallback if no specific section markers: top 60% are required, remaining are preferred
        if not req_skills:
            split_idx = max(1, int(len(all_skills) * 0.65))
            req_skills = all_skills[:split_idx]
            pref_skills = all_skills[split_idx:]
        else:
            # Add remaining unclassified skills as preferred
            classified = set(req_skills).union(set(pref_skills))
            for s in all_skills:
                if s not in classified:
                    pref_skills.append(s)

        # Extract Work Mode
        work_mode = "hybrid"
        if "remote" in text_lower:
            work_mode = "remote"
        elif "onsite" in text_lower or "on-site" in text_lower:
            work_mode = "onsite"

        # Seniority
        seniority = "Mid-Senior"
        if any(w in text_lower for w in ["principal", "staff", "lead", "architect", "founding"]):
            seniority = "Staff / Principal"
        elif any(w in text_lower for w in ["senior", "sr."]):
            seniority = "Senior"
        elif any(w in text_lower for w in ["junior", "entry", "intern"]):
            seniority = "Junior"

        return {
            "job_title": title,
            "required_skills": sorted(set(req_skills)),
            "preferred_skills": sorted(set(pref_skills)),
            "minimum_experience": min_exp,
            "maximum_experience": min_exp + 4.0,
            "education": "Bachelor / Master in Computer Science or related field",
            "responsibilities": [
                "Architect and develop scalable AI/backend systems",
                "Design and optimize high-throughput retrieval and ranking pipelines",
                "Deploy machine learning models to production infrastructure"
            ],
            "location": "Pune / Noida / Remote",
            "work_mode": work_mode,
            "employment_type": "full-time",
            "domain": "Artificial Intelligence / Machine Learning",
            "seniority": seniority,
            "keywords": all_skills
        }
