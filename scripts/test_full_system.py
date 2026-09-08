import os
import sys
import json
from pathlib import Path

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.database import SessionLocal, engine
from backend.app.models.user import User
from backend.app.models.job import Job
from backend.app.models.candidate import CandidateProfile
from backend.app.models.application import Application

def run_tests():
    print("=" * 80)
    print("AI RECRUITMENT INTELLIGENCE PLATFORM — END-TO-END SYSTEM VERIFICATION")
    print("=" * 80)

    passed_tests = 0
    total_tests = 0

    def assert_test(name: str, condition: bool, details: str = ""):
        nonlocal passed_tests, total_tests
        total_tests += 1
        if condition:
            passed_tests += 1
            print(f"  [PASS] {name} {details and '(' + details + ')'}")
        else:
            print(f"  [FAIL] {name} {details and '(' + details + ')'}")
            raise AssertionError(f"Test failed: {name} - {details}")

    client = TestClient(app)

    # -------------------------------------------------------------
    # 1. Core & Health Checks
    # -------------------------------------------------------------
    print("\n--- 1. Testing Core & Health Endpoints ---")
    res = client.get("/health")
    assert_test("GET /health status is 200", res.status_code == 200)
    assert_test("Health status is healthy", res.json().get("status") == "healthy")

    res = client.get("/")
    assert_test("GET / root returns API info", res.status_code == 200 and "status" in res.json())

    # -------------------------------------------------------------
    # 2. Authentication & Authorization
    # -------------------------------------------------------------
    print("\n--- 2. Testing Authentication & Security ---")
    # Recruiter Login
    res = client.post("/api/v1/auth/login", json={
        "email": "recruiter@platform.ai",
        "password": "password123"
    })
    assert_test("Recruiter Login 200 OK", res.status_code == 200)
    recruiter_data = res.json()
    recruiter_token = recruiter_data.get("access_token")
    assert_test("Recruiter Token Generated", bool(recruiter_token))
    assert_test("Recruiter Role Verified", recruiter_data.get("role") == "RECRUITER")
    recruiter_headers = {"Authorization": f"Bearer {recruiter_token}"}

    # Candidate Login
    res = client.post("/api/v1/auth/login", json={
        "email": "candidate@platform.ai",
        "password": "password123"
    })
    assert_test("Candidate Login 200 OK", res.status_code == 200)
    candidate_data = res.json()
    candidate_token = candidate_data.get("access_token")
    assert_test("Candidate Token Generated", bool(candidate_token))
    assert_test("Candidate Role Verified", candidate_data.get("role") == "CANDIDATE")
    candidate_headers = {"Authorization": f"Bearer {candidate_token}"}

    # Invalid Login Test
    res = client.post("/api/v1/auth/login", json={
        "email": "candidate@platform.ai",
        "password": "wrongpassword"
    })
    assert_test("Invalid password rejected with 401", res.status_code == 401)

    # New User Registration
    test_email = f"testuser_{os.getpid()}@platform.ai"
    res = client.post("/api/v1/auth/register", json={
        "email": test_email,
        "password": "testpassword123",
        "role": "CANDIDATE",
        "full_name": "Verification Bot"
    })
    assert_test("Candidate Registration 200/201 OK", res.status_code in [200, 201])
    assert_test("Registered user returned", res.json().get("email") == test_email)

    # -------------------------------------------------------------
    # 3. Job Management & AI JD Parsing
    # -------------------------------------------------------------
    print("\n--- 3. Testing Job Management & AI JD Parsing ---")
    res = client.get("/api/v1/jobs/")
    assert_test("GET /api/v1/jobs/ returns 200", res.status_code == 200)
    jobs_list = res.json()
    assert_test("Job listings exist in database", len(jobs_list) > 0, f"Found {len(jobs_list)} jobs")
    job_id = jobs_list[0]["id"]

    # AI JD Extract Skills
    res = client.post("/api/v1/jobs/extract-skills", json={
        "title": "Lead Computer Vision Engineer",
        "text": "Seeking a Lead Computer Vision Engineer with 5+ years experience. Mandatory: Python, PyTorch, OpenCV, CUDA. Preferred: TensorRT, Docker, AWS."
    })
    assert_test("POST /api/v1/jobs/extract-skills 200 OK", res.status_code == 200)
    jd_parsed = res.json()
    assert_test("Extracted required skills correctly", "python" in [s.lower() for s in jd_parsed.get("required_skills", [])])
    assert_test("Extracted preferred skills correctly", any("docker" in s.lower() or "aws" in s.lower() for s in jd_parsed.get("preferred_skills", [])))

    # Create New Job (Recruiter Authorized)
    res = client.post("/api/v1/jobs/", json={
        "title": "AI Research Scientist - Verification",
        "department": "AI / Research",
        "location": "Bengaluru / Remote",
        "work_mode": "remote",
        "employment_type": "Full-time",
        "minimum_experience": 4.0,
        "maximum_experience": 8.0,
        "education_requirement": "Bachelor or Master in CS",
        "target_shortlist_count": 10,
        "description": "Looking for an AI Research Scientist experienced in NLP, PyTorch, FAISS, Transformers, and scalable inference.",
        "skills": [
            {"name": "Python", "is_required": True},
            {"name": "PyTorch", "is_required": True},
            {"name": "FAISS", "is_required": True},
            {"name": "Transformers", "is_required": False}
        ]
    }, headers=recruiter_headers)
    assert_test("Create Job 200/201 OK", res.status_code in [200, 201])
    created_job = res.json()
    created_job_id = created_job["id"]
    assert_test("Created Job ID exists", created_job_id > 0)

    # -------------------------------------------------------------
    # 4. Candidate Workflows & Resume Parsing
    # -------------------------------------------------------------
    print("\n--- 4. Testing Candidate Workflows & Parsing ---")
    res = client.get("/api/v1/candidates/me", headers=candidate_headers)
    assert_test("GET /api/v1/candidates/me 200 OK", res.status_code == 200)
    profile = res.json()
    assert_test("Profile candidate_id present", bool(profile.get("candidate_id")))

    # Raw Text Resume Parsing
    sample_cv = """
    Alex Johnson
    alex.johnson@example.com | (555) 234-5678 | San Francisco, CA
    
    Professional Summary:
    Senior Machine Learning Engineer with 6 years experience architecting deep learning pipelines.
    Expertise in Python, PyTorch, FAISS, FastAPI, Docker, and Kubernetes.
    
    Work Experience:
    Senior ML Engineer at TechCorp (2021 - Present)
    - Built semantic search engine serving 20M queries daily using FAISS and BERT embeddings.
    
    Software Engineer at DataSoft (2018 - 2021)
    - Developed backend REST microservices in FastAPI and PostgreSQL.
    
    Education:
    B.S. in Computer Science, University of California, Berkeley (2018)
    """
    res = client.post("/api/v1/candidates/parse-resume-text", json={"text": sample_cv}, headers=candidate_headers)
    assert_test("POST /api/v1/candidates/parse-resume-text 200 OK", res.status_code == 200)
    parsed_cv = res.json()
    assert_test("Parsed extracted skills list", len(parsed_cv.get("skills", [])) > 0, f"Skills: {parsed_cv.get('skills')[:4]}")
    assert_test("Parsed contact info", parsed_cv.get("contact_info", {}).get("email") == "alex.johnson@example.com")
    assert_test("Parsed years of experience", parsed_cv.get("years_of_experience", 0) >= 5)

    # Fit Analysis Endpoint
    res = client.post("/api/v1/candidates/match-analysis", json={
        "job_id": job_id,
        "job_description": "We need an AI Engineer skilled in Python, PyTorch, FAISS, Machine Learning, and FastAPI."
    }, headers=candidate_headers)
    assert_test("POST /api/v1/candidates/match-analysis 200 OK", res.status_code == 200)
    analysis = res.json()
    assert_test("Overall match score in [0, 100]", 0 <= analysis.get("overall_match_score", -1) <= 100)
    assert_test("Recommendations provided", len(analysis.get("recommendations", [])) > 0)

    # Apply to Job
    res = client.post(f"/api/v1/jobs/{created_job_id}/apply", headers=candidate_headers)
    assert_test("POST apply to job 200 OK", res.status_code in [200, 201])

    # View Applications
    res = client.get("/api/v1/candidates/my-applications", headers=candidate_headers)
    assert_test("GET /api/v1/candidates/my-applications 200 OK", res.status_code == 200)
    apps = res.json()
    assert_test("Application present in candidate tracker", any(a["job_id"] == created_job_id for a in apps))

    # -------------------------------------------------------------
    # 5. Recruiter 4-Stage Hybrid Screening & Ranking
    # -------------------------------------------------------------
    print("\n--- 5. Testing Recruiter 4-Stage Screening & AI Features ---")
    res = client.post("/api/v1/screening/rank", json={
        "job_id": created_job_id,
        "top_k": 5
    }, headers=recruiter_headers)
    assert_test("POST /api/v1/screening/rank 200 OK", res.status_code == 200)
    screening = res.json()
    candidates = screening.get("candidates", [])
    assert_test("Returned Top-K candidates", len(candidates) == 5, f"Returned {len(candidates)} candidates")
    
    top_cand = candidates[0]
    assert_test("Candidate Rank #1 assigned", top_cand.get("rank") == 1)
    assert_test("Final score normalized in [0, 100]", 0 <= top_cand.get("final_score", -1) <= 100)
    assert_test("Semantic score normalized in [0, 100]", 0 <= top_cand.get("semantic_score", -1) <= 100)
    assert_test("Keyword BM25 score normalized in [0, 100]", 0 <= top_cand.get("keyword_score", -1) <= 100)
    assert_test("Grounded explanation present", bool(top_cand.get("explanation")), "Why ranked evidence generated")

    # Side-by-Side Comparison
    if len(candidates) >= 2:
        res = client.post("/api/v1/screening/compare", json={
            "job_id": created_job_id,
            "candidate_ids": [candidates[0]["candidate_id"], candidates[1]["candidate_id"]]
        }, headers=recruiter_headers)
        assert_test("POST /api/v1/screening/compare 200 OK", res.status_code == 200)
        comp = res.json()
        assert_test("Comparison candidates count", len(comp.get("candidates", [])) == 2)
        assert_test("AI comparison synthesis present", bool(comp.get("ai_comparison_summary") or comp.get("recommendation")))

    # AI Interview Questions Generator
    res = client.post("/api/v1/screening/interview-questions", json={
        "job_id": created_job_id,
        "candidate_id": top_cand["candidate_id"]
    }, headers=recruiter_headers)
    assert_test("POST /api/v1/screening/interview-questions 200 OK", res.status_code == 200)
    q_data = res.json()
    assert_test("Interview questions returned", bool(q_data.get("questions") or q_data))

    # Pipeline Stages
    res = client.get(f"/api/v1/screening/pipeline?job_id={created_job_id}", headers=recruiter_headers)
    assert_test("GET /api/v1/screening/pipeline 200 OK", res.status_code == 200)

    # -------------------------------------------------------------
    # 6. Analytics & Auditing
    # -------------------------------------------------------------
    print("\n--- 6. Testing Analytics & Fairness Auditing ---")
    res = client.get("/api/v1/analytics/dashboard", headers=recruiter_headers)
    assert_test("GET /api/v1/analytics/dashboard 200 OK", res.status_code == 200)
    analytics = res.json()
    assert_test("Score distribution metrics present", "score_distribution" in analytics or "top_skills" in analytics)

    # -------------------------------------------------------------
    # 7. Frontend Build & Static Asset Verification
    # -------------------------------------------------------------
    print("\n--- 7. Testing Frontend Build & Artifacts ---")
    dist_dir = ROOT / "frontend" / "dist"
    index_html = dist_dir / "index.html"
    assert_test("Frontend dist directory exists", dist_dir.exists())
    assert_test("Frontend index.html exists", index_html.exists())

    with open(index_html, "r", encoding="utf-8") as f:
        html_content = f.read()
    assert_test("index.html contains root element", '<div id="root">' in html_content)
    assert_test("index.html contains bundled javascript asset", '<script type="module"' in html_content)

    assets_dir = dist_dir / "assets"
    js_assets = list(assets_dir.glob("*.js"))
    css_assets = list(assets_dir.glob("*.css"))
    assert_test("Bundled JavaScript assets found", len(js_assets) > 0, f"Found {len(js_assets)} JS files")
    assert_test("Bundled CSS assets found", len(css_assets) > 0, f"Found {len(css_assets)} CSS files")

    print("\n" + "=" * 80)
    print(f"VERIFICATION COMPLETE: {passed_tests}/{total_tests} Tests Passed (100% SUCCESS)")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
