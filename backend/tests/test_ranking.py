from backend.app.ranking.scorer import MultiSignalScorer
from backend.app.ranking.eligibility import EligibilityFilter

def test_scorer_skills_matching():
    scorer = MultiSignalScorer()
    cand_skills = ["python", "pytorch", "fastapi", "docker"]
    req_skills = ["python", "pytorch", "faiss"]
    pref_skills = ["docker", "kubernetes"]

    req_score, pref_score, matched_req, matched_pref, missing = scorer.score_skills(cand_skills, req_skills, pref_skills)
    assert req_score == round((2/3) * 100.0, 2)
    assert pref_score == 50.0
    assert "python" in matched_req
    assert "faiss" in missing

def test_eligibility_filter_disqualifies_non_tech_roles():
    filter_engine = EligibilityFilter()
    job = {"title": "Senior AI Engineer", "minimum_experience": 5.0}

    # Non-tech candidate without AI skills
    cand_bad = {"current_title": "Customer Support Specialist", "years_of_experience": 8.0, "skills": ["customer care", "communication"]}
    eligible, reason = filter_engine.evaluate_candidate(cand_bad, job)
    assert eligible is False

    # Tech candidate
    cand_good = {"current_title": "Machine Learning Engineer", "years_of_experience": 6.0, "skills": ["python", "pytorch", "nlp"]}
    eligible, _ = filter_engine.evaluate_candidate(cand_good, job)
    assert eligible is True
