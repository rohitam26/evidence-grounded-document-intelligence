from typing import List, Dict, Any, Set

class RAGEvaluationMetrics:
    """Calculates factual retrieval, generation, citation, and abstention metrics."""

    @staticmethod
    def calculate_hit_rate(retrieved_doc_pages: List[str], expected_doc_page: str) -> float:
        """Hit Rate: 1.0 if expected document page is in top-K retrieved, else 0.0."""
        return 1.0 if expected_doc_page in retrieved_doc_pages else 0.0

    @staticmethod
    def calculate_mrr(retrieved_doc_pages: List[str], expected_doc_page: str) -> float:
        """Mean Reciprocal Rank (MRR): 1 / (rank + 1) of the first relevant passage."""
        for rank, doc_page in enumerate(retrieved_doc_pages):
            if doc_page == expected_doc_page:
                return 1.0 / (rank + 1)
        return 0.0

    @staticmethod
    def calculate_precision_at_k(retrieved_doc_pages: List[str], relevant_doc_pages: Set[str]) -> float:
        """Precision@K: Fraction of retrieved passages that are relevant."""
        if not retrieved_doc_pages:
            return 0.0
        relevant_count = sum(1 for dp in retrieved_doc_pages if dp in relevant_doc_pages)
        return round(relevant_count / len(retrieved_doc_pages), 4)

    @staticmethod
    def calculate_recall_at_k(retrieved_doc_pages: List[str], relevant_doc_pages: Set[str]) -> float:
        """Recall@K: Fraction of ground truth relevant passages that were retrieved."""
        if not relevant_doc_pages:
            return 1.0
        retrieved_set = set(retrieved_doc_pages)
        relevant_retrieved = len(retrieved_set.intersection(relevant_doc_pages))
        return round(relevant_retrieved / len(relevant_doc_pages), 4)

    @staticmethod
    def calculate_citation_precision(citations: List[Dict[str, Any]], retrieved_passages: List[Dict[str, Any]]) -> float:
        """Citation Precision: Ratio of cited passages that directly substantiate the answer."""
        if not citations:
            return 1.0
        valid = [c for c in citations if c.get("evidence_status") == "verified"]
        return round(len(valid) / len(citations), 4)

    @staticmethod
    def calculate_citation_completeness(citations: List[Dict[str, Any]], expected_page: int) -> float:
        """Citation Completeness: Whether the expected source page is included in the citations."""
        if not citations:
            return 0.0
        cited_pages = {c.get("page_number") for c in citations}
        return 1.0 if expected_page in cited_pages else 0.0

    @staticmethod
    def evaluate_abstention(is_unanswerable: bool, did_abstain: bool) -> float:
        """Abstention Accuracy: Correctly abstains on unanswerable and answers on answerable."""
        return 1.0 if (is_unanswerable == did_abstain) else 0.0
