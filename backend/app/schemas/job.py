from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class JobSkillItem(BaseModel):
    name: str
    is_required: bool = True

class JobCreate(BaseModel):
    title: str
    description: str
    department: Optional[str] = "Engineering"
    location: Optional[str] = "Remote"
    work_mode: Optional[str] = "hybrid" # remote, hybrid, onsite
    employment_type: Optional[str] = "full-time"
    minimum_experience: Optional[float] = 0.0
    maximum_experience: Optional[float] = 20.0
    education_requirement: Optional[str] = "Bachelor"
    target_shortlist_count: Optional[int] = 20
    required_skills: List[str] = []
    preferred_skills: List[str] = []

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    employment_type: Optional[str] = None
    minimum_experience: Optional[float] = None
    maximum_experience: Optional[float] = None
    education_requirement: Optional[str] = None
    target_shortlist_count: Optional[int] = None
    status: Optional[str] = None
    required_skills: Optional[List[str]] = None
    preferred_skills: Optional[List[str]] = None

class JobOut(BaseModel):
    id: int
    recruiter_id: Optional[int] = None
    company_name: Optional[str] = "HireSense"
    title: str
    description: str
    department: str
    location: str
    work_mode: str
    employment_type: str
    minimum_experience: float
    maximum_experience: float
    education_requirement: str
    target_shortlist_count: int
    status: str
    skills: List[JobSkillItem] = []
    applicant_count: int = 0
    shortlisted_count: int = 0
    created_at: datetime
    
    model_config = {"from_attributes": True}

class JDAnalysisResponse(BaseModel):
    job_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    minimum_experience: float
    education: str
    responsibilities: List[str]
    location: str
    work_mode: str
    employment_type: str
    domain: str
    seniority: str
    keywords: List[str]
