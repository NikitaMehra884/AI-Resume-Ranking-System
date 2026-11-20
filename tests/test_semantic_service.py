from pathlib import Path
import numpy as np
from backend.app.embeddings import semantic_service

class DummyModel:
    def __init__(self, *args, **kwargs):
        self.max_seq_length = None

    def encode(self, text, **kwargs):
        return np.array([0.1, 0.2], dtype="float32")

def test_semantic_service_uses_singleton(monkeypatch):
    calls = []

    class FakeSentenceTransformer(DummyModel):
        def __init__(self, name, device="cpu", **kwargs):
            super().__init__(name, device, **kwargs)
            calls.append((name, device, kwargs))

    monkeypatch.setattr(semantic_service, "SentenceTransformer", FakeSentenceTransformer)
    semantic_service.SemanticService._instance = None
    semantic_service.SemanticService._model = None

    service = semantic_service.SemanticService()
    emb1 = service.embedding("hello")
    emb2 = service.embedding("world")

    assert len(calls) == 1
    assert calls[0][0] == "all-MiniLM-L6-v2"
    assert calls[0][1] == "cpu"
    assert isinstance(emb1, np.ndarray)
    assert isinstance(emb2, np.ndarray)
