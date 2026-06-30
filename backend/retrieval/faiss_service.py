import pickle
from pathlib import Path

import faiss
import numpy as np


class FAISSService:

    # class-level cache to ensure index and ids loaded once
    _index = None
    _candidate_ids = None

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.cache_dir = (
            self.project_root
            / "cache"
        )

        self.embedding_file = (
            self.cache_dir
            / "candidate_embeddings.npy"
        )

        self.candidate_ids_file = (
            self.cache_dir
            / "candidate_ids.pkl"
        )

        self.index_file = (
            self.cache_dir
            / "candidate.index"
        )

    # ==========================================
    # Load Candidate Embeddings
    # ==========================================

    def load_embeddings(self):

        embeddings = np.load(
            self.embedding_file
        ).astype("float32")

        return embeddings

    # ==========================================
    # Load Candidate IDs
    # ==========================================

    def load_candidate_ids(self):
        if FAISSService._candidate_ids is None:

            with open(
                self.candidate_ids_file,
                "rb"
            ) as file:

                FAISSService._candidate_ids = pickle.load(
                    file
                )

        return FAISSService._candidate_ids

    # ==========================================
    # Build FAISS Index
    # ==========================================

    def build_index(self):

        embeddings = self.load_embeddings()

        dimension = embeddings.shape[1]

        FAISSService._index = faiss.IndexFlatIP(dimension)
        FAISSService._index.add(embeddings)

        print(f"Indexed : {FAISSService._index.ntotal}")
            # ==========================================
    # Save Index
    # ==========================================

    def save_index(self):

        if FAISSService._index is None:
            raise ValueError("Index has not been created.")

        faiss.write_index(FAISSService._index, str(self.index_file))

        print("\nFAISS Index Saved")
        print(self.index_file)

    # ==========================================
    # Load Index
    # ==========================================

    def load_index(self):
        if FAISSService._index is None:

            # If saved index doesn't exist, build from embeddings
            if not self.index_file.exists():
                print("FAISS index file missing; building index from embeddings...")
                self.build_index()
                self.save_index()

            FAISSService._index = faiss.read_index(str(self.index_file))

        return FAISSService._index

    # ==========================================
    # Search Top Candidates
    # ==========================================

    def search_candidates(
        self,
        job_embedding,
        top_k=1500
    ):
        # ensure index is loaded (class-level singleton)
        index = self.load_index()
        candidate_ids = self.load_candidate_ids()

        query = np.asarray([job_embedding], dtype="float32")

        scores, indices = index.search(query, top_k)

        results = []

        for idx, score in zip(indices[0], scores[0]):
            if idx == -1:
                continue

            results.append({
                "candidate_id": candidate_ids[int(idx)],
                "embedding_index": int(idx),
                "semantic_score": float(score),
            })

        return results


# ==========================================
# Build FAISS Index
# ==========================================

def main():

    service = FAISSService()

    service.build_index()

    service.save_index()

    print("\nFAISS Index Generated Successfully")


if __name__ == "__main__":

    main()