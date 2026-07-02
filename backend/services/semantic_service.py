import os
import pickle
from pathlib import Path

import numpy as np
import torch

from sentence_transformers import SentenceTransformer


class SemanticService:

    # class-level singletons to ensure only one model/index is loaded
    _model = None

    _candidate_embeddings = None
    _candidate_ids = None
    _candidate_documents = None

    def __init__(self):

        self.project_root = Path(__file__).resolve().parents[2]

        self.project_cache_dir = self.project_root / "cache"
        self.project_cache_dir.mkdir(parents=True, exist_ok=True)

        hf_home = Path(os.environ.get("HF_HOME") or (Path.home() / ".cache" / "huggingface"))
        self.cache_dir = hf_home
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.model_cache_dir = self.cache_dir / "hub"
        self.model_cache_dir.mkdir(parents=True, exist_ok=True)

        os.environ.setdefault("HF_HUB_OFFLINE", "1")
        os.environ.setdefault("HF_HOME", str(self.cache_dir))
        os.environ.setdefault("TRANSFORMERS_CACHE", str(self.cache_dir / "transformers"))

    def _load_model(self):
        if SemanticService._model is None:
            print("\nLoading Semantic Model (CPU, local cache only)...")
            model_kwargs = {
                "device": "cpu",
                "local_files_only": True,
                "cache_folder": str(self.model_cache_dir),
            }

            SemanticService._model = SentenceTransformer(
                "all-MiniLM-L6-v2",
                **model_kwargs,
            )
            SemanticService._model.max_seq_length = 256

        return SemanticService._model

    # ==========================================
    # Single Embedding
    # ==========================================

    def embedding(self, text):

        if not text:
            text = ""

        model = self._load_model()

        with torch.inference_mode():

            return model.encode(

                text,

                convert_to_numpy=True,

                normalize_embeddings=True,

                show_progress_bar=False

            )

    # ==========================================
    # Batch Embedding
    # ==========================================

    def batch_embedding(self, texts):

        if not texts:
            return []

        model = self._load_model()

        with torch.inference_mode():

            return model.encode(

                texts,

                batch_size=256,

                convert_to_numpy=True,

                normalize_embeddings=True,

                show_progress_bar=False

            )

    # ==========================================
    # Cosine Similarity
    # ==========================================

    def similarity(
        self,
        embedding1,
        embedding2
    ):

        score = float(np.dot(
            embedding1,
            embedding2
        ))

        return round(score, 4)

    # ==========================================
    # Cached Embeddings
    # ==========================================

    def load_candidate_embeddings(self):

        if SemanticService._candidate_embeddings is None:

            print("\nLoading Cached Embeddings...")

            SemanticService._candidate_embeddings = np.load(

                self.project_cache_dir
                / "candidate_embeddings.npy"

            )

        return SemanticService._candidate_embeddings

    def get_candidate_embedding_by_index(self, index):

        embeddings = self.load_candidate_embeddings()

        return embeddings[int(index)]

    # ==========================================
    # Candidate IDs
    # ==========================================

    def load_candidate_ids(self):

        if SemanticService._candidate_ids is None:

            with open(

                self.project_cache_dir
                / "candidate_ids.pkl",

                "rb"

            ) as file:

                SemanticService._candidate_ids = (

                    pickle.load(file)

                )

        return SemanticService._candidate_ids

    # ==========================================
    # Candidate Documents
    # ==========================================

    def load_candidate_documents(self):

        if SemanticService._candidate_documents is None:

            with open(

                self.project_cache_dir
                / "candidate_documents.pkl",

                "rb"

            ) as file:

                SemanticService._candidate_documents = (

                    pickle.load(file)

                )

        return SemanticService._candidate_documents