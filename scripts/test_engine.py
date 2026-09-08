from backend.app.ranking.engine import HybridRankingEngine
from backend.app.parsing.jd_parser import JDParser
from backend.app.core.config import settings

jd_parser = JDParser()
jd_text = """
Job Title: Senior AI Engineer
We are seeking a Senior AI Engineer with 5-9 years of experience.
Must have: Python, PyTorch, FAISS, LLM, RAG, Machine Learning, Fastapi.
Preferred: Docker, Kubernetes, AWS.
Experience: 5+ years building production search and ranking systems.
"""
job_data = jd_parser.parse_jd(jd_text, title="Senior AI Engineer")
job_data["description"] = jd_text

engine = HybridRankingEngine()
result = engine.rank(job_data, top_k=5)

print("Status: Success!")
print(f"Evaluated candidates: {result['total_candidates_evaluated']}")
print(f"Top 5 candidates:")
for c in result["candidates"]:
    print(f"Rank {c['rank']}: {c['name']} ({c['current_title']} at {c['current_company']}) - Score: {c['final_score']} (Skills: {c['skill_score']}, Sem: {c['semantic_score']})")
