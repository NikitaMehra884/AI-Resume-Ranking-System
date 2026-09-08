from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    candidate_id = Column(String(64), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    headline = Column(String(255), default="")
    summary = Column(Text, default="")
    years_of_experience = Column(Float, default=0.0)
    current_title = Column(String(255), default="")
    current_company = Column(String(255), default="")
    current_industry = Column(String(255), default="")
    location = Column(String(255), default="")
    country = Column(String(100), default="")
    work_mode_preference = Column(String(50), default="flexible")
    willing_to_relocate = Column(Boolean, default=False)
    notice_period_days = Column(Integer, default=30)
    raw_resume_text = Column(Text, default="")
    completeness_score = Column(Float, default=100.0)
    recruiter_response_rate = Column(Float, default=0.5)
    github_activity_score = Column(Float, default=0.0)
    open_to_work = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="candidate_profile")
    skills = relationship("CandidateSkill", back_populates="candidate", cascade="all, delete-orphan")
    career_history = relationship("CandidateExperience", back_populates="candidate", cascade="all, delete-orphan")
    education = relationship("CandidateEducation", back_populates="candidate", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")

class CandidateSkill(Base):
    __tablename__ = "candidate_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String(64), ForeignKey("candidate_profiles.candidate_id", ondelete="CASCADE"), index=True)
    name = Column(String(100), index=True, nullable=False)
    proficiency = Column(String(50), default="intermediate")
    endorsements = Column(Integer, default=0)
    duration_months = Column(Integer, default=0)
    
    candidate = relationship("CandidateProfile", back_populates="skills")

class CandidateExperience(Base):
    __tablename__ = "candidate_experience"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String(64), ForeignKey("candidate_profiles.candidate_id", ondelete="CASCADE"), index=True)
    company = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    start_date = Column(String(50), default="")
    end_date = Column(String(50), nullable=True)
    duration_months = Column(Integer, default=0)
    is_current = Column(Boolean, default=False)
    industry = Column(String(100), default="")
    description = Column(Text, default="")
    
    candidate = relationship("CandidateProfile", back_populates="career_history")

class CandidateEducation(Base):
    __tablename__ = "candidate_education"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(String(64), ForeignKey("candidate_profiles.candidate_id", ondelete="CASCADE"), index=True)
    institution = Column(String(255), nullable=False)
    degree = Column(String(100), default="")
    field_of_study = Column(String(255), default="")
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    grade = Column(String(50), default="")
    tier = Column(String(50), default="unknown")
    
    candidate = relationship("CandidateProfile", back_populates="education")
