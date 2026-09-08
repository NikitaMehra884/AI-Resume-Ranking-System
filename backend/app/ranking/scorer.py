from typing import Dict, Any, List

class MultiSignalScorer:
    """Stage 3 Scorer: Computes normalized component scores [0-100] across multiple dimensions."""

    def score_skills(self, candidate_skills: List[str], required_skills: List[str], preferred_skills: List[str]):
        cand_set = {s.lower() for s in candidate_skills}
        req_set = {s.lower() for s in required_skills}
        pref_set = {s.lower() for s in preferred_skills}

        matched_req = [s for s in required_skills if s.lower() in cand_set]
        matched_pref = [s for s in preferred_skills if s.lower() in cand_set]

        req_score = (len(matched_req) / len(required_skills) * 100.0) if required_skills else 100.0
        pref_score = (len(matched_pref) / len(preferred_skills) * 100.0) if preferred_skills else 100.0

        missing_skills = [s for s in required_skills if s.lower() not in cand_set]
        return round(req_score, 2), round(pref_score, 2), matched_req, matched_pref, missing_skills

    def score_experience(self, candidate_exp: float, min_exp: float, max_exp: float = 20.0) -> float:
        if min_exp <= 0:
            return 100.0
        if candidate_exp >= min_exp:
            if candidate_exp <= max_exp:
                return 100.0
            return max(85.0, 100.0 - (candidate_exp - max_exp) * 1.5)
        return round((candidate_exp / min_exp) * 100.0, 2)

    def score_education(self, education_list: List[Dict[str, Any]]) -> float:
        if not education_list:
            return 50.0
        score = 0.0
        for edu in education_list:
            field = str(edu.get("field_of_study", "")).lower()
            tier = str(edu.get("tier", "")).lower()

            if any(k in field for k in ["computer", "artificial intelligence", "data", "software", "information technology", "math"]):
                score += 60.0
            else:
                score += 30.0

            if tier == "tier_1":
                score += 40.0
            elif tier == "tier_2":
                score += 30.0
            elif tier == "tier_3":
                score += 20.0
            else:
                score += 15.0
        return round(min(score / len(education_list), 100.0), 2)

    def score_availability(self, redrob_signals: Dict[str, Any]) -> float:
        score = 0.0
        score += (float(redrob_signals.get("profile_completeness_score", 80)) / 100.0) * 25.0

        resp = float(redrob_signals.get("recruiter_response_rate", 0.5))
        if resp > 1.0:
            resp /= 100.0
        score += min(1.0, max(0.0, resp)) * 30.0

        notice_days = int(redrob_signals.get("notice_period_days", 30))
        if notice_days <= 15:
            score += 25.0
        elif notice_days <= 30:
            score += 20.0
        elif notice_days <= 60:
            score += 15.0
        else:
            score += 10.0

        if redrob_signals.get("open_to_work_flag", True):
            score += 20.0

        return round(min(score, 100.0), 2)
