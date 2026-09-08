import pickle
import threading
from typing import List, Dict, Any, Optional
import faiss
import numpy as np
from backend.app.core.config import settings

class FAISSService:
    """Thread-safe FAISS vector index wrapper for candidate dense retrieval."""
    _instance = None
    _lock = threading.Lock()
    _index = None
    _candidate_ids: Optional[List[str]] = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(FAISSService, cls).__new__(cls)
        return cls._instance

    def _ensure_loaded(self):
        if self._index is None or self._candidate_ids is None:
            with self._lock:
                if self._index is None:
                    if settings.FAISS_INDEX_PATH.exists():
                        self._index = faiss.read_index(str(settings.FAISS_INDEX_PATH))
                    elif settings.EMBEDDINGS_PATH.exists():
                        embs = np.load(settings.EMBEDDINGS_PATH).astype("float32")
                        dim = embs.shape[1]
                        self._index = faiss.IndexFlatIP(dim)
                        self._index.add(embs)
                        faiss.write_index(self._index, str(settings.FAISS_INDEX_PATH))
                    else:
                        self._index = faiss.IndexFlatIP(384)

                if self._candidate_ids is None:
                    if settings.CANDIDATE_IDS_PATH.exists():
                        with open(settings.CANDIDATE_IDS_PATH, "rb") as f:
                            self._candidate_ids = pickle.load(f)
                    else:
                        self._candidate_ids = []

    def search_candidates(self, query_embedding: np.ndarray, top_k: int = 1500) -> List[Dict[str, Any]]:
        self._ensure_loaded()
        if self._index.ntotal == 0 or not self._candidate_ids:
            return []

        actual_k = min(top_k, self._index.ntotal)
        query = np.asarray([query_embedding], dtype="float32")
        scores, indices = self._index.search(query, actual_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            if idx == -1 or idx >= len(self._candidate_ids):
                continue
            results.append({
                "candidate_id": self._candidate_ids[idx],
                "embedding_index": int(idx),
                "semantic_score": float(score)
            })
        return results

    def add_candidate(self, candidate_id: str, embedding: np.ndarray):
        self._ensure_loaded()
        with self._lock:
            vec = np.asarray([embedding], dtype="float32")
            self._index.add(vec)
            self._candidate_ids.append(candidate_id)
