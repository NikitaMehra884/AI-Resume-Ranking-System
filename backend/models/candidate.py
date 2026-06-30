from dataclasses import dataclass


@dataclass
class Candidate:
    candidate_id: str
    name: str
    years_of_experience: float
    current_title: str
    current_company: str
    location: str
    country: str
    summary: str

    skills: list
    career_history: list
    education: list
    certifications: list
    languages: list
    redrob_signals: dict