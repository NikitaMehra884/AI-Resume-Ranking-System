from pathlib import Path
from sqlalchemy.orm import Session
from backend.app.core.database import SessionLocal, init_db
from backend.app.core.security import get_password_hash
from backend.app.models.user import User
from backend.app.models.job import Job, JobSkill, RecruiterProfile
from backend.app.models.candidate import CandidateProfile, CandidateSkill, CandidateExperience, CandidateEducation
from backend.app.models.application import Application

def seed():
    print("Initializing DB...")
    init_db()
    db: Session = SessionLocal()

    try:
        # 1. Create Recruiter
        recruiter_user = db.query(User).filter(User.email == "recruiter@platform.ai").first()
        if not recruiter_user:
            recruiter_user = User(
                email="recruiter@platform.ai",
                hashed_password=get_password_hash("password123"),
                role="RECRUITER"
            )
            db.add(recruiter_user)
            db.commit()
            db.refresh(recruiter_user)

            rec_prof = RecruiterProfile(
                user_id=recruiter_user.id,
                company_name="Redrob AI",
                company_size="51-200",
                industry="AI & Talent Intelligence",
                location="Pune / Noida, India",
                website="https://redrob.ai"
            )
            db.add(rec_prof)
            db.commit()
            db.refresh(rec_prof)
            recruiter_id = rec_prof.id
        else:
            rec_prof = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == recruiter_user.id).first()
            recruiter_id = rec_prof.id if rec_prof else None

        # 2. Create Candidate
        cand_user = db.query(User).filter(User.email == "candidate@platform.ai").first()
        if not cand_user:
            cand_user = User(
                email="candidate@platform.ai",
                hashed_password=get_password_hash("password123"),
                role="CANDIDATE"
            )
            db.add(cand_user)
            db.commit()
            db.refresh(cand_user)

            cand_prof = CandidateProfile(
                user_id=cand_user.id,
                candidate_id="CAND_DEMO01",
                full_name="Alex Morgan",
                headline="Senior AI / ML Engineer | PyTorch, FAISS, LLMs",
                summary="AI engineer with 5.5 years of experience building vector search systems, RAG pipelines, and high-throughput ranking engines.",
                years_of_experience=5.5,
                current_title="AI Engineer",
                current_company="Sarvam AI",
                location="Bangalore",
                country="India",
                work_mode_preference="hybrid",
                willing_to_relocate=True,
                notice_period_days=30,
                completeness_score=100.0,
                recruiter_response_rate=0.88,
                open_to_work=True
            )
            db.add(cand_prof)
            db.commit()
            db.refresh(cand_prof)

            # Skills
            for s in ["python", "pytorch", "faiss", "rag", "llm", "fastapi", "docker", "machine learning"]:
                db.add(CandidateSkill(candidate_id=cand_prof.candidate_id, name=s, proficiency="expert"))

            # Experience
            db.add(CandidateExperience(
                candidate_id=cand_prof.candidate_id,
                company="Sarvam AI",
                title="AI Engineer",
                start_date="2022-01-01",
                duration_months=30,
                is_current=True,
                description="Designed low-latency vector search pipeline using FAISS and SentenceTransformers, handling 2M embeddings."
            ))
            # Education
            db.add(CandidateEducation(
                candidate_id=cand_prof.candidate_id,
                institution="IIT Delhi",
                degree="B.Tech",
                field_of_study="Computer Science",
                start_year=2015,
                end_year=2019,
                tier="tier_1"
            ))
            db.commit()

        # 3. Create Benchmark Job
        job = db.query(Job).filter(Job.title == "Senior AI Engineer - Founding Team").first()
        if not job:
            job = Job(
                recruiter_id=recruiter_id,
                title="Senior AI Engineer - Founding Team",
                description="""
Own the intelligence layer of Redrob's talent platform. Architect search, ranking, and recommendation systems that match candidates to roles across 100,000+ candidates.
Must have: Production experience with embeddings-based retrieval systems (SentenceTransformers, FAISS, Pinecone), strong Python, and evaluation frameworks (NDCG, MRR).
Experience required: 5-9 years in applied machine learning and backend engineering.
Location: Pune/Noida, India (Hybrid cadence) or Remote.
                """.strip(),
                department="AI & Search Intelligence",
                location="Pune / Noida, India",
                work_mode="hybrid",
                employment_type="full-time",
                minimum_experience=5.0,
                maximum_experience=9.0,
                education_requirement="B.Tech / M.Tech in Computer Science",
                target_shortlist_count=20,
                status="PUBLISHED"
            )
            db.add(job)
            db.commit()
            db.refresh(job)

            # Skills
            req_skills = ["python", "pytorch", "faiss", "llm", "rag", "fastapi", "machine learning"]
            pref_skills = ["docker", "kubernetes", "aws", "elasticsearch", "spark"]

            for s in req_skills:
                db.add(JobSkill(job_id=job.id, name=s, is_required=True))
            for s in pref_skills:
                db.add(JobSkill(job_id=job.id, name=s, is_required=False))

            # Initial Application
            cand_prof = db.query(CandidateProfile).filter(CandidateProfile.candidate_id == "CAND_DEMO01").first()
            if cand_prof:
                app = Application(
                    job_id=job.id,
                    candidate_id=cand_prof.candidate_id,
                    status="SHORTLISTED",
                    match_score=87.5,
                    notes="Excellent alignment on vector search and PyTorch experience."
                )
                db.add(app)
            db.commit()

        print("Database seeded successfully with demo users and benchmark job!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
