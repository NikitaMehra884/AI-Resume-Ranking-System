import os
import threading
from pathlib import Path
from typing import List
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from backend.app.core.config import settings

class SemanticService:
    """Thread-safe singleton service for computing sentence embeddings and cosine similarities."""
    _instance = None
    _lock = threading.Lock()
    _model = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SemanticService, cls).__new__(cls)
        return cls._instance

    def _get_model(self) -> SentenceTransformer:
        if self._model is None:
            with self._lock:
                if self._model is None:
                    cache_folder = settings.CACHE_DIR / "sentence_transformers"
                    cache_folder.mkdir(parents=True, exist_ok=True)
                    try:
                        self._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu", cache_folder=str(cache_folder))
                    except Exception:
                        self._model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
                    self._model.max_seq_length = 256
        return self._model

    def embedding(self, text: str) -> np.ndarray:
        if not text:
            text = ""
        model = self._get_model()
        with torch.inference_mode():
            emb = model.encode(text, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
        return emb.astype("float32")

    def batch_embedding(self, texts: List[str], batch_size: int = 128) -> np.ndarray:
        if not texts:
            return np.empty((0, 384), dtype="float32")
        model = self._get_model()
        with torch.inference_mode():
            embs = model.encode(texts, batch_size=batch_size, convert_to_numpy=True, normalize_embeddings=True, show_progress_bar=False)
        return embs.astype("float32")

    def similarity(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        sim = float(np.dot(emb1, emb2))
        return max(0.0, min(1.0, sim))
