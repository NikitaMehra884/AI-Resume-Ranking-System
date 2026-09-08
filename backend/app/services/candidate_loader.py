import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional
from backend.app.core.config import settings

class CandidateLoader:
    """Unified candidate provider supporting random-access offset retrieval from 100,000 JSONL dataset, DB, and sample cache."""

    def __init__(self):
        self.offsets_file = settings.CANDIDATE_OFFSETS_PATH
        self.jsonl_file = settings.CANDIDATES_JSONL_PATH
        self.sample_file = settings.SAMPLE_CANDIDATES_PATH
        self._offsets: Optional[Dict[str, int]] = None
        self._sample_cache: Optional[Dict[str, Dict[str, Any]]] = None

    def _ensure_offsets(self):
        if self._offsets is None:
            if self.offsets_file.exists():
                with open(self.offsets_file, "rb") as f:
                    self._offsets = pickle.load(f)
            else:
                self._offsets = {}

    def _ensure_sample_cache(self):
        if self._sample_cache is None:
            if self.sample_file.exists():
                with open(self.sample_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._sample_cache = {item["candidate_id"]: item for item in data}
            else:
                self._sample_cache = {}

    def load_candidates_by_ids(self, candidate_ids: List[str]) -> List[Dict[str, Any]]:
        if not candidate_ids:
            return []

        self._ensure_offsets()
        results = {}

        # 1. Try fast byte-offset reading if candidates.jsonl and offsets exist
        if self._offsets and self.jsonl_file.exists():
            seek_pairs = [(cid, self._offsets[cid]) for cid in candidate_ids if cid in self._offsets]
            seek_pairs.sort(key=lambda x: x[1])

            with open(self.jsonl_file, "rb") as f:
                for cid, offset in seek_pairs:
                    f.seek(offset)
                    line = f.readline()
                    try:
                        item = json.loads(line.decode("utf-8"))
                        results[cid] = self._normalize_record(item)
                    except Exception:
                        continue

        # 2. Check sample cache for any missing
        missing_ids = [cid for cid in candidate_ids if cid not in results]
        if missing_ids:
            self._ensure_sample_cache()
            for cid in missing_ids:
                if cid in self._sample_cache:
                    results[cid] = self._normalize_record(self._sample_cache[cid])

        # Return in requested order
        return [results[cid] for cid in candidate_ids if cid in results]

    def _normalize_record(self, item: Dict[str, Any]) -> Dict[str, Any]:
        profile = item.get("profile", {})
        skills = item.get("skills", [])
        clean_skills = [s.get("name", "") if isinstance(s, dict) else str(s) for s in skills]

        return {
            "candidate_id": item.get("candidate_id", ""),
            "name": profile.get("anonymized_name", item.get("full_name", "Candidate")),
            "full_name": profile.get("anonymized_name", item.get("full_name", "Candidate")),
            "headline": profile.get("headline", ""),
            "summary": profile.get("summary", ""),
            "years_of_experience": float(profile.get("years_of_experience", 0.0)),
            "current_title": profile.get("current_title", ""),
            "current_company": profile.get("current_company", ""),
            "current_industry": profile.get("current_industry", ""),
            "location": profile.get("location", ""),
            "country": profile.get("country", ""),
            "skills": clean_skills,
            "career_history": item.get("career_history", []),
            "education": item.get("education", []),
            "redrob_signals": item.get("redrob_signals", {})
        }
