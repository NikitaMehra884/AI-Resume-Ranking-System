from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.core.database import Base

class Application(Base):
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    candidate_id = Column(String(64), ForeignKey("candidate_profiles.candidate_id", ondelete="CASCADE"), index=True)
    status = Column(String(50), default="APPLIED") # APPLIED, SCREENING, SHORTLISTED, INTERVIEW, SELECTED, REJECTED
    match_score = Column(Float, default=0.0)
    evidence_json = Column(Text, default="{}") # Grounded match & ranking breakdown
    applied_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    notes = Column(Text, default="")
    
    @property
    def created_at(self):
        return self.applied_at

    job = relationship("Job", back_populates="applications")
    candidate = relationship("CandidateProfile", back_populates="applications")
    interviews = relationship("Interview", back_populates="application", cascade="all, delete-orphan")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"), index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), index=True)
    candidate_id = Column(String(64), ForeignKey("candidate_profiles.candidate_id", ondelete="CASCADE"), index=True)
    status = Column(String(50), default="SCHEDULED") # SCHEDULED, COMPLETED, CANCELLED
    scheduled_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    questions_json = Column(Text, default="[]") # Phase 15: AI Generated interview questions
    notes = Column(Text, default="")
    
    application = relationship("Application", back_populates="interviews")
