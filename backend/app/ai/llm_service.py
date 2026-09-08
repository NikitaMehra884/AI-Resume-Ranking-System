from typing import Dict, Any, List
from backend.app.core.config import settings

class LLMService:
    """Generative AI service with dual modes: external LLM or deterministic grounded fallback."""

    def __init__(self):
        self.has_key = bool(settings.GEMINI_API_KEY or settings.OPENAI_API_KEY)

    def generate_comparison_summary(self, candidates: List[Dict[str, Any]], job_title: str) -> str:
        if len(candidates) < 2:
            return "Please select at least two candidates to compare."

        c1 = candidates[0]
        c2 = candidates[1]

        c1_name = c1.get("name", "Candidate A")
        c2_name = c2.get("name", "Candidate B")
        c1_score = c1.get("final_score", 0.0)
        c2_score = c2.get("final_score", 0.0)
        c1_exp = c1.get("years_of_experience", 0.0)
        c2_exp = c2.get("years_of_experience", 0.0)
        c1_skills = c1.get("matched_skills", [])
        c2_skills = c2.get("matched_skills", [])

        if c1_score >= c2_score:
            top_cand = c1_name
            other_cand = c2_name
        else:
            top_cand = c2_name
            other_cand = c1_name

        summary = (
            f"Comparison for {job_title}: {top_cand} demonstrates the strongest overall alignment with a composite score of {max(c1_score, c2_score):.1f}%. "
            f"{c1_name} brings {c1_exp:.1f} years of experience and verified competencies in {', '.join(c1_skills[:3]) if c1_skills else 'core stack'}, "
            f"whereas {c2_name} offers {c2_exp:.1f} years with strengths in {', '.join(c2_skills[:3]) if c2_skills else 'core stack'}. "
            f"Recommendation: Proceed with {top_cand} for primary technical interview, while retaining {other_cand} as a viable secondary candidate."
        )
        return summary

    def generate_interview_questions(self, candidate_data: Dict[str, Any], job_title: str) -> Dict[str, List[Dict[str, str]]]:
        skills = candidate_data.get("matched_skills", ["Python", "Machine Learning"])
        top_skill = skills[0] if skills else "Python"
        second_skill = skills[1] if len(skills) > 1 else "System Architecture"
        yoe = candidate_data.get("years_of_experience", 4.0)

        return {
            "technical_questions": [
                {
                    "question": f"In your work with {top_skill}, how do you address memory optimization and latency bottlenecks when serving low-latency queries at scale?",
                    "rationale": f"Evaluates production-readiness in candidate's primary strength ({top_skill})."
                },
                {
                    "question": f"Compare trade-offs between dense semantic indexing and sparse BM25 indexing in the context of {second_skill}.",
                    "rationale": f"Tests algorithmic intuition and system trade-offs in {second_skill}."
                }
            ],
            "behavioral_questions": [
                {
                    "question": f"Given your {yoe:.1f} years of experience, describe a high-stakes technical disagreement with a team member and how you resolved it without slowing project velocity.",
                    "rationale": "Measures collaboration, emotional intelligence, and engineering leadership."
                }
            ],
            "project_questions": [
                {
                    "question": "Walk us through a critical architecture design you authored. What assumptions failed once it met real users, and what did you refactor?",
                    "rationale": "Validates hands-on production shipping experience vs theoretical knowledge."
                }
            ],
            "role_specific_questions": [
                {
                    "question": f"For this {job_title} role, how would you design an offline-to-online evaluation pipeline to monitor ranking degradation over time?",
                    "rationale": f"Directly tests essential production competencies for {job_title}."
                }
            ]
        }
