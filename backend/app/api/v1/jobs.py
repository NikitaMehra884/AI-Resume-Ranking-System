from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from backend.app.api.deps import get_db, require_recruiter, require_candidate, get_current_user
from backend.app.models.user import User
from backend.app.models.job import Job, JobSkill, RecruiterProfile
from backend.app.schemas.job import JobCreate, JobUpdate, JobOut, JDAnalysisResponse
from backend.app.parsing.jd_parser import JDParser

router = APIRouter(prefix="/jobs", tags=["Jobs"])
jd_parser = JDParser()

@router.get("/", response_model=List[JobOut])
def list_jobs(
    q: Optional[str] = None,
    work_mode: Optional[str] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Job).filter(Job.status == "PUBLISHED")
    if q:
        query = query.filter(Job.title.ilike(f"%{q}%") | Job.description.ilike(f"%{q}%"))
    if work_mode:
        query = query.filter(Job.work_mode == work_mode.lower())
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    return query.order_by(Job.created_at.desc()).all()

@router.get("/{job_id}", response_model=JobOut)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.post("/", response_model=JobOut)
def create_job(data: JobCreate, db: Session = Depends(get_db), current_user: User = Depends(require_recruiter)):
    recruiter = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == current_user.id).first()
    recruiter_id = recruiter.id if recruiter else None

    job = Job(
        recruiter_id=recruiter_id,
        title=data.title,
        description=data.description,
        department=data.department or "Engineering",
        location=data.location or "Remote",
        work_mode=data.work_mode or "hybrid",
        employment_type=data.employment_type or "full-time",
        minimum_experience=data.minimum_experience or 0.0,
        maximum_experience=data.maximum_experience or 20.0,
        education_requirement=data.education_requirement or "Bachelor",
        target_shortlist_count=data.target_shortlist_count or 20,
        status="PUBLISHED"
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Save Skills
    for skill in data.required_skills:
        db.add(JobSkill(job_id=job.id, name=skill.strip(), is_required=True))
    for skill in data.preferred_skills:
        db.add(JobSkill(job_id=job.id, name=skill.strip(), is_required=False))
    db.commit()
    db.refresh(job)
    return job

@router.put("/{job_id}", response_model=JobOut)
def update_job(job_id: int, data: JobUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_recruiter)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    for field, val in data.model_dump(exclude_unset=True).items():
        if field not in {"required_skills", "preferred_skills"} and val is not None:
            setattr(job, field, val)

    if data.required_skills is not None or data.preferred_skills is not None:
        db.query(JobSkill).filter(JobSkill.job_id == job.id).delete()
        if data.required_skills:
            for s in data.required_skills:
                db.add(JobSkill(job_id=job.id, name=s.strip(), is_required=True))
        if data.preferred_skills:
            for s in data.preferred_skills:
                db.add(JobSkill(job_id=job.id, name=s.strip(), is_required=False))

    db.commit()
    db.refresh(job)
    return job

@router.post("/analyze-jd", response_model=JDAnalysisResponse)
@router.post("/extract-skills", response_model=JDAnalysisResponse)
def analyze_jd(payload: dict):
    text = payload.get("text", "")
    title = payload.get("title", "Software Role")
    if not text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty")
    analysis = jd_parser.parse_jd(text, title=title)
    return analysis

@router.post("/{job_id}/apply")
def apply_to_job(job_id: int, payload: Optional[dict] = None, db: Session = Depends(get_db), current_user: User = Depends(require_candidate)):
    import json
    from backend.app.models.candidate import CandidateProfile, CandidateSkill
    from backend.app.models.application import Application
    from backend.app.ranking.scorer import MultiSignalScorer
    from backend.app.ranking.explainability import ExplainabilityService
    from backend.app.embeddings.semantic_service import SemanticService

    scorer = MultiSignalScorer()
    semantic_service = SemanticService()

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        profile = CandidateProfile(
            user_id=current_user.id,
            candidate_id=f"CAND_{current_user.id:07d}",
            full_name=current_user.email.split("@")[0].capitalize() or "Candidate",
            years_of_experience=3.0,
            completeness_score=85.0
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)

    # If applicant provided updated details during apply
    if payload:
        if payload.get("full_name"):
            profile.full_name = payload["full_name"]
        if payload.get("current_title"):
            profile.current_title = payload["current_title"]
        if payload.get("years_of_experience") is not None:
            try:
                profile.years_of_experience = float(payload["years_of_experience"])
            except (ValueError, TypeError):
                pass
        if payload.get("resume_text"):
            profile.raw_resume_text = payload["resume_text"]
        if payload.get("skills"):
            raw_s = payload["skills"]
            skill_names = [s.strip() for s in raw_s.split(",") if s.strip()] if isinstance(raw_s, str) else [str(s) for s in raw_s]
            if skill_names:
                db.query(CandidateSkill).filter(CandidateSkill.candidate_id == profile.candidate_id).delete()
                for s_name in skill_names:
                    db.add(CandidateSkill(candidate_id=profile.candidate_id, name=s_name.lower(), proficiency="advanced"))
        db.commit()
        db.refresh(profile)

    # Collect candidate skills
    cand_skills = [s.name.lower() for s in profile.skills] if profile.skills else []
    req_skills = [s.name.lower() for s in job.skills if s.is_required]
    pref_skills = [s.name.lower() for s in job.skills if not s.is_required]

    req_score, pref_score, matched_req, matched_pref, missing = scorer.score_skills(cand_skills, req_skills, pref_skills)
    exp_score = scorer.score_experience(profile.years_of_experience or 0.0, job.minimum_experience, job.maximum_experience)

    cand_text = profile.raw_resume_text or f"{profile.current_title} with skills {', '.join(cand_skills)}"
    c_emb = semantic_service.embedding(cand_text)
    j_emb = semantic_service.embedding(job.description)
    sem_score = round(semantic_service.similarity(c_emb, j_emb) * 100.0, 1)

    overall_score = round(0.40 * req_score + 0.30 * exp_score + 0.30 * sem_score, 1)
    overall_score = max(5.0, min(99.0, overall_score))

    rec = "Strong Fit" if overall_score >= 80 else ("Good Fit" if overall_score >= 65 else ("Moderate Fit" if overall_score >= 50 else "Potential Fit"))

    evidence = {
        "overall_score": overall_score,
        "skill_score": req_score,
        "experience_score": exp_score,
        "semantic_score": sem_score,
        "matched_skills": matched_req + matched_pref,
        "missing_skills": missing,
        "recommendation": rec,
        "why_ranked": f"Matches {len(matched_req)} required skills ({', '.join(matched_req[:4])}). Experience is {profile.years_of_experience} yrs for a {job.minimum_experience}+ yr role.",
        "cover_note": payload.get("cover_note", "") if payload else ""
    }

    existing = db.query(Application).filter(Application.job_id == job_id, Application.candidate_id == profile.candidate_id).first()
    if existing:
        existing.match_score = overall_score
        existing.evidence_json = json.dumps(evidence)
        if payload and payload.get("cover_note"):
            existing.notes = payload["cover_note"]
        db.commit()
        db.refresh(existing)
        return {"message": "Application updated successfully", "application_id": existing.id, "match_score": existing.match_score, "status": existing.status}

    app_rec = Application(
        job_id=job_id,
        candidate_id=profile.candidate_id,
        status="APPLIED",
        match_score=overall_score,
        evidence_json=json.dumps(evidence),
        notes=payload.get("cover_note", "") if payload else ""
    )
    db.add(app_rec)
    db.commit()
    db.refresh(app_rec)
    return {"message": "Application submitted successfully", "application_id": app_rec.id, "match_score": app_rec.match_score, "status": app_rec.status}

@router.post("/{job_id}/seed-demo-applicants")
def seed_demo_applicants(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_recruiter)):
    import json
    import uuid
    from backend.app.models.candidate import CandidateProfile, CandidateSkill, CandidateExperience, CandidateEducation
    from backend.app.models.application import Application

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    job_req_skills = [s.name.lower() for s in job.skills if s.is_required]
    
    samples = [
        {
            "name": "Arjun Sharma",
            "email": "arjun.sharma@example.com",
            "title": "Lead Software Architect",
            "company": "Tech Innovations",
            "yoe": max(5.0, job.minimum_experience + 2.0),
            "score": 93.5,
            "status": "SHORTLISTED",
            "skills": job_req_skills + ["docker", "system design", "aws"],
            "why": f"Superb match: Possesses all required skills ({', '.join(job_req_skills[:3])}) with senior leadership experience."
        },
        {
            "name": "Pooja Patel",
            "email": "pooja.patel@example.com",
            "title": "Senior Engineer",
            "company": "NextGen Systems",
            "yoe": max(3.5, job.minimum_experience + 0.5),
            "score": 82.0,
            "status": "INTERVIEW",
            "skills": job_req_skills[:3] + ["fastapi", "postgresql", "git"],
            "why": f"Strong alignment with {', '.join(job_req_skills[:2])}. Solid project experience and quick ramp-up potential."
        },
        {
            "name": "Devendra Kumar",
            "email": "devendra.k@example.com",
            "title": "Mid Software Developer",
            "company": "CloudNative Labs",
            "yoe": max(2.0, job.minimum_experience - 1.0),
            "score": 67.5,
            "status": "APPLIED",
            "skills": job_req_skills[:2] + ["python", "sql", "linux"],
            "why": "Good foundational developer. Slightly below target experience window, but strong core competencies."
        },
        {
            "name": "Ritu Singhania",
            "email": "ritu.s@example.com",
            "title": "Junior Associate Engineer",
            "company": "StartUp Hub",
            "yoe": 1.0,
            "score": 48.0,
            "status": "APPLIED",
            "skills": ["python", "javascript", "html", "css"],
            "why": f"Entry-level profile with limited overlap with senior role requirements."
        }
    ]

    added = 0
    for s in samples:
        cid = f"DEMO_{uuid.uuid4().hex[:6].upper()}"
        prof = CandidateProfile(
            candidate_id=cid,
            full_name=s["name"],
            headline=f"{s['title']} at {s['company']}",
            years_of_experience=s["yoe"],
            current_title=s["title"],
            current_company=s["company"],
            location=job.location,
            completeness_score=95.0,
            raw_resume_text=f"{s['name']} is a {s['title']} with {s['yoe']} years of experience in {', '.join(s['skills'])}."
        )
        db.add(prof)
        db.commit()
        db.refresh(prof)

        for sk in s["skills"]:
            db.add(CandidateSkill(candidate_id=cid, name=sk, proficiency="advanced"))

        ev = {
            "overall_score": s["score"],
            "matched_skills": [sk for sk in s["skills"] if sk in job_req_skills],
            "missing_skills": [sk for sk in job_req_skills if sk not in s["skills"]],
            "recommendation": "Strong Fit" if s["score"] >= 80 else ("Good Fit" if s["score"] >= 65 else "Review"),
            "why_ranked": s["why"]
        }

        app = Application(
            job_id=job.id,
            candidate_id=cid,
            status=s["status"],
            match_score=s["score"],
            evidence_json=json.dumps(ev)
        )
        db.add(app)
        added += 1

    db.commit()
    return {"message": f"Successfully added {added} realistic applicants to job #{job.id}", "job_id": job.id, "applicant_count": job.applicant_count}
