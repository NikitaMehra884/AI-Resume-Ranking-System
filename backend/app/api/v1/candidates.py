from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db, require_candidate, get_current_user
from backend.app.models.user import User
from backend.app.models.candidate import CandidateProfile, CandidateSkill, CandidateExperience, CandidateEducation
from backend.app.models.job import Job
from backend.app.models.application import Application
from backend.app.schemas.candidate import CandidateProfileOut, CandidateProfileUpdate
from backend.app.schemas.ranking import CandidateMatchReport
from backend.app.parsing.resume_parser import ResumeParser
from backend.app.ranking.scorer import MultiSignalScorer
from backend.app.ranking.explainability import ExplainabilityService
from backend.app.embeddings.semantic_service import SemanticService

router = APIRouter(prefix="/candidates", tags=["Candidates"])
resume_parser = ResumeParser()
scorer = MultiSignalScorer()
explain_service = ExplainabilityService()
semantic_service = SemanticService()

@router.get("/profile", response_model=CandidateProfileOut)
@router.get("/me", response_model=CandidateProfileOut)
def get_profile(db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(
            user_id=current_user.id,
            candidate_id=f"CAND_{current_user.id:07d}",
            full_name="Verified Candidate",
            headline="Software Engineer",
            years_of_experience=3.0,
            completeness_score=75.0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("/profile", response_model=CandidateProfileOut)
@router.put("/me", response_model=CandidateProfileOut)
def update_profile(data: CandidateProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(
            user_id=current_user.id,
            candidate_id=f"CAND_{current_user.id:07d}",
            full_name="Verified Candidate",
            headline="Software Engineer",
            years_of_experience=3.0,
            completeness_score=75.0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    for field, val in data.model_dump(exclude_unset=True).items():
        if field not in {"skills", "career_history", "education"} and val is not None:
            setattr(profile, field, val)

    if data.skills is not None:
        db.query(CandidateSkill).filter(CandidateSkill.candidate_id == profile.candidate_id).delete()
        for s in data.skills:
            db.add(CandidateSkill(candidate_id=profile.candidate_id, name=s.name, proficiency=s.proficiency or "intermediate"))

    if data.career_history is not None:
        db.query(CandidateExperience).filter(CandidateExperience.candidate_id == profile.candidate_id).delete()
        for exp in data.career_history:
            db.add(CandidateExperience(
                candidate_id=profile.candidate_id,
                company=exp.company,
                title=exp.title,
                duration_months=exp.duration_months or 0,
                description=exp.description or ""
            ))

    if data.education is not None:
        db.query(CandidateEducation).filter(CandidateEducation.candidate_id == profile.candidate_id).delete()
        for edu in data.education:
            db.add(CandidateEducation(
                candidate_id=profile.candidate_id,
                institution=edu.institution,
                degree=edu.degree or "",
                field_of_study=edu.field_of_study or ""
            ))

    db.commit()
    db.refresh(profile)
    return profile

@router.post("/resume/upload", response_model=CandidateProfileOut)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    contents = await file.read()
    filename = (file.filename or "").lower()

    if filename.endswith(".pdf"):
        text = resume_parser.extract_text_from_pdf(contents)
    elif filename.endswith(".docx"):
        text = resume_parser.extract_text_from_docx(contents)
    else:
        text = contents.decode("utf-8", errors="ignore")

    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from resume")

    parsed = resume_parser.parse_resume(text, full_name=current_user.email.split("@")[0].capitalize())

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(
            user_id=current_user.id,
            candidate_id=f"CAND_{uuid.uuid4().hex[:7].upper()}",
            full_name=parsed["full_name"]
        )
        db.add(profile)

    profile.full_name = parsed["full_name"]
    profile.raw_resume_text = text
    profile.years_of_experience = parsed["years_of_experience"]
    profile.current_title = parsed["current_title"]
    profile.completeness_score = 95.0

    # Replace skills
    db.query(CandidateSkill).filter(CandidateSkill.candidate_id == profile.candidate_id).delete()
    for s in parsed["skills"]:
        db.add(CandidateSkill(candidate_id=profile.candidate_id, name=s["name"], proficiency=s["proficiency"]))

    db.commit()
    db.refresh(profile)
    return profile

@router.post("/match/{job_id}", response_model=CandidateMatchReport)
def analyze_my_match(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate profile not found")
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    cand_skills = [s.name for s in profile.skills]
    req_skills = [s.name for s in job.skills if s.is_required]
    pref_skills = [s.name for s in job.skills if not s.is_required]

    req_score, pref_score, matched_req, matched_pref, missing = scorer.score_skills(cand_skills, req_skills, pref_skills)
    exp_score = scorer.score_experience(profile.years_of_experience, job.minimum_experience, job.maximum_experience)

    # Compute Semantic Match
    c_emb = semantic_service.embedding(profile.raw_resume_text or profile.summary or f"{profile.current_title} with skills {', '.join(cand_skills)}")
    j_emb = semantic_service.embedding(job.description)
    sem_score = round(semantic_service.similarity(c_emb, j_emb) * 100.0, 2)

    final_score = round(0.35 * req_score + 0.15 * pref_score + 0.25 * sem_score + 0.25 * exp_score, 2)

    candidate_result = {
        "candidate_id": profile.candidate_id,
        "final_score": final_score,
        "semantic_score": sem_score,
        "keyword_score": req_score,
        "skill_score": req_score,
        "experience_score": exp_score,
        "education_score": 85.0,
        "availability_score": 90.0,
        "matched_skills": matched_req + matched_pref,
        "missing_skills": missing,
        "years_of_experience": profile.years_of_experience
    }

    job_data = {
        "id": job.id,
        "title": job.title,
        "minimum_experience": job.minimum_experience
    }
    return explain_service.generate_candidate_report(candidate_result, job_data)

@router.post("/parse-resume-text")
def parse_resume_text(payload: dict):
    text = payload.get("text", "")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty")
    return resume_parser.parse_resume(text)

@router.post("/parse-resume")
async def parse_resume_file(file: UploadFile = File(...)):
    contents = await file.read()
    filename = (file.filename or "").lower()
    if filename.endswith(".pdf"):
        text = resume_parser.extract_text_from_pdf(contents)
    elif filename.endswith(".docx"):
        text = resume_parser.extract_text_from_docx(contents)
    else:
        text = contents.decode("utf-8", errors="ignore")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from resume")
    return resume_parser.parse_resume(text)

@router.post("/match-analysis")
def candidate_match_analysis(payload: dict, db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    job_id = payload.get("job_id")
    custom_desc = payload.get("job_description", "")
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(user_id=current_user.id, candidate_id=f"CAND_{current_user.id:07d}", full_name="Candidate")

    cand_skills = [s.name for s in profile.skills] if profile.skills else ["python", "machine learning", "pytorch"]

    if job_id:
        job = db.query(Job).filter(Job.id == job_id).first()
        jd_text = job.description if job else custom_desc
        req_skills = [s.name for s in job.skills if s.is_required] if job else []
        pref_skills = [s.name for s in job.skills if not s.is_required] if job else []
        min_exp = job.minimum_experience if job else 2.0
    else:
        from backend.app.parsing.jd_parser import JDParser
        jd_p = JDParser()
        parsed_j = jd_p.parse_jd(custom_desc)
        jd_text = custom_desc
        req_skills = parsed_j.get("required_skills", [])
        pref_skills = parsed_j.get("preferred_skills", [])
        min_exp = parsed_j.get("minimum_experience", 2.0)

    req_score, pref_score, matched_req, matched_pref, missing = scorer.score_skills(cand_skills, req_skills, pref_skills)
    exp_score = scorer.score_experience(profile.years_of_experience or 3.0, min_exp, min_exp + 4)

    c_emb = semantic_service.embedding(profile.raw_resume_text or " ".join(cand_skills))
    j_emb = semantic_service.embedding(jd_text)
    sem_score = round(semantic_service.similarity(c_emb, j_emb) * 100.0, 2)
    overall = round(0.35 * req_score + 0.15 * pref_score + 0.25 * sem_score + 0.25 * exp_score, 2)

    recs = []
    if missing:
        recs.append(f"Consider acquiring or highlighting experience in: {', '.join(missing[:3])}.")
    if exp_score < 70:
        recs.append("Emphasize high-impact leadership or system-level accomplishments to compensate for experience window.")
    if not recs:
        recs.append("Your skills and background are strongly aligned with this role.")

    return {
        "overall_match_score": overall,
        "semantic_score": sem_score,
        "required_skill_score": req_score,
        "experience_score": exp_score,
        "matched_skills": matched_req + matched_pref,
        "missing_skills": missing,
        "recommendations": recs
    }

@router.get("/applications")
@router.get("/my-applications")
def get_my_applications(db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        return []
    apps = db.query(Application).filter(Application.candidate_id == profile.candidate_id).all()
    results = []
    for a in apps:
        results.append({
            "id": a.id,
            "job_id": a.job_id,
            "job": {
                "id": a.job.id if a.job else a.job_id,
                "title": a.job.title if a.job else "Job Position",
                "department": a.job.department if a.job else "Engineering",
                "location": a.job.location if a.job else "Remote"
            },
            "status": a.status,
            "match_score": a.match_score,
            "created_at": a.created_at.isoformat() if a.created_at else "2026-09-07T00:00:00"
        })
    return results
