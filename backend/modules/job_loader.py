from pathlib import Path

from backend.models.job import Job
from backend.services.job_service import JobService


class JobLoader:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.file_path = (
            self.project_root
            / "data"
            / "dataset"
            / "job_description.docx"
        )

    def load_job(self):

        description = ""

        # Try to use python-docx if available, otherwise fallback to plain text
        try:
            from docx import Document

            document = Document(self.file_path)

            for paragraph in document.paragraphs:

                if paragraph.text.strip():

                    description += paragraph.text + "\n"

        except Exception:

            # Fallback: try to read a .txt version of the job description
            txt_path = self.file_path.with_suffix(".txt")

            if txt_path.exists():

                with open(txt_path, "r", encoding="utf-8") as f:

                    description = f.read()

            else:

                raise

        job_service = JobService()

        minimum_experience = job_service.extract_experience(description)

        return Job(
            title="AI Resume Ranking Challenge",
            description=description,
            required_skills=[],
            preferred_skills=[],
            minimum_experience=minimum_experience,
        )