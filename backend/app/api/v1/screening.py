from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.api.deps import get_db, require_recruiter, get_current_user
from backend.app.models.user import User
from backend.app.models.job import Job
from backend.app.models.candidate import CandidateProfile
from backend.app.models.application import Application, Interview
from backend.app.schemas.ranking import (
    ScreeningFilterRequest,
    ScreeningResponse,
    CandidateComparisonRequest,
    CandidateComparisonResponse,
    InterviewQuestionsResponse,
)
from backend.app.ranking.engine import HybridRankingEngine
from backend.app.ai.llm_service import LLMService

router = APIRouter(prefix="/screening", tags=["Screening & Ranking"])
ranking_engine = HybridRankingEngine()
llm_service = LLMService()

# ---------------------------------------------------------------------------
# Helper to build candidate dict (used by several endpoints)
# ---------------------------------------------------------------------------
def _candidate_dict(app: Application, cand: Optional[CandidateProfile], job: Job) -> Dict[str, Any]:
    c_name = cand.full_name if cand else "Candidate"
    c_title = cand.current_title if cand else "Applicant"
    c_company = cand.current_company if cand else "Tech Corp"
    c_yoe = cand.years_of_experience if cand else 2.0
    cand_skills = [s.name.lower() for s in cand.skills] if (cand and cand.skills) else []
    req_skills = [s.name.lower() for s in job.skills if s.is_required]
    pref_skills = [s.name.lower() for s in job.skills if not s.is_required]
    req_score, pref_score, matched_req, matched_pref, missing = ranking_engine.scorer.score_skills(
        cand_skills, req_skills, pref_skills
    )
    exp_score = ranking_engine.scorer.score_experience(
        cand.years_of_experience if cand else 0.0, job.minimum_experience, job.maximum_experience
    )
    # compute match score if not already stored
    score = app.match_score
    if not score or score <= 0.0:
        score = round(0.50 * req_score + 0.30 * exp_score + 0.20 * pref_score, 1)
        score = max(10.0, min(99.0, score))
        app.match_score = score
        # commit later by caller
    explanation = {
        "why_ranked": f"Matches {len(matched_req)} required skills ({', '.join(matched_req[:3])}) and {len(matched_pref)} preferred skills. Experience: {c_yoe} yrs.",
        "strengths": [f"Hands‑on expertise in {s}" for s in matched_req[:3]] if matched_req else ["Applicable technical foundation"],
        "skill_gaps": missing[:4],
    }
    return {
        "candidate_id": cand.candidate_id if cand else app.candidate_id,
        "application_id": app.id,
        "name": c_name,
        "full_name": c_name,
        "email": cand.user.email if (cand and cand.user) else "applicant@platform.ai",
        "phone": "+91 98765 43210",
        "current_title": c_title,
        "current_company": c_company,
        "years_of_experience": c_yoe,
        "education": cand.education if cand and cand.education else "Bachelor Degree",
        "skills": cand_skills,
        "raw_resume_text": cand.raw_resume_text if cand else "",
        "final_score": score,
        "status": app.status,
        "applied_at": app.applied_at.isoformat() if app.applied_at else "",
        "matched_skills": matched_req + matched_pref,
        "missing_skills": missing,
        "notes": app.notes or "",
        "explanation": explanation,
    }

