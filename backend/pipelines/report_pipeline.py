from backend.services.report_service import ReportService
from backend.services.career_service import CareerService


class ReportPipeline:

    def __init__(self):

        self.report_service = ReportService()

        self.career_service = CareerService()

    # ==========================================
    # Print Top Candidates
    # ==========================================

    def print_top_candidates(
        self,
        ranked_candidates
    ):

        print("\n")
        print("=" * 70)
        print("TOP 100 CANDIDATES")
        print("=" * 70)

        for i, result in enumerate(
            ranked_candidates,
            start=1
        ):

            candidate = result["candidate"]

            print(

                f"{i:3d}. "

                f"{candidate.name:25} "

                f"{candidate.current_title:30} "

                f"Score : {result['final_score']}"

            )

    # ==========================================
    # Print Best Candidate
    # ==========================================

    def print_best_candidate(

        self,

        ranked_candidates,

        candidate_ranker,

        job

    ):

        if not ranked_candidates:

            return

        best = ranked_candidates[0]

        candidate = best["candidate"]

        company_type = (

            self.career_service.company_type(

                candidate.current_company

            )

        )

        career_experience = (

            self.career_service.calculate_total_experience(

                candidate.career_history

            )

        )

        current_company = (

            self.career_service.current_company(

                candidate.career_history

            )

        )

        current_role = (

            self.career_service.current_role(

                candidate.career_history

            )

        )

        total_jobs = (

            self.career_service.total_jobs(

                candidate.career_history

            )

        )

        average_job_duration = (

            self.career_service.average_job_duration(

                candidate.career_history

            )

        )

        candidate_skills = (

            candidate_ranker.skill_service.extract_skills(

                candidate.summary

            )

        )

        job_skills = (

            candidate_ranker.skill_service.extract_skills(

                job.description

            )

        )

        print("\n")
        print("=" * 70)
        print("BEST CANDIDATE REPORT")
        print("=" * 70)

        self.report_service.print_candidate(

            candidate,

            company_type,

            career_experience,

            current_company,

            current_role,

            total_jobs,

            average_job_duration,

            candidate_skills,

            job_skills,

            best["matched_skills"],

            best["skill_score"],

            best["experience_score"],

            best["education_score"],

            best["career_relevance"],

            best["redrob_score"],

            best["semantic_score"],

            best["bm25_score"],

            best["final_score"],

            best["candidate_document"],

            job,

            best["company_score"],

            best["notice_score"],

            best["location_score"]

        )