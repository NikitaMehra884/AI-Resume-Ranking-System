from backend.config import *


class RankingService:

    # ==========================================
    # Skill Score
    # ==========================================

    def calculate_skill_score(
        self,
        candidate_skills,
        job_skills
    ):

        if not job_skills:
            return 0.0, []

        candidate_set = set(candidate_skills)

        matched = [
            skill
            for skill in job_skills
            if skill in candidate_set
        ]

        score = (
            len(matched) /
            len(job_skills)
        ) * 100

        return round(score, 2), matched

    # ==========================================
    # Experience Score
    # ==========================================

    def calculate_experience_score(
        self,
        candidate_experience,
        minimum_experience
    ):

        if minimum_experience <= 0:
            return 100.0

        if candidate_experience >= minimum_experience:
            return 100.0

        return round(
            (
                candidate_experience /
                minimum_experience
            ) * 100,
            2
        )

    # ==========================================
    # Final Hybrid Score
    # ==========================================

    def calculate_hybrid_score(

        self,

        skill_score,

        experience_score,

        education_score,

        career_relevance,

        redrob_score,

        semantic_score,

        bm25_score,

        company_score,

        notice_score,

        location_score

    ):

        score = 0.0

        score += (
            skill_score *
            SKILL_WEIGHT
        )

        score += (
            experience_score *
            EXPERIENCE_WEIGHT
        )

        score += (
            education_score *
            EDUCATION_WEIGHT
        )

        score += (
            career_relevance *
            CAREER_WEIGHT
        )

        score += (
            redrob_score *
            REDROB_WEIGHT
        )

        score += (
            semantic_score *
            100 *
            SEMANTIC_WEIGHT
        )

        score += (
            bm25_score *
            BM25_WEIGHT
        )

        score += (
            company_score *
            COMPANY_WEIGHT
        )

        score += (
            notice_score *
            NOTICE_WEIGHT
        )

        score += (
            location_score *
            LOCATION_WEIGHT
        )

        score = max(
            0.0,
            min(
                100.0,
                score
            )
        )

        return round(score, 2)