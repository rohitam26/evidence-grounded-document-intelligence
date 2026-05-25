import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    PROJECT_NAME: str = "Evidence-Grounded Document Intelligence"
    PROJECT_SUBTITLE: str = "Autonomous Document Analysis, Hybrid RAG and AI Agent System"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # Environment
    ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "papertrail-production-insecure-secret-key-change-in-prod-xyz123"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]
    
    # Storage
    STORAGE_DIR: Path = BASE_DIR / "data" / "uploads"
    SAMPLE_DOCS_DIR: Path = BASE_DIR / "data" / "sample_documents"
    EVALUATION_DIR: Path = BASE_DIR / "evaluation"
    MAX_UPLOAD_SIZE_BYTES: int = 25 * 1024 * 1024  # 25 MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".png", ".jpg", ".jpeg"]
    
    # Database (PostgreSQL with SQLite fallback)
    DATABASE_URL: str = f"sqlite:///{BASE_DIR / 'data' / 'papertrail.db'}"
    
    # Qdrant Vector Store
    QDRANT_HOST: Optional[str] = None
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str = "papertrail_chunks"
    QDRANT_PATH: Optional[str] = str(BASE_DIR / "data" / "qdrant_storage")
    
    # Redis Cache (optional)
    REDIS_URL: Optional[str] = None
    
    # Ollama Local Inference
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b-instruct"
    OLLAMA_TIMEOUT_SECONDS: float = 60.0
    MOCK_LLM_ENABLED: bool = False
    
    # Embeddings
    EMBEDDING_MODEL: str = "BAAI/bge-small-en-v1.5"
    EMBEDDING_DIM: int = 384
    
    # Chunking
    CHUNK_SIZE: int = 500  # tokens/words approx
    CHUNK_OVERLAP: int = 75
    
    # Retrieval
    RETRIEVAL_TOP_K: int = 5
    DENSE_WEIGHT: float = 0.6
    SPARSE_WEIGHT: float = 0.4
    RERANKER_ENABLED: bool = True
    MIN_CITATION_CONFIDENCE: float = 0.05

settings = Settings()
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
os.makedirs(settings.SAMPLE_DOCS_DIR, exist_ok=True)
os.makedirs(settings.EVALUATION_DIR / "results", exist_ok=True)
os.makedirs(settings.EVALUATION_DIR / "reports", exist_ok=True)
