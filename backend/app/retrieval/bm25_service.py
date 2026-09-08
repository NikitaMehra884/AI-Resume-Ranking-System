import pickle
import threading
from typing import List, Dict, Any, Optional
import numpy as np
from rank_bm25 import BM25Okapi
from backend.app.core.config import settings

STOPWORDS = {
    "the", "a", "an", "and", "or", "in", "on", "at", "to", "for", "with", "is", "are", "was", "were",
    "of", "by", "as", "from", "about", "into", "through", "during", "before", "after", "above", "below",
    "up", "down", "out", "over", "under", "again", "further", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such",
    "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now", "we", "you", "your", "they", "their", "our", "ours", "he", "she",
    "it", "his", "her", "its", "i", "me", "my", "myself", "this", "that", "these", "those", "have", "has",
    "had", "having", "do", "does", "did", "doing", "would", "could", "be", "been", "being"
}

class BM25Service:
    """Sparse lexical search service with document caching, stopword pruning, and score normalization."""
    _instance = None
    _lock = threading.Lock()
    _bm25: Optional[BM25Okapi] = None
    _candidate_ids: Optional[List[str]] = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(BM25Service, cls).__new__(cls)
        return cls._instance

    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        tokens = []
        for w in text.split():
            clean = "".join(c for c in w.lower() if c.isalnum() or c in "+#.-_")
            if len(clean) > 1 and clean not in STOPWORDS:
                tokens.append(clean)
        return tokens

    def _ensure_corpus(self):
        if self._bm25 is None:
            with self._lock:
                if self._bm25 is None:
                    cache_bm25_path = settings.CACHE_DIR / "candidate_bm25.pkl"
                    if settings.CANDIDATE_IDS_PATH.exists():
                        with open(settings.CANDIDATE_IDS_PATH, "rb") as f:
                            self._candidate_ids = pickle.load(f)

                    if cache_bm25_path.exists():
                        with open(cache_bm25_path, "rb") as f:
                            self._bm25 = pickle.load(f)
                    elif settings.CANDIDATE_DOCUMENTS_PATH.exists() and self._candidate_ids:
                        with open(settings.CANDIDATE_DOCUMENTS_PATH, "rb") as f:
                            documents = pickle.load(f)

                        tokenized_corpus = [self.tokenize(d) for d in documents]
                        self._bm25 = BM25Okapi(tokenized_corpus)
                        try:
                            with open(cache_bm25_path, "wb") as f:
                                pickle.dump(self._bm25, f, protocol=pickle.HIGHEST_PROTOCOL)
                        except Exception:
                            pass
                    else:
                        self._candidate_ids = []
                        self._bm25 = BM25Okapi([["empty"]])

    def search_candidates(self, query_text: str, top_k: int = 1500) -> List[Dict[str, Any]]:
        self._ensure_corpus()
        if not self._candidate_ids or self._bm25 is None:
            return []

        query_tokens = self.tokenize(query_text)
        if not query_tokens:
            return []

        # Deduplicate and prioritize key distinct terms (up to 30) for fast evaluation
        seen = set()
        deduped = []
        for t in query_tokens:
            if t not in seen:
                seen.add(t)
                deduped.append(t)
        query_tokens = deduped[:30]

        scores = np.array(self._bm25.get_scores(query_tokens), dtype="float32")
        scores = np.maximum(scores, 0.0)

        max_score = float(np.max(scores)) if scores.size > 0 else 0.0
        if max_score <= 0.0:
            return []

        normalized_scores = (scores / max_score) * 100.0
        actual_k = min(top_k, len(scores))
        top_indices = np.argpartition(scores, -actual_k)[-actual_k:]
        top_indices = top_indices[np.argsort(-scores[top_indices])]

        results = []
        for idx in top_indices:
            if idx < len(self._candidate_ids):
                results.append({
                    "candidate_id": self._candidate_ids[idx],
                    "bm25_score": float(normalized_scores[idx]),
                    "raw_score": float(scores[idx])
                })
        return results
