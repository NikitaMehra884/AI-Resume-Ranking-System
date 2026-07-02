from backend.services.skill_service import SkillService
from backend.services.ranking_service import RankingService
from backend.services.bm25_service import BM25Service
from backend.services.education_service import EducationService
from backend.services.career_relevance_service import CareerRelevanceService
from backend.services.redrob_service import RedrobService
from backend.services.company_score_service import CompanyScoreService
from backend.services.notice_period_service import NoticePeriodService
from backend.services.location_service import LocationService


class CandidateRanker:

    def __init__(
        self,
        semantic_service=None,
        bm25_service=None,
        skill_service=None,
        ranking_service=None,
    ):

        # reuse shared services when provided to avoid repeated initialization
        self.semantic_service = semantic_service

        self.skill_service = skill_service or SkillService()
        self.ranking_service = ranking_service or RankingService()

        self.bm25_service = bm25_service or BM25Service()

        self.education_service = EducationService()
        # career relevance should reuse the semantic service
        self.career_relevance_service = CareerRelevanceService(
            semantic_service=self.semantic_service
        )

        self.redrob_service = RedrobService()

        self.company_service = CompanyScoreService()
        self.notice_service = NoticePeriodService()
        self.location_service = LocationService()

    # ======================================================
    # Rank Candidate
    # ======================================================

    def rank_candidate(
        self,
        candidate,
        candidate_document,
        candidate_embedding,
        job,
        job_embedding,
        job_skills=None,
        semantic_service=None,
        candidate_index=None,
        career_relevance_score=None,
        candidate_skills=None,
    ):

        # ==========================================
        # Skill Score
        # ==========================================

        if candidate_skills is None:
            candidate_skills = self.skill_service.extract_skills(candidate_document)

        # Job skills can be passed in (cached) to avoid repeated extraction
        if job_skills is None:
            job_skills = self.skill_service.extract_skills(job.description)

        skill_score, matched_skills = (
            self.ranking_service.calculate_skill_score(
                candidate_skills,
                job_skills
            )
        )

        # ==========================================
        # Experience Score
        # ==========================================

        experience_score = (
            self.ranking_service.calculate_experience_score(
                candidate.years_of_experience,
                job.minimum_experience
            )
        )

        # ==========================================
        # Education Score
        # ==========================================

        education_score = (
            self.education_service.calculate_score(
                candidate.education
            )
        )

        # ==========================================
        # Career Relevance
        # ==========================================

        if career_relevance_score is None:
            career_score = (
                self.career_relevance_service.calculate_score(
                    candidate.career_history,
                    job_embedding
                )
            )
        else:
            career_score = career_relevance_score

        # ==========================================
        # Redrob Score
        # ==========================================

        redrob_score = (
            self.redrob_service.calculate_score(
                candidate.redrob_signals
            )
        )

        # ==========================================
        # Company Score
        # ==========================================

        company_score = (
            self.company_service.calculate_score(
                candidate.current_company
            )
        )

        # ==========================================
        # Notice Period Score
        # ==========================================

        notice_score = (
            self.notice_service.calculate_score(
                candidate.redrob_signals
            )
        )

        # ==========================================
        # Location Score
        # ==========================================

        location_score = (
            self.location_service.calculate_score(
                candidate.location
            )
        )

        # ==========================================
        # Semantic Similarity
        # ==========================================

        semantic_score = (
            self.career_relevance_service.semantic_service.similarity(
                candidate_embedding,
                job_embedding
            )
        )

        # ==========================================
        # BM25 Score
        # ==========================================

        bm25_score = (
            self.bm25_service.score(
                job_text=job.description,
                semantic_service=semantic_service,
                candidate_index=candidate_index,
            )
        )

        # ==========================================
        # Final Hybrid Score
        # ==========================================

        final_score = (
            self.ranking_service.calculate_hybrid_score(
                skill_score,
                experience_score,
                education_score,
                career_score,
                redrob_score,
                semantic_score,
                bm25_score,
                company_score,
                notice_score,
                location_score
            )
        )

        return {

            "candidate": candidate,

            "candidate_document": candidate_document,

            "matched_skills": matched_skills,

            "skill_score": skill_score,

            "experience_score": experience_score,

            "education_score": education_score,

            "career_relevance": career_score,

            "redrob_score": redrob_score,

            "company_score": company_score,

            "notice_score": notice_score,

            "location_score": location_score,

            "semantic_score": semantic_score,

            "bm25_score": bm25_score,

            "final_score": round(final_score, 2)

        }