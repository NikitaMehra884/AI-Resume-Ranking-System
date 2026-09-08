from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_jobs_list_endpoint():
    response = client.get("/api/v1/jobs/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analyze_jd_endpoint():
    payload = {
        "title": "Backend Lead",
        "text": "Senior Backend Lead with 5+ years experience. Must have: Python, FastAPI, PostgreSQL. Preferred: Docker."
    }
    response = client.post("/api/v1/jobs/analyze-jd", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Backend Lead"
    assert "python" in data["required_skills"]
    assert data["minimum_experience"] >= 5.0
