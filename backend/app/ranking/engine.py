import time
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings
from backend.app.embeddings.semantic_service import SemanticService
from backend.app.retrieval.faiss_service import FAISSService
from backend.app.retrieval.bm25_service import BM25Service
from backend.app.ranking.eligibility import EligibilityFilter
from backend.app.ranking.scorer import MultiSignalScorer
from backend.app.services.candidate_loader import CandidateLoader

class HybridRankingEngine:
    """Production 4-Stage Multi-Signal Hybrid Retrieval & Ranking Engine."""

    def __init__(self):
        self.semantic_service = SemanticService()
        self.faiss_service = FAISSService()
        self.bm25_service = BM25Service()
        self.eligibility_filter = EligibilityFilter()
        self.scorer = MultiSignalScorer()
        self.loader = CandidateLoader()

    def rank(
        self,
        job_data: Dict[str, Any],
        top_k: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        start_time = time.perf_counter()

        w_sem = weights.get("semantic_weight", settings.SEMANTIC_WEIGHT) if weights else settings.SEMANTIC_WEIGHT
        w_bm25 = weights.get("bm25_weight", settings.BM25_WEIGHT) if weights else settings.BM25_WEIGHT
        w_req = weights.get("required_skill_weight", settings.REQUIRED_SKILL_WEIGHT) if weights else settings.REQUIRED_SKILL_WEIGHT
        w_pref = weights.get("preferred_skill_weight", settings.PREFERRED_SKILL_WEIGHT) if weights else settings.PREFERRED_SKILL_WEIGHT
        w_exp = weights.get("experience_weight", settings.EXPERIENCE_WEIGHT) if weights else settings.EXPERIENCE_WEIGHT
        w_edu = weights.get("education_weight", settings.EDUCATION_WEIGHT) if weights else settings.EDUCATION_WEIGHT
        w_career = weights.get("career_alignment_weight", settings.CAREER_ALIGNMENT_WEIGHT) if weights else settings.CAREER_ALIGNMENT_WEIGHT
        w_avail = weights.get("availability_weight", settings.AVAILABILITY_WEIGHT) if weights else settings.AVAILABILITY_WEIGHT

        job_desc = job_data.get("description", "")
        job_embedding = self.semantic_service.embedding(job_desc)

        # STAGE 2: Hybrid Candidate Retrieval (FAISS + BM25 Union)
        faiss_results = self.faiss_service.search_candidates(job_embedding, top_k=settings.RETRIEVAL_TOP_N)
        bm25_results = self.bm25_service.search_candidates(job_desc, top_k=settings.RETRIEVAL_TOP_N)

        candidate_map = {}
        for r in faiss_results:
            cid = r["candidate_id"]
            candidate_map[cid] = {
                "candidate_id": cid,
                "embedding_index": r.get("embedding_index", 0),
                "semantic_score": round(r["semantic_score"] * 100.0, 2),
                "bm25_score": 0.0
            }

        for r in bm25_results:
            cid = r["candidate_id"]
            if cid in candidate_map:
                candidate_map[cid]["bm25_score"] = round(r["bm25_score"], 2)
            else:
                candidate_map[cid] = {
                    "candidate_id": cid,
                    "embedding_index": 0,
                    "semantic_score": 50.0,
                    "bm25_score": round(r["bm25_score"], 2)
                }

        retrieved_ids = list(candidate_map.keys())
        candidates = self.loader.load_candidates_by_ids(retrieved_ids)

        req_skills = job_data.get("required_skills", [])
        pref_skills = job_data.get("preferred_skills", [])
        min_exp = float(job_data.get("minimum_experience", 0.0))
        max_exp = float(job_data.get("maximum_experience", 20.0))

        # STAGE 1 & 3: Filter & Multi-Signal Scoring
        scored_candidates = []
        for cand in candidates:
            cid = cand["candidate_id"]

            # Stage 1 Eligibility Hard Filter
            eligible, reason = self.eligibility_filter.evaluate_candidate(cand, job_data)
            if not eligible:
                continue

            # Check User Filters (Phase 4)
            if filters:
                min_user_exp = filters.get("min_experience")
                if min_user_exp is not None and cand.get("years_of_experience", 0) < min_user_exp:
                    continue

                filter_skills = filters.get("required_skills", [])
                if filter_skills:
                    cand_skills_lower = [s.lower() for s in cand.get("skills", [])]
                    if not all(fs.lower() in cand_skills_lower for fs in filter_skills):
                        continue

            cand_skills = cand.get("skills", [])
            req_score, pref_score, matched_req, matched_pref, missing = self.scorer.score_skills(cand_skills, req_skills, pref_skills)
            exp_score = self.scorer.score_experience(cand.get("years_of_experience", 0.0), min_exp, max_exp)
            edu_score = self.scorer.score_education(cand.get("education", []))
            avail_score = self.scorer.score_availability(cand.get("redrob_signals", {}))

            sem_score = candidate_map[cid]["semantic_score"]
            bm25_score = candidate_map[cid]["bm25_score"]
            career_score = sem_score

            # STAGE 4: Final Score Computation
            final_score = (
                w_sem * sem_score +
                w_bm25 * bm25_score +
                w_req * req_score +
                w_pref * pref_score +
                w_exp * exp_score +
                w_edu * edu_score +
                w_career * career_score +
                w_avail * avail_score
            )
            final_score = round(max(0.0, min(100.0, final_score)), 2)

            if filters and filters.get("min_score") and final_score < filters["min_score"]:
                continue

            reasons = []
            if req_score >= 80:
                reasons.append(f"Strong required skills match ({len(matched_req)}/{len(req_skills)})")
            if exp_score >= 95:
                reasons.append(f"Experience aligned with target ({cand.get('years_of_experience', 0):.1f} yrs)")
            if sem_score >= 70:
                reasons.append("High semantic role relevance")

            scored_candidates.append({
                "candidate_id": cid,
                "name": cand.get("name", "Candidate"),
                "current_title": cand.get("current_title", ""),
                "current_company": cand.get("current_company", ""),
                "years_of_experience": cand.get("years_of_experience", 0.0),
                "location": cand.get("location", ""),
                "country": cand.get("country", ""),
                "final_score": final_score,
                "semantic_score": sem_score,
                "keyword_score": bm25_score,
                "skill_score": req_score,
                "experience_score": exp_score,
                "education_score": edu_score,
                "career_score": career_score,
                "availability_score": avail_score,
                "matched_skills": matched_req + matched_pref,
                "missing_skills": missing,
                "reasons": reasons,
                "status": "SCREENING"
            })

        scored_candidates.sort(key=lambda x: x["final_score"], reverse=True)
        results = scored_candidates[:top_k]
        for idx, item in enumerate(results, start=1):
            item["rank"] = idx
            why_text = f"Ranked #{idx} with composite score {item['final_score']}%. " + (item["reasons"][0] if item["reasons"] else "Balanced multi-signal profile.")
            item["explanation"] = {
                "why_ranked": why_text,
                "strengths": [f"Verified experience with {s}" for s in item["matched_skills"][:4]] if item["matched_skills"] else ["Broad engineering background"],
                "skill_gaps": [f"Missing {s}" for s in item["missing_skills"][:3]] if item["missing_skills"] else ["No critical skill gaps identified"]
            }

        elapsed = time.perf_counter() - start_time
        return {
            "job_id": job_data.get("id", 1),
            "job_title": job_data.get("title", ""),
            "total_candidates_evaluated": len(candidates),
            "returned_count": len(results),
            "candidates": results,
            "execution_time_seconds": round(elapsed, 3)
        }
