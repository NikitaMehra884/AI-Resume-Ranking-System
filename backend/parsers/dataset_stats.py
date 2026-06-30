import json
from pathlib import Path


def dataset_statistics():

    project_root = Path(__file__).resolve().parents[2]

    file_path = project_root / "data" / "dataset" / "candidates.jsonl"

    total = 0

    with open(file_path, "r", encoding="utf-8") as file:

        for line in file:
            json.loads(line)
            total += 1

    print("=" * 70)
    print("DATASET STATISTICS")
    print("=" * 70)

    print(f"Total Candidates : {total}")


if __name__ == "__main__":
    dataset_statistics()