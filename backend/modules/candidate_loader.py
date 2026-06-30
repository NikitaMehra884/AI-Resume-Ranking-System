import json
import pickle
from pathlib import Path

from backend.models.candidate import Candidate


class CandidateLoader:

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.file_path = (
            self.project_root
            / "data"
            / "dataset"
            / "candidates.jsonl"
        )

        print("\nLoading Candidates From:")
        print(self.file_path)
        self.cache_dir = self.project_root / "cache"
        self.cache_dir.mkdir(exist_ok=True)

        self.offsets_file = self.cache_dir / "candidate_offsets.pkl"

    # ============================================
    # Batch Generator (Used for Precompute)
    # ============================================

    def load_candidate_batches(
        self,
        batch_size=512
    ):

        batch = []

        total = 0

        with open(
            self.file_path,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:

                if not line.strip():
                    continue

                item = json.loads(line)

                batch.append(
                    self._build_candidate(item)
                )

                total += 1

                if len(batch) == batch_size:

                    yield batch

                    batch = []

        if batch:

            yield batch

        print(
            f"\nTotal Candidates Loaded : {total}"
        )

    # ============================================
    # Load Only Required Candidate IDs
    # ============================================

    def load_candidates_by_ids(
        self,
        candidate_ids
    ):
        # optimized loading using byte offsets (built once)
        candidate_ids = list(candidate_ids)

        offsets = self._load_offset_index()

        ids_and_offsets = [
            (cid, offsets.get(cid))
            for cid in candidate_ids
        ]

        ids_and_offsets = [
            (cid, off)
            for cid, off in ids_and_offsets
            if off is not None
        ]

        ids_and_offsets.sort(key=lambda item: item[1])

        candidates_by_id = {}

        with open(self.file_path, "rb") as f:

            for cid, off in ids_and_offsets:

                f.seek(off)
                line = f.readline()

                try:
                    item = json.loads(line.decode("utf-8"))
                except Exception:
                    continue

                candidates_by_id[cid] = self._build_candidate(item)

        return [
            candidates_by_id[cid]
            for cid in candidate_ids
            if cid in candidates_by_id
        ]

    # ============================================
    # Build / Load Offset Index
    # ============================================

    def _load_offset_index(self):

        if self.offsets_file.exists():

            with open(self.offsets_file, "rb") as fh:

                return pickle.load(fh)

        return self._build_offset_index()

    def _build_offset_index(self):

        offsets = {}

        with open(self.file_path, "rb") as f:

            while True:
                pos = f.tell()
                line = f.readline()
                if not line:
                    break

                try:
                    item = json.loads(line.decode("utf-8"))
                    cid = item.get("candidate_id")
                    if cid:
                        offsets[cid] = pos
                except Exception:
                    continue

        with open(self.offsets_file, "wb") as fh:
            pickle.dump(offsets, fh)

        return offsets
        # ============================================
    # Candidate Builder
    # ============================================

    def _build_candidate(self, item):

        profile = item.get("profile", {})

        skills = [

            skill.get("name", "")

            for skill in item.get(
                "skills",
                []
            )

            if skill.get("name")
        ]

        return Candidate(

            candidate_id=item.get(
                "candidate_id",
                ""
            ),

            name=profile.get(
                "anonymized_name",
                "Unknown"
            ),

            years_of_experience=profile.get(
                "years_of_experience",
                0
            ),

            current_title=profile.get(
                "current_title",
                ""
            ),

            current_company=profile.get(
                "current_company",
                ""
            ),

            location=profile.get(
                "location",
                ""
            ),

            country=profile.get(
                "country",
                ""
            ),

            summary=profile.get(
                "summary",
                ""
            ),

            skills=skills,

            career_history=item.get(
                "career_history",
                []
            ),

            education=item.get(
                "education",
                []
            ),

            certifications=item.get(
                "certifications",
                []
            ),

            languages=item.get(
                "languages",
                []
            ),

            redrob_signals=item.get(
                "redrob_signals",
                {}
            )

        )