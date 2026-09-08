from typing import Any, Dict, List

class DocumentBuilder:
    """Constructs rich text documents from structured candidate records for semantic and lexical indexing."""

    def build_candidate_document(self, candidate: Any) -> str:
        if isinstance(candidate, dict):
            profile = candidate.get("profile", {})
            name = profile.get("anonymized_name", candidate.get("full_name", "Candidate"))
            title = profile.get("current_title", candidate.get("current_title", ""))
            company = profile.get("current_company", candidate.get("current_company", ""))
            yoe = profile.get("years_of_experience", candidate.get("years_of_experience", 0))
            loc = profile.get("location", candidate.get("location", ""))
            country = profile.get("country", candidate.get("country", ""))
            summary = profile.get("summary", candidate.get("summary", ""))

            raw_skills = candidate.get("skills", [])
            skills = [s.get("name", "") if isinstance(s, dict) else str(s) for s in raw_skills]
            history = candidate.get("career_history", [])
            education = candidate.get("education", [])
        else:
            name = getattr(candidate, "full_name", "Candidate")
            title = getattr(candidate, "current_title", "")
            company = getattr(candidate, "current_company", "")
            yoe = getattr(candidate, "years_of_experience", 0)
            loc = getattr(candidate, "location", "")
            country = getattr(candidate, "country", "")
            summary = getattr(candidate, "summary", "")

            raw_skills = getattr(candidate, "skills", [])
            skills = [s.name if hasattr(s, "name") else str(s) for s in raw_skills]
            history = getattr(candidate, "career_history", [])
            education = getattr(candidate, "education", [])

        sections: List[str] = [
            f"Candidate: {name}",
            f"Current Role: {title} at {company}",
            f"Total Experience: {yoe} years",
            f"Location: {loc}, {country}"
        ]

        if summary:
            sections.append(f"Professional Summary: {summary}")

        if skills:
            sections.append(f"Core Technical Skills: {', '.join(skills)}")

        if history:
            sections.append("Career History:")
            for job in history:
                j_title = job.get("title", "") if isinstance(job, dict) else getattr(job, "title", "")
                j_company = job.get("company", "") if isinstance(job, dict) else getattr(job, "company", "")
                j_desc = job.get("description", "") if isinstance(job, dict) else getattr(job, "description", "")
                j_dur = job.get("duration_months", "") if isinstance(job, dict) else getattr(job, "duration_months", "")
                sections.append(f"- {j_title} at {j_company} ({j_dur} months): {j_desc}")

        if education:
            sections.append("Education:")
            for edu in education:
                e_deg = edu.get("degree", "") if isinstance(edu, dict) else getattr(edu, "degree", "")
                e_field = edu.get("field_of_study", "") if isinstance(edu, dict) else getattr(edu, "field_of_study", "")
                e_inst = edu.get("institution", "") if isinstance(edu, dict) else getattr(edu, "institution", "")
                sections.append(f"- {e_deg} in {e_field}, {e_inst}")

        return "\n".join(sections)
