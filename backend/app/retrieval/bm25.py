import re
from typing import List, Dict, Any, Optional
from rank_bm25 import BM25Okapi
from app.core.logging import logger

def tokenize(text: str) -> List[str]:
    """Simple alphanumeric tokenizer for BM25."""
    return re.findall(r"\w+", text.lower())

class SparseBM25Retriever:
    """In-memory BM25 index for sparse keyword retrieval across document chunks."""

    def __init__(self):
        self.corpus_chunks: List[Dict[str, Any]] = []
        self.tokenized_corpus: List[List[str]] = []
        self.bm25: Optional[BM25Okapi] = None

    def add_chunks(self, chunks: List[Dict[str, Any]]):
        """Index a list of chunk dicts into the BM25 model."""
        for c in chunks:
            self.corpus_chunks.append(c)
            indexable_text = f"{c.get('document_name', '')} {c.get('section_heading', '')} {c.get('content', '')}"
            self.tokenized_corpus.append(tokenize(indexable_text))
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
            logger.info(f"BM25 index updated. Total indexed chunks: {len(self.corpus_chunks)}")

    def search_sparse(
        self,
        query: str,
        top_k: int = 5,
        document_ids: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """Search BM25 keyword index."""
        if not self.bm25 or not self.corpus_chunks:
            return []

        tokens = tokenize(query)
        if not tokens:
            return []

        scores = self.bm25.get_scores(tokens)
        scored_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)

        results = []
        for idx in scored_indices:
            score = float(scores[idx])
            chunk_tokens = self.tokenized_corpus[idx]
            has_match = any(t in chunk_tokens for t in tokens)
            if not has_match:
                continue

            chunk = self.corpus_chunks[idx]
            if document_ids and chunk.get("document_id") not in document_ids:
                continue

            results.append({
                "chunk_id": chunk.get("chunk_id"),
                "document_id": chunk.get("document_id"),
                "document_name": chunk.get("document_name"),
                "page_number": chunk.get("page_number"),
                "section_heading": chunk.get("section_heading", ""),
                "content": chunk.get("content"),
                "score": max(score, 0.01),
                "retrieval_method": "sparse_bm25",
                "metadata": chunk
            })
            if len(results) >= top_k:
                break

        return results

    def remove_document(self, document_id: str):
        """Remove all chunks belonging to a document and rebuild BM25."""
        new_chunks = [c for c in self.corpus_chunks if c.get("document_id") != document_id]
        self.corpus_chunks = new_chunks
        self.tokenized_corpus = [tokenize(c["content"]) for c in self.corpus_chunks]
        if self.tokenized_corpus:
            self.bm25 = BM25Okapi(self.tokenized_corpus)
        else:
            self.bm25 = None

bm25_retriever = SparseBM25Retriever()
