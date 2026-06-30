class DocumentBuilder:
    """
    Builds a rich candidate document for:

    - Semantic Search
    - BM25
    - LLM Ranking
    """

    def build_candidate_document(self, candidate):

        sections = []

        # =====================================
        # Basic Information
        # =====================================

        sections.append(f"Candidate Name: {candidate.name}")

        sections.append(
            f"Current Role: {candidate.current_title}"
        )

        sections.append(
            f"Current Company: {candidate.current_company}"
        )

        sections.append(
            f"Experience: {candidate.years_of_experience} years"
        )

        sections.append(
            f"Location: {candidate.location}, {candidate.country}"
        )

        # =====================================
        # Professional Summary
        # =====================================

        if candidate.summary:

            sections.append("\nProfessional Summary")

            sections.append(candidate.summary)

        # =====================================
        # Skills
        # =====================================

        if candidate.skills:

            sections.append("\nSkills")

            sections.append(
                ", ".join(candidate.skills)
            )

        # =====================================
        # Career History
        # =====================================

        if candidate.career_history:

            sections.append("\nCareer History")

            for job in candidate.career_history:

                company = job.get(
                    "company",
                    ""
                )

                title = job.get(
                    "title",
                    ""
                )

                description = job.get(
                    "description",
                    ""
                )

                duration = job.get(
                    "duration_months",
                    ""
                )

                sections.append(
                    f"{title} at {company}"
                )

                sections.append(
                    f"Duration: {duration} months"
                )

                sections.append(
                    description
                )

        # =====================================
        # Education
        # =====================================

        if candidate.education:

            sections.append("\nEducation")

            for edu in candidate.education:

                degree = edu.get(
                    "degree",
                    ""
                )

                field = edu.get(
                    "field_of_study",
                    ""
                )

                institute = edu.get(
                    "institution",
                    ""
                )

                grade = edu.get(
                    "grade",
                    ""
                )

                sections.append(
                    f"{degree} in {field}"
                )

                sections.append(
                    institute
                )

                sections.append(
                    grade
                )

        # =====================================
        # Certifications
        # =====================================

        if candidate.certifications:

            sections.append("\nCertifications")

            for cert in candidate.certifications:

                if isinstance(cert, dict):

                    sections.append(
                        cert.get("name", "")
                    )

                else:

                    sections.append(str(cert))

        # =====================================
        # Languages
        # =====================================

        if candidate.languages:

            sections.append("\nLanguages")

            for language in candidate.languages:

                if isinstance(language, dict):

                    sections.append(
                        f"{language.get('language')} ({language.get('proficiency')})"
                    )

        return "\n".join(sections)