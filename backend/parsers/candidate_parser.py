import json
from pathlib import Path


def load_sample_candidates():
    project_root = Path(__file__).resolve().parents[2]

    file_path = project_root / "data" / "dataset" / "sample_candidates.json"

    with open(file_path, "r", encoding="utf-8") as file:
        candidates = json.load(file)

    print("=" * 70)
    print(f"Total Sample Candidates : {len(candidates)}")
    print("=" * 70)

    first = candidates[0]

    print("\nCandidate ID :", first["candidate_id"])
    print("Name         :", first["profile"]["anonymized_name"])
    print("Experience   :", first["profile"]["years_of_experience"])
    print("Current Role :", first["profile"]["current_title"])
    print("Company      :", first["profile"]["current_company"])


if __name__ == "__main__":
    load_sample_candidates()