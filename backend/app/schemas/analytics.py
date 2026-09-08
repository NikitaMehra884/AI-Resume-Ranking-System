from typing import List
from pydantic import BaseModel

class PipelineStageCount(BaseModel):
    applied: int = 0
    screening: int = 0
    shortlisted: int = 0
    interview: int = 0
    selected: int = 0
    rejected: int = 0
    total: int = 0

class SkillDistributionItem(BaseModel):
    skill: str
    count: int

class ScoreBucket(BaseModel):
    bucket: str
    count: int

class RecruiterAnalyticsResponse(BaseModel):
    total_jobs: int
    active_jobs: int
    total_applicants: int
    pipeline: PipelineStageCount
    average_match_score: float
    top_skills: List[SkillDistributionItem]
    score_distribution: List[ScoreBucket]
