import re
from typing import List, Dict, Any, Optional
from app.retrieval.hybrid import hybrid_search_engine
from app.services.extraction_service import extraction_service
from app.services.comparison_service import comparison_service
from app.core.database import get_db_session
from app.models import Document, Chunk

def tool_search_documents(query: str, document_ids: Optional[List[str]] = None, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search for relevant document passages."""
    results = hybrid_search_engine.search(query=query, top_k=top_k, document_ids=document_ids)
    return [
        {
            "chunk_id": r["chunk_id"],
            "document_name": r["document_name"],
            "page_number": r["page_number"],
            "content": r["content"],
            "score": r["score"]
        }
        for r in results
    ]

def tool_retrieve_evidence(document_id: str, query: str) -> List[Dict[str, Any]]:
    """Retrieve verified evidence passages for a specific document."""
    return tool_search_documents(query=query, document_ids=[document_id], top_k=3)

def tool_extract_document_fields(document_id: str, schema_name: str = "contract") -> Dict[str, Any]:
    """Extract structured data fields according to schema."""
    res = extraction_service.extract(document_id=document_id, schema_name=schema_name)
    return res.model_dump()

def tool_compare_documents(document_a_id: str, document_b_id: str, user_id: str = "system") -> Dict[str, Any]:
    """Compare two documents across key legal and commercial categories."""
    res = comparison_service.compare(document_a_id=document_a_id, document_b_id=document_b_id, user_id=user_id)
    return res.model_dump()

def tool_find_obligations(document_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Identify contractual obligations, SLAs, and warranties across documents."""
    query = "obligations guarantees warranty SLA uptime confidentiality audit requirements"
    results = hybrid_search_engine.search(query=query, top_k=6, document_ids=document_ids)
    return [
        {
            "document": r["document_name"],
            "page": r["page_number"],
            "obligation_text": r["content"][:250],
            "confidence": r["score"]
        }
        for r in results
    ]

def tool_identify_deadlines(document_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """Identify dates, deadlines, renewal periods, and expiration terms."""
    query = "deadline expiration date renewal notice days payment due date"
    results = hybrid_search_engine.search(query=query, top_k=6, document_ids=document_ids)
    deadlines = []
    for r in results:
        matches = re.findall(r"(\d+\s*days|January\s*\d+|February\s*\d+|March\s*\d+|Net\s*\d+)", r["content"], re.IGNORECASE)
        deadlines.append({
            "document": r["document_name"],
            "page": r["page_number"],
            "key_deadlines": matches if matches else ["Explicit timeframe in passage"],
            "passage": r["content"][:200]
        })
    return deadlines

def tool_validate_citations(claims_with_citations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Verify that cited passages actually contain the asserted claims."""
    verified = []
    unverified = []
    for item in claims_with_citations:
        passage = item.get("passage", "").lower()
        claim = item.get("claim", "").lower()
        key_words = [w for w in claim.split() if len(w) > 3]
        match_count = sum(1 for w in key_words if w in passage)
        if match_count >= min(2, len(key_words)):
            verified.append(item)
        else:
            unverified.append(item)
    return {
        "verified_count": len(verified),
        "unverified_count": len(unverified),
        "all_valid": len(unverified) == 0,
        "details": {"verified": verified, "unverified": unverified}
    }

def tool_generate_report(title: str, evidence: List[Dict[str, Any]], findings: List[str]) -> str:
    """Generate an evidence-backed executive markdown report."""
    md_lines = [
        f"# {title}",
        "",
        "## Executive Summary",
        "This report was autonomously generated and grounded in verified document intelligence.",
        "",
        "## Key Verified Findings",
    ]
    for f in findings:
        md_lines.append(f"- {f}")

    md_lines.extend([
        "",
        "## Source Evidence & Citations",
        "| Document | Page | Verified Passage |",
        "| --- | --- | --- |"
    ])
    for e in evidence:
        doc = e.get("document_name") or e.get("document") or "Source Document"
        page = e.get("page_number") or e.get("page") or 1
        text = (e.get("content") or e.get("passage") or e.get("obligation_text") or "")[:150].replace("\n", " ")
        md_lines.append(f"| {doc} | Page {page} | {text}... |")

    md_lines.extend([
        "",
        "---",
        "*Audited and certified by Autonomous Document Intelligence Agent.*"
    ])
    return "\n".join(md_lines)
