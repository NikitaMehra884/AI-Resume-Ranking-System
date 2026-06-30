import numpy as np
from rank_bm25 import BM25Okapi


class BM25Service:

    def __init__(self):

        self.bm25 = None
        self.candidate_documents = None
        self.doc_to_index = None
        self.job_score_cache = {}

    # ==========================================
    # Tokenizer
    # ==========================================

    def tokenize(self, text):

        if not text:
            return []

        return text.lower().split()

    # ==========================================
    # Ensure BM25 corpus built (candidate documents)
    # ==========================================

    def ensure_corpus(self, semantic_service):

        if self.bm25 is not None:
            return

        # Lazy import to avoid cycles
        if self.candidate_documents is None:
            self.candidate_documents = semantic_service.load_candidate_documents()

        tokenized = [self.tokenize(d) for d in self.candidate_documents]

        self.bm25 = BM25Okapi(tokenized)

        # build document -> index mapping
        self.doc_to_index = {d: i for i, d in enumerate(self.candidate_documents)}

    # ==========================================
    # Build and cache scores for a job
    # ==========================================

    def build_job_scores(self, job_text, semantic_service):

        if job_text in self.job_score_cache:
            return

        self.ensure_corpus(semantic_service)

        query = self.tokenize(job_text)

        scores = np.array(self.bm25.get_scores(query), dtype="float32")
        scores = np.maximum(scores, 0.0)

        if scores.size == 0:
            normalized = np.zeros_like(scores)
        else:
            max_score = float(np.max(scores))
            if max_score <= 0:
                normalized = np.zeros_like(scores)
            else:
                normalized = (scores / max_score) * 100.0

        self.job_score_cache[job_text] = normalized.tolist()

    # ==========================================
    # Score Candidate (uses cached job scores)
    # ==========================================

    def score(self, candidate_document=None, job_text=None, semantic_service=None, candidate_index=None):

        if semantic_service is None:
            raise ValueError("semantic_service is required for BM25Service.score")

        if job_text is None:
            raise ValueError("job_text is required for BM25Service.score")

        self.build_job_scores(job_text, semantic_service)

        if candidate_index is not None:
            if 0 <= candidate_index < len(self.job_score_cache[job_text]):
                return round(self.job_score_cache[job_text][candidate_index], 4)
            return 0.0

        if candidate_document is None:
            return 0.0

        idx = self.doc_to_index.get(candidate_document)

        if idx is None:
            return 0.0

        score = self.job_score_cache[job_text][idx]

        return round(score, 4)