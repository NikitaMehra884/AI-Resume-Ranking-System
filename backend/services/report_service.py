class ReportService:

    def print_candidate(
        self,
        candidate,
        company_type,
        career_experience,
        current_company,
        current_role,
        total_jobs,
        average_job_duration,
        candidate_skills,
        job_skills,
        matched_skills,
        skill_score,
        experience_score,
        education_score,
        career_relevance,
        redrob_score,
        semantic_score,
        bm25_score,
        final_score,
        candidate_document,
        job,
        company_score=0,
        notice_score=0,
        location_score=0
    ):

        print("=" * 70)
        print("AI Resume Ranking System")
        print("=" * 70)

        print(f"Job Title              : {job.title}")
        print(f"Minimum Experience     : {job.minimum_experience} Years")

        print("\nCandidate Information")
        print("-" * 70)
        print(f"Candidate ID           : {candidate.candidate_id}")
        print(f"Name                   : {candidate.name}")
        print(f"Current Role           : {candidate.current_title}")
        print(f"Current Company        : {candidate.current_company}")
        print(f"Company Type           : {company_type}")
        print(f"Experience             : {candidate.years_of_experience} Years")
        print(f"Location               : {candidate.location}, {candidate.country}")

        print("\nCareer Information")
        print("-" * 70)
        print(f"Career Experience      : {career_experience:.2f} Years")
        print(f"Current Company        : {current_company}")
        print(f"Current Role           : {current_role}")
        print(f"Total Jobs             : {total_jobs}")
        print(f"Average Job Duration   : {average_job_duration:.2f} Months")

        print("\nCandidate Skills")
        print("-" * 70)
        print(candidate.skills)

        print("\nExtracted Skills")
        print("-" * 70)
        print(candidate_skills)

        print("\nJob Skills")
        print("-" * 70)
        print(job_skills)

        print("\nMatched Skills")
        print("-" * 70)
        print(matched_skills)

        print("\nScore Breakdown")
        print("-" * 70)
        print(f"Skill Score            : {skill_score}")
        print(f"Experience Score       : {experience_score}")
        print(f"Education Score        : {education_score}")
        print(f"Career Relevance       : {career_relevance}")
        print(f"Redrob Score           : {redrob_score}")
        print(f"Company Score          : {company_score}")
        print(f"Notice Period Score    : {notice_score}")
        print(f"Location Score         : {location_score}")
        print(f"Semantic Score         : {semantic_score}")
        print(f"BM25 Score             : {bm25_score}")

        print("-" * 70)
        print(f"FINAL AI SCORE         : {final_score}")
        print("-" * 70)

        print("\nCandidate Document")
        print("-" * 70)
        print(candidate_document)