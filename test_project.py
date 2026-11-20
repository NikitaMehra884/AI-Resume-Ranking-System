"""Full project test script"""
import httpx
import sys

base = 'http://127.0.0.1:8000'
client = httpx.Client(timeout=120.0)
errors = []

def test(name, fn):
    try:
        fn()
        print(f"  ✓ {name}")
    except Exception as e:
        print(f"  ✗ {name}: {e}")
        errors.append(name)

# --- Auth Tests ---
print("\n=== AUTH TESTS ===")

def t1():
    r = client.post(f'{base}/api/v1/auth/login', json={'email': 'test_cand@test.com', 'password': 'Test@123'})
    assert r.status_code == 200
    global cand_token, headers_cand
    cand_token = r.json()['access_token']
    headers_cand = {'Authorization': f'Bearer {cand_token}'}
test("Login Candidate", t1)

def t2():
    r = client.post(f'{base}/api/v1/auth/login', json={'email': 'test_recruiter@test.com', 'password': 'Test@123'})
    assert r.status_code == 200
    global rec_token, headers_rec
    rec_token = r.json()['access_token']
    headers_rec = {'Authorization': f'Bearer {rec_token}'}
test("Login Recruiter", t2)

def t3():
    r = client.get(f'{base}/api/v1/auth/me', headers=headers_rec)
    assert r.status_code == 200
    assert r.json()['role'] == 'RECRUITER'
test("Auth /me", t3)

# --- Job Tests ---
print("\n=== JOB TESTS ===")

def t4():
    r = client.get(f'{base}/api/v1/jobs/')
    assert r.status_code == 200
    assert len(r.json()) > 0
test("List Jobs", t4)

def t5():
    r = client.get(f'{base}/api/v1/jobs/9')
    assert r.status_code == 200
    assert r.json()['title'] == 'AI Engineer'
test("Get Job by ID", t5)

# --- Candidate Tests ---
print("\n=== CANDIDATE TESTS ===")

def t6():
    r = client.get(f'{base}/api/v1/candidates/profile', headers=headers_cand)
    assert r.status_code == 200
    assert r.json()['candidate_id']
test("Get Candidate Profile", t6)

def t7():
    r = client.put(f'{base}/api/v1/candidates/profile', headers=headers_cand, json={
        'full_name': 'Test Candidate Updated',
        'years_of_experience': 5.0,
        'current_title': 'AI Engineer',
        'skills': [{'name': 'python', 'proficiency': 'advanced'}, {'name': 'pytorch', 'proficiency': 'advanced'}, {'name': 'nlp'}]
    })
    assert r.status_code == 200
test("Update Candidate Profile", t7)

def t8():
    print("    (Loading ML model, may take time...)")
    r = client.post(f'{base}/api/v1/jobs/9/apply', json={
        'skills': 'python, pytorch, nlp, machine learning, deep learning, rag',
        'years_of_experience': 5,
        'cover_note': 'Excited to apply!'
    }, headers=headers_cand)
    assert r.status_code == 200
    print(f"    Match Score: {r.json().get('match_score')}")
test("Apply to Job", t8)

def t9():
    r = client.get(f'{base}/api/v1/candidates/applications', headers=headers_cand)
    assert r.status_code == 200
    assert len(r.json()) > 0
test("My Applications", t9)

# --- Recruiter Tests ---
print("\n=== RECRUITER TESTS ===")

def t10():
    r = client.post(f'{base}/api/v1/jobs/9/seed-demo-applicants', headers=headers_rec)
    assert r.status_code == 200
    print(f"    {r.json().get('message')}")
test("Seed Demo Applicants", t10)

def t11():
    r = client.post(f'{base}/api/v1/screening/rank', json={'job_id': 9, 'top_k': 10}, headers=headers_rec)
    assert r.status_code == 200
    data = r.json()
    print(f"    Evaluated: {data.get('total_candidates_evaluated')}, Returned: {data.get('returned_count')}")
test("Screen/Rank Candidates", t11)

def t12():
    r = client.get(f'{base}/api/v1/analytics/dashboard', headers=headers_rec)
    assert r.status_code == 200
    data = r.json()
    print(f"    Jobs: {data['total_jobs']}, Applicants: {data['total_applicants']}")
test("Analytics Dashboard", t12)

def t13():
    r = client.post(f'{base}/api/v1/screening/auto-shortlist', json={'job_id': 9, 'threshold': 70.0}, headers=headers_rec)
    assert r.status_code == 200
    print(f"    {r.json().get('message')}")
test("Auto Shortlist", t13)

def t14():
    r = client.get(f'{base}/api/v1/screening/pipeline?job_id=9', headers=headers_rec)
    assert r.status_code == 200
    print(f"    Pipeline items: {len(r.json())}")
test("Interview Pipeline", t14)

# --- AI/Parsing Tests ---
print("\n=== PARSING TESTS ===")

def t15():
    r = client.post(f'{base}/api/v1/jobs/analyze-jd', json={
        'text': 'We need a Senior Python Developer with 5+ years experience in Django, FastAPI, PostgreSQL. Machine learning experience preferred. Must have Docker and AWS skills.',
        'title': 'Senior Python Dev'
    })
    assert r.status_code == 200
    data = r.json()
    print(f"    Required: {data.get('required_skills', [])[:4]}")
    print(f"    Preferred: {data.get('preferred_skills', [])[:4]}")
test("Analyze Job Description", t15)

def t16():
    r = client.post(f'{base}/api/v1/candidates/parse-resume-text', json={
        'text': 'John Doe\njohndoe@email.com\nSenior AI Engineer with 6 years of experience in Python, PyTorch, TensorFlow, NLP, RAG systems, FAISS. M.Tech in Computer Science from IIT Delhi.'
    })
    assert r.status_code == 200
    data = r.json()
    print(f"    Name: {data.get('full_name')}, YOE: {data.get('years_of_experience')}")
    print(f"    Skills: {[s['name'] if isinstance(s, dict) else s for s in data.get('skills', [])][:6]}")
test("Parse Resume Text", t16)

# --- Summary ---
print("\n" + "="*50)
if errors:
    print(f"FAILED: {len(errors)} test(s) failed: {', '.join(errors)}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED! ✓ Backend is fully functional.")
    sys.exit(0)
