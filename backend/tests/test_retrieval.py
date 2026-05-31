import os
import pytest
from app.retrieval.embeddings import embedding_generator
from app.retrieval.vector_store import vector_store
from app.retrieval.bm25 import bm25_retriever
from app.retrieval.reranker import reranker
from app.retrieval.hybrid import hybrid_search_engine
from app.config import settings

def test_embedding_generation():
    texts = ["Master Services Agreement payment terms", "Standard invoice billing cycle"]
    embeddings = embedding_generator.embed_texts(texts)
    assert len(embeddings) == 2
    assert len(embeddings[0]) == settings.EMBEDDING_DIM

def test_bm25_sparse_retrieval():
    test_chunks = [
        {
            "chunk_id": "c1",
            "document_id": "d1",
            "document_name": "contract.pdf",
            "page_number": 1,
            "section_heading": "Payment Terms",
            "content": "All invoices are payable under Net 30 days from invoice issuance date."
        },
        {
            "chunk_id": "c2",
            "document_id": "d1",
            "document_name": "contract.pdf",
            "page_number": 2,
            "section_heading": "Governing Law",
            "content": "This agreement is governed by the laws of the State of Delaware."
        }
    ]
    bm25_retriever.add_chunks(test_chunks)
    res = bm25_retriever.search_sparse("Net 30 payment invoice", top_k=2)
    assert len(res) > 0
    assert res[0]["chunk_id"] == "c1"

def test_hybrid_rrf_and_reranker():
    results = hybrid_search_engine.search(
        query="payment terms Net 30 days",
        top_k=3,
        mode="hybrid",
        apply_rerank=True
    )
    assert isinstance(results, list)
    if results:
        assert "score" in results[0]
        assert "content" in results[0]
        assert "retrieval_method" in results[0]
