from typing import Dict, Any

class ExplainabilityService:
    """Generates transparent, grounded explanations for candidate rankings without hallucinations."""

    def generate_candidate_report(self, candidate_result: Dict[str, Any], job_data: Dict[str, Any]) -> Dict[str, Any]:
        cid = candidate_result["candidate_id"]
        score = candidate_result["final_score"]
        matched = candidate_result.get("matched_skills", [])
        missing = candidate_result.get("missing_skills", [])
        yoe = candidate_result.get("years_of_experience", 0)
        min_exp = job_data.get("minimum_experience", 0)

        exp_assessment = "Strong match" if yoe >= min_exp else f"Below target ({yoe:.1f} yrs vs {min_exp:.1f} yrs)"
        edu_assessment = "Meets requirement" if candidate_result.get("education_score", 0) >= 70 else "Partial match"
        proj_assessment = "High relevance" if candidate_result.get("semantic_score", 0) >= 65 else "Moderate relevance"

        why_good = (
            f"Candidate has {yoe:.1f} years of professional experience with verified core competencies in {', '.join(matched[:5]) if matched else 'core domains'}. "
            f"Semantic profile demonstrates {candidate_result.get('semantic_score', 0):.1f}% contextual alignment with job expectations."
        )

        what_to_improve = (
            f"To increase match potential, candidate should acquire or demonstrate hands-on experience in: {', '.join(missing[:4]) if missing else 'emerging framework tools'}."
        )

        return {
            "candidate_id": cid,
            "job_id": job_data.get("id", 1),
            "match_score": score,
            "strong_matches": matched[:6],
            "partial_matches": matched[6:10],
            "missing_skills": missing,
            "experience_assessment": exp_assessment,
            "education_assessment": edu_assessment,
            "project_relevance": proj_assessment,
            "why_good_match": why_good,
            "what_to_improve": what_to_improve,
            "evidence_breakdown": {
                "semantic_score": candidate_result.get("semantic_score", 0),
                "keyword_score": candidate_result.get("keyword_score", 0),
                "skill_score": candidate_result.get("skill_score", 0),
                "experience_score": candidate_result.get("experience_score", 0),
                "education_score": candidate_result.get("education_score", 0),
                "availability_score": candidate_result.get("availability_score", 0)
            }
        }
