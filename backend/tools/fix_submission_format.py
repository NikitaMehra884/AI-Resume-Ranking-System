import csv
from pathlib import Path


def normalize_submission(in_path, out_path, top_n=None):
    in_path = Path(in_path)
    out_path = Path(out_path)

    if not in_path.exists():
        print(f"Input file not found: {in_path}")
        return

    rows = []

    with in_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            # keep only required columns
            cid = r.get("candidate_id") or r.get("candidate") or r.get("id")
            rank = r.get("rank")
            score = r.get("score")
            reasoning = r.get("reasoning") or r.get("reason") or ""

            if cid is None or rank is None or score is None:
                continue

            try:
                score_f = float(score)
            except Exception:
                score_f = 0.0

            rows.append((cid, int(rank), score_f, reasoning.strip()))

    # sort by rank
    rows.sort(key=lambda x: x[1])

    if top_n:
        rows = rows[:top_n]

    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for cid, rank, score_f, reasoning in rows:
            writer.writerow([cid, rank, f"{score_f:.4f}", reasoning])

    print(f"Normalized submission written to: {out_path}")


if __name__ == "__main__":
    in_file = Path(__file__).resolve().parents[2] / "backend" / "outputs" / "submission.csv"
    out_file = in_file
    normalize_submission(in_file, out_file, top_n=None)
