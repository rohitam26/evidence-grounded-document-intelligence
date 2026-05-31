import re
from typing import List, Dict, Any, Tuple
from app.core.logging import logger

class CrossEncoderReranker:
    """Reranker implementing lexical-semantic cross-scoring and BGE cross-encoder interfaces."""

    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
        self.model_name = model_name
        self._model = None
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import CrossEncoder
            self._model = CrossEncoder(self.model_name)
            logger.info(f"Loaded CrossEncoder: {self.model_name}")
        except Exception:
            self._model = None

    def rerank(self, query: str, candidate_chunks: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Rerank candidates based on deep cross-encoder or lexical-alignment score."""
        if not candidate_chunks:
            return []

        if self._model is not None:
            try:
                pairs = [[query, c["content"]] for c in candidate_chunks]
                scores = self._model.predict(pairs)
                for i, score in enumerate(scores):
                    candidate_chunks[i]["score"] = float(score)
                    candidate_chunks[i]["retrieval_method"] = "bge_cross_encoder"
                ranked = sorted(candidate_chunks, key=lambda x: x["score"], reverse=True)
                return ranked[:top_k]
            except Exception as e:
                logger.warning(f"CrossEncoder inference failed ({e}); falling back to alignment reranking.")

        # Lexical and position-weighted cross-alignment scoring
        query_terms = set(re.findall(r"\w+", query.lower()))
        scored_candidates = []

        for c in candidate_chunks:
            doc_name = str(c.get("document_name", "")).lower()
            heading = str(c.get("section_heading", "")).lower()
            content = str(c.get("content", "")).lower()
            text = f"{doc_name} {heading} {content}"
            content_terms = re.findall(r"\w+", text)
            total_terms = len(content_terms)
            if total_terms == 0:
                continue

            # Query term coverage
            matched_terms = [t for t in query_terms if t in text]
            term_coverage = len(matched_terms) / max(len(query_terms), 1)

            # Exact phrase match bonus
            phrase_bonus = 0.3 if query.lower() in text else 0.0

            # Heading relevance bonus
            heading_bonus = 0.2 if any(t in heading for t in query_terms if len(t) > 3) else 0.0

            # Document name match bonus
            doc_bonus = 0.35 if any(t in doc_name for t in query_terms if len(t) > 3) else 0.0

            # Combined reranking score
            base_score = float(c.get("score", 0.5))
            rerank_score = (0.45 * term_coverage) + (0.2 * base_score) + phrase_bonus + heading_bonus + doc_bonus

            item = dict(c)
            item["score"] = round(rerank_score, 4)
            item["retrieval_method"] = "reranked_hybrid"
            scored_candidates.append(item)

        scored_candidates.sort(key=lambda x: x["score"], reverse=True)
        return scored_candidates[:top_k]

reranker = CrossEncoderReranker()
