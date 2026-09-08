from backend.app.parsing.skill_extractor import SkillExtractor
from backend.app.parsing.jd_parser import JDParser
from backend.app.parsing.resume_parser import ResumeParser

def test_skill_extractor():
    extractor = SkillExtractor()
    text = "Proficient in Python, PyTorch, FAISS, and RAG. Experience with LLM and large language models."
    skills = extractor.extract_skills(text)
    assert "python" in skills
    assert "pytorch" in skills
    assert "faiss" in skills
    assert "rag" in skills
    assert "llm" in skills

def test_jd_parser_distinguishes_required_from_preferred():
    parser = JDParser()
    jd_text = """
    Job Title: Senior AI Engineer
    Must have: Python, PyTorch, FAISS, RAG
    Nice to have: Docker, AWS, Kubernetes
    Experience: 5-8 years of production experience.
    """
    parsed = parser.parse_jd(jd_text, title="Senior AI Engineer")
    assert parsed["job_title"] == "Senior AI Engineer"
    assert parsed["minimum_experience"] == 5.0
    assert "python" in parsed["required_skills"]
    assert "pytorch" in parsed["required_skills"]
    assert "docker" in parsed["preferred_skills"] or "aws" in parsed["preferred_skills"]

def test_resume_parser_extracts_contact_and_skills():
    parser = ResumeParser()
    text = """
    Jane Doe
    jane.doe@example.com | +1 555-123-4567
    Experience: 6 years of software development.
    Skills: Python, FastAPI, Docker, PostgreSQL, Machine Learning.
    Education: B.Tech in Computer Science from University of Delhi.
    """
    res = parser.parse_resume(text, full_name="Jane Doe")
    assert res["email"] == "jane.doe@example.com"
    assert res["years_of_experience"] == 6.0
    skill_names = [s["name"] for s in res["skills"]]
    assert "python" in skill_names
    assert "fastapi" in skill_names
