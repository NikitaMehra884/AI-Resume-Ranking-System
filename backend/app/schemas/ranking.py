from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class ScoringWeightsConfig(BaseModel):
    semantic_weight: Optional[float] = None
    bm25_weight: Optional[float] = None
    required_skill_weight: Optional[float] = None
    preferred_skill_weight: Optional[float] = None
    experience_weight: Optional[float] = None
    education_weight: Optional[float] = None
    career_alignment_weight: Optional[float] = None
    availability_weight: Optional[float] = None

class ScreeningFilterRequest(BaseModel):
    top_k: int = 20
    min_score: Optional[float] = 0.0
    required_skills: Optional[List[str]] = []
    min_experience: Optional[float] = None
    max_experience: Optional[float] = None
    work_mode: Optional[str] = None
    location: Optional[str] = None
    education_tier: Optional[str] = None
    weights: Optional[ScoringWeightsConfig] = None

class RankedCandidateItem(BaseModel):
    rank: int
    candidate_id: str
    name: str
    current_title: str
    current_company: str
    years_of_experience: float
    location: str
    country: str
    final_score: float
    semantic_score: float
    keyword_score: float
    skill_score: float
    experience_score: float
    education_score: float
    career_score: float
    availability_score: float
    matched_skills: List[str]
    missing_skills: List[str]
    status: str = "SCREENING"
    reasons: List[str] = []
    application_id: Optional[int] = None

class ScreeningResponse(BaseModel):
    job_id: int
    job_title: str
    total_candidates_evaluated: int
    returned_count: int
    candidates: List[RankedCandidateItem]
    execution_time_seconds: float

class CandidateMatchReport(BaseModel):
    candidate_id: str
    job_id: int
    match_score: float
    strong_matches: List[str]
    partial_matches: List[str]
    missing_skills: List[str]
    experience_assessment: str
    education_assessment: str
    project_relevance: str
    why_good_match: str
    what_to_improve: str
    evidence_breakdown: Dict[str, Any]

class CandidateComparisonRequest(BaseModel):
    candidate_ids: List[str]

class CandidateComparisonResponse(BaseModel):
    job_id: int
    candidates: List[Dict[str, Any]]
    comparison_summary: str

class InterviewQuestionsResponse(BaseModel):
    candidate_id: str
    job_id: int
    candidate_name: str
    job_title: str
    technical_questions: List[Dict[str, str]]
    behavioral_questions: List[Dict[str, str]]
    project_questions: List[Dict[str, str]]
    role_specific_questions: List[Dict[str, str]]
