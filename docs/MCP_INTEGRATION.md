# Model Context Protocol (MCP) Integration

## 1. Overview

**PaperTrail MCP Server** exposes the complete document intelligence toolkit over the official Model Context Protocol (MCP) standard using standard I/O (`stdio`) transport. Any MCP-compatible host—including Claude Desktop, Cursor IDE, or custom agent orchestrators—can discover, search, extract, compare, and verify documents managed by Evidence-Grounded Document Intelligence.

```mermaid
flowchart LR
    subgraph Host["MCP Client Host (e.g. Claude Desktop, Cursor, Custom Agent)"]
        ClientRuntime["MCP Client SDK<br/>(TypeScript / Python / Rust)"]
        UI["Chat / Editor Interface"]
        UI --> ClientRuntime
    end

    subgraph MCPBoundary["MCP Protocol Transport (JSON-RPC 2.0 over Stdio)"]
        ClientRuntime -- "tools/list" --> StdioPipe["Standard In / Standard Out"]
        ClientRuntime -- "tools/call" --> StdioPipe
    end

    subgraph Server["PaperTrail MCP Server (backend/app/mcp/server.py)"]
        MCPEngine["Official Python MCP Server Instance"]
        StdioPipe --> MCPEngine
        
        subgraph Tools["Registered MCP Tools"]
            T1["search_documents<br/>(Hybrid RRF Search)"]
            T2["extract_document_data<br/>(Pydantic Schema Extraction)"]
            T3["compare_documents<br/>(Cross-Contract Audit)"]
            T4["get_document_metadata<br/>(SHA-256 & Chunk Stats)"]
        end

        MCPEngine --> T1
        MCPEngine --> T2
        MCPEngine --> T3
        MCPEngine --> T4
    end

    subgraph Platform["Core Platform Engines"]
        T1 --> SearchEngine["Hybrid Retrieval & Reranker"]
        T2 --> ExtractionEngine["Information Extraction Studio"]
        T3 --> ComparisonEngine["Contract Comparison Studio"]
        T4 --> StorageEngine["PostgreSQL & Qdrant Store"]
    end
```

---

## 2. Available MCP Tools

| Tool Name | Parameters | Description | Return Format |
|---|---|---|---|
| `search_documents` | `query: str`, `top_k: int = 5` | Executes hybrid dense/sparse search with reranking | JSON array of chunks with citations & relevance |
| `extract_document_data` | `document_id: str`, `schema_type: str = "contract"` | Extracts schema entities (`contract`, `invoice`) | Structured JSON with page numbers & verbatim passages |
| `compare_documents` | `document_id_a: str`, `document_id_b: str` | Audits clause conflicts across two documents | JSON comparison table across 4 legal dimensions |
| `get_document_metadata` | `document_id: str` | Retrieves cryptographic hash, page count, and status | Document metadata payload |

---

## 3. Configuration & Usage

### 3.1 Claude Desktop Configuration (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "evidence-document-intelligence": {
      "command": "python",
      "args": [
        "E:\\develop\\evidence-grounded-document-intelligence\\mcp_server\\server.py"
      ],
      "env": {
        "PYTHONPATH": "E:\\develop\\evidence-grounded-document-intelligence\\backend"
      }
    }
  }
}
```

### 3.2 Testing via Demo Client (`scripts/mcp_client_demo.py`)
Run the standalone MCP client harness to verify tool discovery and execution:
```bash
python scripts/mcp_client_demo.py
```
Output:
```text
======================================================================
PAPERTRAIL MCP CLIENT TEST & TOOL DISCOVERY
======================================================================
[*] Initializing PaperTrail MCP Server...
[*] Discovering available MCP tools:
  - search_documents: Hybrid search across indexed documents
  - extract_document_data: Extract structured schema entities
  - compare_documents: Compare two documents across key dimensions
  - get_document_metadata: Retrieve file hash, pages, and metadata
[*] Executing test search: 'payment terms Net 30'
  ✓ Search executed successfully. Retrieved candidate chunks.
[*] Executing test extraction on schema: 'contract'
  ✓ Schema extracted with page-level citations.
======================================================================
MCP Integration Test Completed Successfully!
======================================================================
```
