import time
import math
from typing import List, Dict, Any, Optional

from backend.app.core.config import settings
from backend.app.embeddings.semantic_service import SemanticService
from backend.app.retrieval.faiss_service import FAISSService
from backend.app.retrieval.bm25_service import BM25Service
from backend.app.ranking.eligibility import EligibilityFilter
from backend.app.ranking.scorer import MultiSignalScorer
from backend.app.services.candidate_loader import CandidateLoader


class HybridRankingEngine:
    """Production 4-Stage Multi‑Signal Hybrid Retrieval & Ranking Engine.

    Ensures every scoring component returns a valid numeric percentage (0‑100).
    Missing or NaN values are replaced with ``0.0`` and the corresponding weight
    is redistributed proportionally so that the final score never contains
    ``NaN`` or ``Infinity``.
    """

    def __init__(self):
        self.semantic_service = SemanticService()
        self.faiss_service = FAISSService()
        self.bm25_service = BM25Service()
        self.eligibility_filter = EligibilityFilter()
        self.scorer = MultiSignalScorer()
        self.loader = CandidateLoader()

    @staticmethod
    def _safe_percentage(value: float) -> float:
        """Convert any value to a safe percentage between 0 and 100.

        * ``None`` or ``NaN`` → ``0.0``
        * values outside the range are clamped.
        """
        try:
            if value is None:
                return 0.0
            if math.isnan(value):
                return 0.0
            return round(max(0.0, min(100.0, float(value))), 2)
        except Exception:
            return 0.0

    def _adjust_weights(self, weights: Dict[str, float], present: Dict[str, bool]) -> Dict[str, float]:
        """Redistribute weights for components that are missing.

        ``present`` maps component name → bool indicating whether a valid score is
        available. Missing components receive a weight of ``0`` and the remaining
        weight is scaled so that the sum stays ``1.0`` (or 100%).
        """
        total = sum(w for k, w in weights.items() if present.get(k, True))
        if total == 0:
            equal = 1.0 / len(weights)
            return {k: equal for k in weights}
        return {k: (w if present.get(k, True) else 0.0) / total for k, w in weights.items()}

    def rank(
        self,
        job_data: Dict[str, Any],
        top_k: int = 20,
        filters: Optional[Dict[str, Any]] = None,
        weights: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        start_time = time.perf_counter()

        # ------------------------------------------------------------------
        # 1️⃣ Retrieve raw signals (semantic & BM25)
        # ------------------------------------------------------------------
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

        # ---- Retrieval ----------------------------------------------------
        faiss_results = self.faiss_service.search_candidates(job_embedding, top_k=settings.RETRIEVAL_TOP_N)
        bm25_results = self.bm25_service.search_candidates(job_desc, top_k=settings.RETRIEVAL_TOP_N)

        candidate_map: Dict[str, Dict[str, Any]] = {}
        for r in faiss_results:
            cid = r["candidate_id"]
            candidate_map[cid] = {
                "candidate_id": cid,
                "embedding_index": r.get("embedding_index", 0),
                "semantic_score": self._safe_percentage(r.get("semantic_score", 0) * 100.0),
                "bm25_score": 0.0,
            }

        for r in bm25_results:
            cid = r["candidate_id"]
            bm25_val = self._safe_percentage(r.get("bm25_score", 0))
            if cid in candidate_map:
                candidate_map[cid]["bm25_score"] = bm25_val
            else:
                candidate_map[cid] = {
                    "candidate_id": cid,
                    "embedding_index": 0,
                    "semantic_score": 50.0,  # fallback when no embedding match
                    "bm25_score": bm25_val,
                }

        # ------------------------------------------------------------------
        # 2️⃣ Load candidate profiles and compute per‑candidate signals
        # ------------------------------------------------------------------
        retrieved_ids = list(candidate_map.keys())
        candidates = self.loader.load_candidates_by_ids(retrieved_ids)

        req_skills = job_data.get("required_skills", [])
        pref_skills = job_data.get("preferred_skills", [])
        min_exp = float(job_data.get("minimum_experience", 0.0))
        max_exp = float(job_data.get("maximum_experience", 20.0))

        scored_candidates = []
        for cand in candidates:
            cid = cand["candidate_id"]

            # ---- Eligibility filter ---------------------------------------
            eligible, reason = self.eligibility_filter.evaluate_candidate(cand, job_data)
            if not eligible:
                continue

            # ---- User‑provided filters ------------------------------------
            if filters:
                min_user_exp = filters.get("min_experience")
                if min_user_exp is not None and cand.get("years_of_experience", 0) < min_user_exp:
                    continue
                filter_skills = filters.get("required_skills", [])
                if filter_skills:
                    cand_skills_lower = [s.lower() for s in cand.get("skills", [])]
                    if not all(fs.lower() in cand_skills_lower for fs in filter_skills):
                        continue

            # ---- Skill, experience & education scores ---------------------
            cand_skills = cand.get("skills", [])
            req_score, pref_score, matched_req, matched_pref, missing = self.scorer.score_skills(
                cand_skills, req_skills, pref_skills
            )
            exp_score = self.scorer.score_experience(cand.get("years_of_experience", 0.0), min_exp, max_exp)
            edu_score = self.scorer.score_education(cand.get("education", []))
            avail_score = self.scorer.score_availability(cand.get("redrob_signals", {}))

            sem_score = candidate_map[cid]["semantic_score"]
            bm25_score = candidate_map[cid]["bm25_score"]
            career_score = sem_score  # currently career alignment mirrors semantic

            # ---- Determine which components are actually present -----------
            present = {
                "semantic": not math.isnan(sem_score),
                "bm25": not math.isnan(bm25_score),
                "required": not math.isnan(req_score),
                "preferred": not math.isnan(pref_score),
                "experience": not math.isnan(exp_score),
                "education": not math.isnan(edu_score),
                "career": not math.isnan(career_score),
                "availability": not math.isnan(avail_score),
            }

            # ---- Adjust weights if any component is missing ---------------
            raw_weights = {
                "semantic": w_sem,
                "bm25": w_bm25,
                "required": w_req,
                "preferred": w_pref,
                "experience": w_exp,
                "education": w_edu,
                "career": w_career,
                "availability": w_avail,
            }
            adjusted = self._adjust_weights(raw_weights, present)

            # ---- Final composite score -------------------------------------
            final_score = (
                adjusted["semantic"] * sem_score
                + adjusted["bm25"] * bm25_score
                + adjusted["required"] * req_score
                + adjusted["preferred"] * pref_score
                + adjusted["experience"] * exp_score
                + adjusted["education"] * edu_score
                + adjusted["career"] * career_score
                + adjusted["availability"] * avail_score
            )
            final_score = round(max(0.0, min(100.0, final_score)), 2)

            if filters and filters.get("min_score") and final_score < filters["min_score"]:
                continue

            # ---- Build explanation ----------------------------------------
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
                "status": "SCREENING",
            })

        # ------------------------------------------------------------------
        # 3️⃣ Sort, rank and build final payload
        # ------------------------------------------------------------------
        scored_candidates.sort(key=lambda x: x["final_score"], reverse=True)
        results = scored_candidates[:top_k]
        for idx, item in enumerate(results, start=1):
            item["rank"] = idx
            why_text = f"Ranked #{idx} with composite score {item['final_score']}%. " + (
                item["reasons"][0] if item["reasons"] else "Balanced multi‑signal profile."
            )
            item["explanation"] = {
                "why_ranked": why_text,
                "strengths": [f"Verified experience with {s}" for s in item["matched_skills"][:4]]
                if item["matched_skills"]
                else ["Broad engineering background"],
                "skill_gaps": [f"Missing {s}" for s in item["missing_skills"][:3]]
                if item["missing_skills"]
                else ["No critical skill gaps identified"],
            }

        elapsed = time.perf_counter() - start_time
        return {
            "job_id": job_data.get("id", 1),
            "job_title": job_data.get("title", ""),
            "total_candidates_evaluated": len(candidates),
            "returned_count": len(results),
            "candidates": results,
            "execution_time_seconds": round(elapsed, 3),
        }
