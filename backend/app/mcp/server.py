import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from mcp.server.mcpserver import MCPServer
from app.services.search_service import search_service
from app.services.extraction_service import extraction_service
from app.services.comparison_service import comparison_service
from app.agents.tools import tool_find_obligations, tool_generate_report
from app.core.database import get_db_session
from app.models import Document, Chunk

# Initialize Official Python SDK MCPServer
mcp_server = MCPServer(
    name="Evidence-Grounded Document Intelligence MCP Server",
    instructions="Provides evidence-grounded search, extraction, and comparison tools over verified documents."
)

@mcp_server.tool()
def search_documents(query: str, top_k: int = 5) -> str:
    """Search for relevant verified document passages with citations."""
    res = search_service.search(query=query, top_k=top_k)
    return json.dumps([item.model_dump() for item in res.results], indent=2)

@mcp_server.tool()
def get_document_metadata(document_id: str) -> str:
    """Retrieve metadata, page count, and status for a document."""
    with get_db_session() as db:
        doc = db.query(Document).filter(Document.id == document_id).first()
        if not doc:
            return json.dumps({"error": f"Document {document_id} not found"})
        return json.dumps({
            "id": doc.id,
            "filename": doc.filename,
            "file_type": doc.file_type,
            "page_count": doc.page_count,
            "processing_status": doc.processing_status,
            "metadata": doc.metadata_json
        }, indent=2)

@mcp_server.tool()
def retrieve_document_evidence(document_id: str, query: str) -> str:
    """Retrieve verified evidence passages within a specific document."""
    res = search_service.search(query=query, document_ids=[document_id], top_k=3)
    return json.dumps([item.model_dump() for item in res.results], indent=2)

@mcp_server.tool()
def extract_structured_data(document_id: str, schema_name: str = "contract") -> str:
    """Extract schema-validated fields with page citations from a document."""
    res = extraction_service.extract(document_id=document_id, schema_name=schema_name)
    return json.dumps(res.model_dump(), indent=2)

@mcp_server.tool()
def compare_documents(document_a_id: str, document_b_id: str) -> str:
    """Compare two documents across payment terms, termination, and governing law."""
    res = comparison_service.compare(document_a_id=document_a_id, document_b_id=document_b_id, user_id="mcp-client")
    return json.dumps(res.model_dump(), indent=2)

@mcp_server.tool()
def find_document_obligations(document_ids: Optional[List[str]] = None) -> str:
    """Identify contractual obligations and service level commitments."""
    obligations = tool_find_obligations(document_ids=document_ids)
    return json.dumps(obligations, indent=2)

@mcp_server.tool()
def generate_document_report(title: str, query: str) -> str:
    """Generate an evidence-backed markdown intelligence report."""
    res = search_service.search(query=query, top_k=5)
    evidence = [item.model_dump() for item in res.results]
    findings = [f"Verified evidence retrieved for query: '{query}'."]
    report = tool_generate_report(title=title, evidence=evidence, findings=findings)
    return report

if __name__ == "__main__":
    mcp_server.run()
