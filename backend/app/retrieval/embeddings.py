import os
import hashlib
from typing import List
import numpy as np
from app.config import settings
from app.core.logging import logger

class EmbeddingGenerator:
    """Embedding generator with support for BGE embeddings and fallback vectorizer."""

    def __init__(self, model_name: str = settings.EMBEDDING_MODEL, dim: int = settings.EMBEDDING_DIM):
        self.model_name = model_name
        self.dim = dim
        self._model = None
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded sentence transformer: {self.model_name}")
        except Exception as e:
            logger.warning(f"SentenceTransformer not loaded ({e}); initializing deterministic embedding generator.")
            self._model = None

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate normalized dense embeddings for a list of strings."""
        if not texts:
            return []

        if self._model is not None:
            try:
                embeddings = self._model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
                return [e.tolist() for e in embeddings]
            except Exception as e:
                logger.error(f"Error generating transformer embeddings: {e}")

        # Deterministic semantic hash projection fallback (384-dim normalized vector)
        return [self._fallback_embed(t) for t in texts]

    def embed_query(self, query: str) -> List[float]:
        """Embed a single query."""
        res = self.embed_texts([query])
        return res[0] if res else [0.0] * self.dim

    def _fallback_embed(self, text: str) -> List[float]:
        """High-entropy deterministic pseudo-embedding preserving cosine similarity for similar terms."""
        words = text.lower().split()
        vec = np.zeros(self.dim, dtype=np.float32)
        for w in words:
            # Deterministic hash to dimension index
            h = int(hashlib.md5(w.encode("utf-8")).hexdigest(), 16)
            idx = h % self.dim
            sign = 1.0 if ((h >> 4) % 2 == 0) else -1.0
            vec[idx] += sign

        norm = np.linalg.norm(vec)
        if norm > 1e-6:
            vec = vec / norm
        else:
            vec[0] = 1.0
        return vec.tolist()

embedding_generator = EmbeddingGenerator()
