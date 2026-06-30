import json
from pathlib import Path


def read_first_candidate():

    project_root = Path(__file__).resolve().parents[2]

    file_path = project_root / "data" / "dataset" / "candidates.jsonl"

    with open(file_path, "r", encoding="utf-8") as file:

        first_line = file.readline()

        candidate = json.loads(first_line)

    print("=" * 70)
    print("FIRST REAL CANDIDATE")
    print("=" * 70)

    print("Candidate ID :", candidate["candidate_id"])
    print("Name         :", candidate["profile"]["anonymized_name"])
    print("Experience   :", candidate["profile"]["years_of_experience"])
    print("Current Role :", candidate["profile"]["current_title"])
    print("Company      :", candidate["profile"]["current_company"])


if __name__ == "__main__":
    read_first_candidate()