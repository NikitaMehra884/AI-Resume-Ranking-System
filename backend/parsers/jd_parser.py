from pathlib import Path
from docx import Document


def read_job_description():

    project_root = Path(__file__).resolve().parents[2]

    file_path = project_root / "data" / "dataset" / "job_description.docx"

    document = Document(file_path)

    print("=" * 70)
    print("JOB DESCRIPTION")
    print("=" * 70)

    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            print(paragraph.text)


if __name__ == "__main__":
    read_job_description()