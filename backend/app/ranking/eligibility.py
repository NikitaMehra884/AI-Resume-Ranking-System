from typing import Dict, Any, Tuple

class EligibilityFilter:
    """Stage 1 Hard Filters: Evaluates eligibility and prevents misaligned role anomalies."""

    DISQUALIFIED_ROLES_FOR_TECH = {
        "customer support", "customer service", "operations manager", "call center",
        "administrative assistant", "front desk", "receptionist", "sales representative",
        "retail associate", "cashier", "telemarketer"
    }

    def evaluate_candidate(self, candidate_data: Dict[str, Any], job_data: Dict[str, Any]) -> Tuple[bool, str]:
        profile = candidate_data.get("profile", {})
        title = profile.get("current_title", candidate_data.get("current_title", "")).lower()
        job_title = job_data.get("title", "").lower()

        # Disqualify non-tech roles when job is AI/ML/Software Engineering
        is_tech_job = any(w in job_title for w in ["ai", "machine learning", "software", "backend", "full stack", "data scientist", "engineer"])
        if is_tech_job:
            if any(disq in title for disq in self.DISQUALIFIED_ROLES_FOR_TECH):
                skills = [s.lower() if isinstance(s, str) else s.get("name", "").lower() for s in candidate_data.get("skills", [])]
                tech_skills_count = sum(1 for s in skills if s in {"python", "pytorch", "tensorflow", "fastapi", "machine learning", "nlp", "rag", "faiss"})
                if tech_skills_count < 3:
                    return False, f"Current title '{title}' misaligned with technical engineering mandate."

        # Minimum Experience Check
        min_exp = float(job_data.get("minimum_experience", 0.0))
        cand_exp = float(profile.get("years_of_experience", candidate_data.get("years_of_experience", 0.0)))
        if min_exp > 0 and cand_exp < (min_exp * 0.4):
            return False, f"Candidate experience ({cand_exp:.1f} yrs) below threshold for {min_exp:.1f} yr requirement."

        return True, "Eligible"
