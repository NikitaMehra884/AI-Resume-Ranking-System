from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class SkillItem(BaseModel):
    name: str
    proficiency: Optional[str] = "intermediate"
    endorsements: Optional[int] = 0
    duration_months: Optional[int] = 0

class ExperienceItem(BaseModel):
    company: str
    title: str
    start_date: Optional[str] = ""
    end_date: Optional[str] = None
    duration_months: Optional[int] = 0
    is_current: Optional[bool] = False
    industry: Optional[str] = ""
    description: Optional[str] = ""

class EducationItem(BaseModel):
    institution: str
    degree: Optional[str] = ""
    field_of_study: Optional[str] = ""
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    grade: Optional[str] = ""
    tier: Optional[str] = "unknown"

class CandidateProfileCreate(BaseModel):
    full_name: str
    headline: Optional[str] = ""
    summary: Optional[str] = ""
    years_of_experience: Optional[float] = 0.0
    current_title: Optional[str] = ""
    current_company: Optional[str] = ""
    current_industry: Optional[str] = ""
    location: Optional[str] = ""
    country: Optional[str] = ""
    work_mode_preference: Optional[str] = "flexible"
    willing_to_relocate: Optional[bool] = False
    notice_period_days: Optional[int] = 30
    skills: List[SkillItem] = []
    career_history: List[ExperienceItem] = []
    education: List[EducationItem] = []

class CandidateProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    years_of_experience: Optional[float] = None
    current_title: Optional[str] = None
    current_company: Optional[str] = None
    current_industry: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None
    work_mode_preference: Optional[str] = None
    willing_to_relocate: Optional[bool] = None
    notice_period_days: Optional[int] = None
    skills: Optional[List[SkillItem]] = None
    career_history: Optional[List[ExperienceItem]] = None
    education: Optional[List[EducationItem]] = None

class CandidateProfileOut(BaseModel):
    id: int
    user_id: Optional[int] = None
    candidate_id: str
    full_name: str
    headline: Optional[str] = ""
    summary: Optional[str] = ""
    years_of_experience: float
    current_title: Optional[str] = ""
    current_company: Optional[str] = ""
    location: Optional[str] = ""
    country: Optional[str] = ""
    work_mode_preference: Optional[str] = "flexible"
    willing_to_relocate: bool
    notice_period_days: int
    completeness_score: float
    skills: List[SkillItem] = []
    career_history: List[ExperienceItem] = []
    education: List[EducationItem] = []
    created_at: datetime
    
    model_config = {"from_attributes": True}