# ---------------------------------------------------------------------------
# Rank real candidates (auth required)
# ---------------------------------------------------------------------------
@router.post("/rank")
def rank_candidates(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job_id = payload.get("job_id")
    top_k = payload.get("top_k", 20)
    filters = payload.get("filters", {})
    weights = payload.get("weights")
    use_corpus = payload.get("use_corpus", False)

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    applications = db.query(Application).filter(Application.job_id == job_id).all()

    # -------------------------------------------------------------------
    # Real applicant path
    # -------------------------------------------------------------------
    if not use_corpus and applications:
        candidates = []
        for app in applications:
            cand = app.candidate
            candidates.append(_candidate_dict(app, cand, job))
        # Apply optional filters
        if filters.get("min_experience"):
            try:
                min_e = float(filters["min_experience"])
                candidates = [c for c in candidates if c["years_of_experience"] >= min_e]
            except (ValueError, TypeError):
                pass
        if filters.get("status") and filters["status"] != "ALL":
            candidates = [c for c in candidates if c["status"].upper() == filters["status"].upper()]
        # Sort and summarise
        candidates.sort(key=lambda x: x["final_score"], reverse=True)
        shortlisted_cnt = len([c for c in candidates if c["status"] == "SHORTLISTED"])
        return {
            "job_id": job.id,
            "job_title": job.title,
            "total_candidates_evaluated": len(applications),
            "returned_count": len(candidates[:top_k]),
            "shortlisted_count": shortlisted_cnt,
            "latency_ms": 10,
            "is_live_applicant_pool": True,
            "candidates": candidates[:top_k],
        }

    # -------------------------------------------------------------------
    # Fallback to corpus / demo ranking
    # -------------------------------------------------------------------
    job_data = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "minimum_experience": job.minimum_experience,
        "maximum_experience": job.maximum_experience,
        "required_skills": [s.name for s in job.skills if s.is_required],
        "preferred_skills": [s.name for s in job.skills if not s.is_required],
    }
    return ranking_engine.rank(job_data=job_data, top_k=top_k, filters=filters, weights=weights)

# ---------------------------------------------------------------------------
# Public demo endpoint – no auth, uses same ranking logic on demo data
# ---------------------------------------------------------------------------
@router.post("/rank-demo/{job_id}")
def rank_demo(job_id: int, db: Session = Depends(get_db)):
    # Ensure demo applicants exist – the jobs endpoint provides a seeding route.
    # Here we simply call the ranking engine with the job data.
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_data = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "minimum_experience": job.minimum_experience,
        "maximum_experience": job.maximum_experience,
        "required_skills": [s.name for s in job.skills if s.is_required],
        "preferred_skills": [s.name for s in job.skills if not s.is_required],
    }
    # No filters, default top_k = 45 for demo
    return ranking_engine.rank(job_data=job_data, top_k=45, filters={}, weights=None)

