import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings

PROJECT_ROOT = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Recruitment Intelligence Platform"
    VERSION: str = "2.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "recruit-intelligence-secret-key-2026-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{PROJECT_ROOT}/data/platform.db")
    
    # Paths & Cache
    PROJECT_ROOT_PATH: Path = PROJECT_ROOT
    DATA_DIR: Path = PROJECT_ROOT / "data"
    CACHE_DIR: Path = PROJECT_ROOT / "cache"
    OUTPUT_DIR: Path = PROJECT_ROOT / "backend" / "outputs"
    
    FAISS_INDEX_PATH: Path = CACHE_DIR / "candidate.index"
    EMBEDDINGS_PATH: Path = CACHE_DIR / "candidate_embeddings.npy"
    CANDIDATE_IDS_PATH: Path = CACHE_DIR / "candidate_ids.pkl"
    CANDIDATE_DOCUMENTS_PATH: Path = CACHE_DIR / "candidate_documents.pkl"
    CANDIDATE_OFFSETS_PATH: Path = CACHE_DIR / "candidate_offsets.pkl"
    
    CANDIDATES_JSONL_PATH: Path = DATA_DIR / "dataset" / "candidates.jsonl"
    SAMPLE_CANDIDATES_PATH: Path = DATA_DIR / "dataset" / "sample_candidates.json"
    DEFAULT_JD_PATH: Path = DATA_DIR / "dataset" / "job_description.docx"
    
    # Phase 12: Configurable Scoring Engine Weights (Defaults sum to 1.0)
    SEMANTIC_WEIGHT: float = 0.20
    BM25_WEIGHT: float = 0.15
    REQUIRED_SKILL_WEIGHT: float = 0.25
    PREFERRED_SKILL_WEIGHT: float = 0.10
    EXPERIENCE_WEIGHT: float = 0.12
    EDUCATION_WEIGHT: float = 0.08
    CAREER_ALIGNMENT_WEIGHT: float = 0.05
    AVAILABILITY_WEIGHT: float = 0.05
    
    # Retrieval Hyperparameters
    RETRIEVAL_TOP_N: int = 1500
    DEFAULT_SHORTLIST_K: int = 20
    
    # LLM Integration (Optional, seamless offline fallback provided)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY", None)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    model_config = {"case_sensitive": True, "env_file": ".env", "extra": "ignore"}

settings = Settings()
