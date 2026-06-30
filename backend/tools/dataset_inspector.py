from pathlib import Path
import zipfile


def inspect_dataset():
    project_root = Path(__file__).resolve().parents[2]

    dataset_path = project_root / "data" / "[PUB] India_runs_data_and_ai_challenge.zip"

    print("=" * 70)
    print("AI Resume Ranking System")
    print("Dataset Inspector")
    print("=" * 70)

    print(f"\nDataset Path:\n{dataset_path}")

    if not dataset_path.exists():
        print("\n❌ Dataset not found.")
        return

    print("\n✅ Dataset Found")

    with zipfile.ZipFile(dataset_path, "r") as zip_file:

        print("\nFiles inside ZIP:\n")

        for file in zip_file.namelist():
            print(file)


if __name__ == "__main__":
    inspect_dataset()