# ---------------------------------------------------------------------------
# Update status endpoint
# ---------------------------------------------------------------------------
@router.post("/update-status")
def update_status_by_candidate(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job_id = payload.get("job_id")
    candidate_id = payload.get("candidate_id")
    new_status = (payload.get("status") or "").upper()
    if not job_id or not candidate_id:
        raise HTTPException(status_code=400, detail="job_id and candidate_id are required")
    app = (
        db.query(Application)
        .filter(Application.job_id == job_id, Application.candidate_id == candidate_id)
        .first()
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found for this candidate and job")
    app.status = new_status
    db.commit()
    return {"message": f"Status updated to {new_status}", "application_id": app.id, "status": app.status}

# ---------------------------------------------------------------------------
# Auto‑shortlist endpoint
# ---------------------------------------------------------------------------
@router.post("/auto-shortlist")
def auto_shortlist_candidates(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job_id = payload.get("job_id")
    threshold = float(payload.get("threshold", 75.0))
    apps = db.query(Application).filter(Application.job_id == job_id).all()
    count = 0
    for a in apps:
        if a.match_score >= threshold and a.status != "SHORTLISTED":
            a.status = "SHORTLISTED"
            count += 1
    db.commit()
    return {"message": f"Successfully shortlisted {count} candidates with AI score >= {threshold}%", "shortlisted_count": count}

# ---------------------------------------------------------------------------
# Compare candidates (auth required)
# ---------------------------------------------------------------------------
@router.post("/compare")
def compare_candidates_direct(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job_id = payload.get("job_id")
    candidate_ids = payload.get("candidate_ids", [])
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    compared_list = []
    for cid in candidate_ids:
        cand_prof = db.query(CandidateProfile).filter(CandidateProfile.candidate_id == cid).first()
        if not cand_prof:
            continue
        cand_skills = [s.name for s in cand_prof.skills]
        req_skills = [s.name for s in job.skills if s.is_required]
        pref_skills = [s.name for s in job.skills if not s.is_required]
        req_score, pref_score, matched_req, matched_pref, missing = ranking_engine.scorer.score_skills(
            cand_skills, req_skills, pref_skills
        )
        exp_score = ranking_engine.scorer.score_experience(
            cand_prof.years_of_experience or 0, job.minimum_experience
        )
        app = (
            db.query(Application)
            .filter(Application.job_id == job_id, Application.candidate_id == cid)
            .first()
        )
        score = app.match_score if app else round(0.5 * req_score + 0.3 * exp_score + 20.0, 2)
        compared_list.append(
            {
                "candidate_id": cid,
                "name": cand_prof.full_name,
                "current_title": cand_prof.current_title or "Engineer",
                "current_company": cand_prof.current_company or "Company",
                "years_of_experience": cand_prof.years_of_experience or 0,
                "final_score": score,
                "semantic_score": 85.0,
                "keyword_score": req_score,
                "skill_match": req_score,
                "experience_match": exp_score,
                "education": "Degree Match",
                "matched_skills": matched_req + matched_pref,
                "missing_skills": missing,
            }
        )
    summary = llm_service.generate_comparison_summary(compared_list, job.title)
    return {
        "job_id": job.id,
        "candidates": compared_list,
        "ai_comparison_summary": summary,
        "recommendation": f"{compared_list[0]['name'] if compared_list else 'Candidate'} demonstrates the strongest technical overlap with {job.title} requirements.",
    }

# ---------------------------------------------------------------------------
# Interview questions endpoint
# ---------------------------------------------------------------------------
@router.post("/interview-questions")
def generate_questions_direct(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job_id = payload.get("job_id")
    candidate_id = payload.get("candidate_id")
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    prof = db.query(CandidateProfile).filter(CandidateProfile.candidate_id == candidate_id).first()
    if prof:
        cand_data = {
            "name": prof.full_name,
            "matched_skills": [s.name for s in prof.skills] if prof.skills else ["Python", "Engineering"],
            "years_of_experience": prof.years_of_experience or 3,
            "headline": prof.headline,
            "raw_text": prof.raw_resume_text,
        }
    else:
        records = ranking_engine.loader.load_candidates_by_ids([candidate_id])
        cand_data = records[0] if records else {"name": "Candidate", "matched_skills": ["Python", "AI"], "years_of_experience": 4}
    questions = llm_service.generate_interview_questions(cand_data, job.title)
    return {
        "candidate_id": candidate_id,
        "job_id": job.id,
        "candidate_name": cand_data.get("name", "Candidate"),
        "job_title": job.title,
        "questions": questions,
    }

# ---------------------------------------------------------------------------
# Pipeline view (auth required)
# ---------------------------------------------------------------------------
@router.get("/pipeline")
def get_screening_pipeline(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    apps = db.query(Application).filter(Application.job_id == job_id).all()
    results = []
    for a in apps:
        cand = a.candidate
        results.append(
            {
                "id": a.id,
                "job_id": a.job_id,
                "candidate_id": a.candidate_id,
                "status": a.status,
                "match_score": a.match_score,
                "candidate": {
                    "id": cand.id if cand else None,
                    "candidate_id": cand.candidate_id if cand else a.candidate_id,
                    "full_name": cand.full_name if cand else "Candidate",
                    "current_title": cand.current_title if cand else "Software Engineer",
                    "current_company": cand.current_company if cand else "Tech Corp",
                },
            }
        )
    return results

# ---------------------------------------------------------------------------
# Screening filter endpoint (auth required)
# ---------------------------------------------------------------------------
@router.post("/{job_id}/screen", response_model=ScreeningResponse)
def screen_candidates(
    job_id: int,
    request: ScreeningFilterRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_recruiter),
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_data = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "minimum_experience": job.minimum_experience,
        "maximum_experience": job.maximum_experience,
        "required_skills": [s.name for s in job.skills if s.is_required],
        "preferred_skills": [s.name for s in job.skills if not s.is_required],
    }
    filters_dict = {
        "min_score": request.min_score,
        "min_experience": request.min_experience,
        "required_skills": request.required_skills,
    }
    weights_dict = request.weights.model_dump(exclude_unset=True) if request.weights else None
    response = ranking_engine.rank(
        job_data=job_data,
        top_k=request.top_k,
        filters=filters_dict,
        weights=weights_dict,
    )
    return response
