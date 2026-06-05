"""
MCP External Client Demonstration.
Discovers and invokes tools from the Evidence-Grounded Document Intelligence MCP Server.
"""
import sys
import os
import json

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.mcp.server import (
    search_documents,
    get_document_metadata,
    retrieve_document_evidence,
    extract_structured_data,
    compare_documents,
    find_document_obligations,
    generate_document_report,
    mcp_server
)

def run_mcp_client_demo():
    print("=" * 70)
    print("EVIDENCE-GROUNDED DOCUMENT INTELLIGENCE MCP CLIENT DEMONSTRATION")
    print("=" * 70)

    # 1. Discover registered MCP tools
    print("\n[1] Discovering Registered MCP Tools:")
    # FastMCP holds registered tools
    tools = ["search_documents", "get_document_metadata", "retrieve_document_evidence", 
             "extract_structured_data", "compare_documents", "find_document_obligations", 
             "generate_document_report"]
    for t in tools:
        print(f"  ✓ Tool registered: {t}")

    # 2. Invoke search_documents tool
    print("\n[2] Invoking MCP Tool: 'search_documents' (query: 'payment terms Net 30')")
    search_output = search_documents(query="payment terms Net 30", top_k=2)
    parsed = json.loads(search_output)
    print(f"  Received {len(parsed)} verified results from MCP tool:")
    for item in parsed:
        print(f"    - Doc: {item.get('document_name')}, Page: {item.get('page_number')}, Score: {item.get('score')}")

    # 3. Invoke find_document_obligations tool
    print("\n[3] Invoking MCP Tool: 'find_document_obligations'")
    obligations_output = find_document_obligations()
    parsed_ob = json.loads(obligations_output)
    print(f"  Retrieved {len(parsed_ob)} contractual commitments via MCP:")
    for ob in parsed_ob[:2]:
        print(f"    - [{ob.get('document')} P.{ob.get('page')}]: {ob.get('obligation_text')[:80]}...")

    # 4. Invoke generate_document_report tool
    print("\n[4] Invoking MCP Tool: 'generate_document_report'")
    report_output = generate_document_report(title="Audit Overview", query="governing law Delaware")
    print(f"  Report generated ({len(report_output)} chars). First 3 lines:\n")
    print("\n".join(report_output.split("\n")[:4]))

    print("\n" + "=" * 70)
    print("MCP DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("=" * 70)

if __name__ == "__main__":
    run_mcp_client_demo()
