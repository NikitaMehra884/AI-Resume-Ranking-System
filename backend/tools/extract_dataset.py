from pathlib import Path
import zipfile


def extract_dataset():
    project_root = Path(__file__).resolve().parents[2]

    data_folder = project_root / "data"

    zip_file = next(data_folder.glob("*.zip"))

    extract_folder = data_folder / "dataset"

    if extract_folder.exists():
        print("✅ Dataset already extracted.")
        return

    print("Extracting dataset...")

    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(extract_folder)

    print("✅ Extraction Completed.")


if __name__ == "__main__":
    extract_dataset()