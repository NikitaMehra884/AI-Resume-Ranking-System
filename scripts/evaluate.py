import json
import math
from typing import List, Dict, Any
import numpy as np
from pathlib import Path
from backend.app.ranking.engine import HybridRankingEngine
from backend.app.parsing.jd_parser import JDParser

ROOT = Path(__file__).resolve().parents[1]

# Ground-truth evaluation dataset with graded relevance judgments (0 to 3)
# 3 = Highly Relevant (Senior AI Engineer with Python, PyTorch, FAISS, RAG, 5+ yrs)
# 2 = Relevant (Software Engineer with Python and ML experience)
# 1 = Somewhat Relevant (Backend / Data engineer with Python, low ML experience)
# 0 = Irrelevant (Non-tech roles or unrelated domain)
GROUND_TRUTH_LABELS = {
    "CAND_0005649": 3, # Senior Data Scientist with AI skills
    "CAND_0007460": 3, # AI Engineer with PyTorch, NLP, FAISS
    "CAND_0000001": 2, # Backend Engineer with 6.9 yrs and Python/Spark
    "CAND_0079764": 0, # Customer Support
    "CAND_0056327": 0, # Operations Manager
    "CAND_0000002": 2, # Machine Learning practitioner
    "CAND_0000003": 1, # Data Analyst
    "CAND_0000004": 2, # Fullstack Engineer with Python
    "CAND_0000005": 3, # Senior AI Architect
    "CAND_0000006": 1, # Junior Frontend Developer
}

def dcg_at_k(r: List[int], k: int) -> float:
    r = np.asarray(r, dtype=float)[:k]
    if r.size:
        return np.sum((2**r - 1) / np.log2(np.arange(2, r.size + 2)))
    return 0.0

def ndcg_at_k(r: List[int], k: int) -> float:
    dcg_max = dcg_at_k(sorted(r, reverse=True), k)
    if not dcg_max:
        return 0.0
    return dcg_at_k(r, k) / dcg_max

def evaluate_ranking(top_k: int = 10):
    print("=" * 70)
    print("AI RECRUITMENT INTELLIGENCE PLATFORM - RANKING EVALUATION")
    print("=" * 70)

    engine = HybridRankingEngine()
    parser = JDParser()
    jd_text = """
    Job Title: Senior AI Engineer
    Company: Redrob AI
    Must have: Python, PyTorch, FAISS, RAG, LLM, Machine Learning, FastAPI.
    Experience: 5+ years.
    """
    job_data = parser.parse_jd(jd_text, title="Senior AI Engineer")
    job_data["description"] = jd_text

    result = engine.rank(job_data, top_k=50)
    ranked_candidates = result["candidates"]

    # Dynamically score candidate relevance based on ground-truth criteria:
    # 3 = High Match (AI/ML Engineer with Python/PyTorch/NLP/FAISS and >= 5 yrs)
    # 2 = Relevant (Software Engineer with Python/Backend and >= 3 yrs)
    # 1 = Borderline (Junior or partial skills)
    # 0 = Irrelevant (Non-tech or missing core competencies)
    relevance_scores = []
    binary_relevant = []
    mrr_rank = None

    for idx, c in enumerate(ranked_candidates, start=1):
        cid = c["candidate_id"]
        # Explicit ground truth override if present
        if cid in GROUND_TRUTH_LABELS:
            rel = GROUND_TRUTH_LABELS[cid]
        else:
            title = (c.get("current_title") or "").lower()
            skills = [s.lower() for s in c.get("matched_skills", [])]
            exp = float(c.get("years_of_experience", 0.0))

            has_ai = any(term in title for term in ["ai", "machine learning", "ml", "data scientist", "nlp", "vision"]) or any(s in skills for s in ["pytorch", "faiss", "machine learning", "rag", "llm", "tensorflow"])
            has_py = "python" in skills or "python" in title or "software" in title or "engineer" in title

            if has_ai and exp >= 4.0:
                rel = 3
            elif has_py and exp >= 2.0:
                rel = 2
            elif has_py or exp >= 1.0:
                rel = 1
            else:
                rel = 0

        relevance_scores.append(rel)
        is_rel = 1 if rel >= 2 else 0
        binary_relevant.append(is_rel)
        if is_rel and mrr_rank is None:
            mrr_rank = idx

    # Compute Metrics
    p_at_5 = np.mean(binary_relevant[:5]) if len(binary_relevant) >= 5 else 0.0
    p_at_10 = np.mean(binary_relevant[:10]) if len(binary_relevant) >= 10 else 0.0

    total_relevant_in_gt = sum(1 for v in GROUND_TRUTH_LABELS.values() if v >= 2)
    found_relevant_at_10 = sum(binary_relevant[:10])
    recall_at_10 = min(1.0, found_relevant_at_10 / max(1, total_relevant_in_gt))

    mrr = (1.0 / mrr_rank) if mrr_rank else 0.0
    ndcg_5 = ndcg_at_k(relevance_scores, 5)
    ndcg_10 = ndcg_at_k(relevance_scores, 10)

    print("\nEVALUATION METRICS SUMMARY (Top-10 Cutoff):")
    print("-" * 70)
    print(f"Precision@5   : {p_at_5:.4f} ({p_at_5*100:.1f}%)")
    print(f"Precision@10  : {p_at_10:.4f} ({p_at_10*100:.1f}%)")
    print(f"Recall@10     : {recall_at_10:.4f} ({recall_at_10*100:.1f}%)")
    print(f"MRR           : {mrr:.4f}")
    print(f"NDCG@5        : {ndcg_5:.4f}")
    print(f"NDCG@10       : {ndcg_10:.4f}")
    print("=" * 70)

if __name__ == "__main__":
    evaluate_ranking()
