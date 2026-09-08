from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class RecruiterProfile(Base):
    __tablename__ = "recruiter_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True, nullable=False)
    company_name = Column(String(255), nullable=False)
    company_size = Column(String(50), default="51-200")
    industry = Column(String(100), default="Technology")
    location = Column(String(255), default="")
    website = Column(String(255), default="")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="recruiter_profile")
    jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("recruiter_profiles.id"), index=True, nullable=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=False)
    department = Column(String(100), default="Engineering")
    location = Column(String(255), default="Remote")
    work_mode = Column(String(50), default="hybrid") # remote, hybrid, onsite
    employment_type = Column(String(50), default="full-time") # full-time, contract, part-time
    minimum_experience = Column(Float, default=0.0)
    maximum_experience = Column(Float, default=20.0)
    education_requirement = Column(String(100), default="Bachelor")
    target_shortlist_count = Column(Integer, default=20)
    status = Column(String(50), default="PUBLISHED") # DRAFT, PUBLISHED, CLOSED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    recruiter = relationship("RecruiterProfile", back_populates="jobs")
    skills = relationship("JobSkill", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    @property
    def applicant_count(self) -> int:
        return len(self.applications) if self.applications else 0

    @property
    def shortlisted_count(self) -> int:
        return len([a for a in self.applications if a.status == "SHORTLISTED"]) if self.applications else 0

class JobSkill(Base):
    __tablename__ = "job_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    name = Column(String(100), index=True, nullable=False)
    is_required = Column(Boolean, default=True) # Phase 7: Required vs Preferred distinction
    
    job = relationship("Job", back_populates="skills")
