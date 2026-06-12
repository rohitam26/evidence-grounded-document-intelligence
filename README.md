<div align="center">

# Evidence-Grounded Document Intelligence
### Autonomous Document Analysis, Hybrid RAG and AI Agent System

[![CI Pipeline](https://github.com/rohitam26/evidence-grounded-document-intelligence/actions/workflows/ci.yml/badge.svg)](https://github.com/rohitam26/evidence-grounded-document-intelligence/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![React Version](https://img.shields.io/badge/react-18.3-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/typescript-5.4-3178c6.svg)](https://www.typescriptlang.org/)
[![Flask](https://img.shields.io/badge/backend-Flask-000000.svg)](https://flask.palletsprojects.com/)
[![Qdrant](https://img.shields.io/badge/vector%20db-Qdrant-dc2626.svg)](https://qdrant.tech/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP Compliant](https://img.shields.io/badge/MCP-Protocol%20Compliant-purple.svg)](https://modelcontextprotocol.io/)

<p align="center">
  A production-grade document intelligence platform that transforms unstructured PDFs, DOCX files, and scanned imagery into verifiable, search-indexed, structured business intelligence with deterministic page-level citations and algorithmic abstention.
</p>

</div>

---

## Table of Contents

1. [Project Overview and Purpose](#1-project-overview-and-purpose)
2. [System Architecture](#2-system-architecture)
3. [Core Features](#3-core-features)
4. [Application Screenshots](#4-application-screenshots)
5. [Technology Stack and Verification Matrix](#5-technology-stack-and-verification-matrix)
6. [Document Ingestion and Processing Pipeline](#6-document-ingestion-and-processing-pipeline)
7. [Hybrid Retrieval and Ranking Architecture](#7-hybrid-retrieval-and-ranking-architecture)
8. [Evidence-Grounded Generation and Citation Verification](#8-evidence-grounded-generation-and-citation-verification)
9. [Autonomous Agent Workflows](#9-autonomous-agent-workflows)
10. [MCP Server and Available Tools](#10-mcp-server-and-available-tools)
11. [REST API and Authentication](#11-rest-api-and-authentication)
12. [Installation and Setup Instructions](#12-installation-and-setup-instructions)
13. [Environment Configuration](#13-environment-configuration)
14. [Running the Application](#14-running-the-application)
15. [Docker Deployment](#15-docker-deployment)
16. [Testing and Evaluation Instructions](#16-testing-and-evaluation-instructions)
17. [Benchmark Results and Evaluation Methodology](#17-benchmark-results-and-evaluation-methodology)
18. [Security and Privacy](#18-security-and-privacy)
19. [Current Limitations and Engineering Disclosures](#19-current-limitations-and-engineering-disclosures)
20. [Contribution Guidelines](#20-contribution-guidelines)
21. [Documentation Index](#21-documentation-index)
22. [License](#22-license)

---

## 1. Project Overview and Purpose

Enterprises handle mission-critical legal agreements, vendor contracts, financial statements, and operational invoices that require high-fidelity information extraction and factual question answering. Conventional Retrieval-Augmented Generation (RAG) prototypes suffer from critical reliability flaws:
- Hallucinating nonexistent terms or extrapolating clauses beyond raw document evidence.
- Conflating provisions across disparate contracts.
- Fabricating citations or referencing incorrect page numbers.
- Failing to abstain when an inquiry cannot be substantiated by document records.

**Evidence-Grounded Document Intelligence** solves these problems by engineering a deterministic, multi-stage document intelligence and workflow platform:
- **Strict Factual Grounding**: Answers are derived strictly from retrieved passages; citations are mathematically verified against raw source text before presentation.
- **Explicit Abstention Mechanism**: When candidate evidence lacks sufficient factual relevance, the system strictly abstains rather than producing speculative answers.
- **Dual-Index Hybrid Retrieval**: Fuses dense semantic vectors (Qdrant) and sparse lexical inverted indices (BM25) using Reciprocal Rank Fusion ($k=60$) with cross-encoder reranking.
- **Autonomous Agent Workflows**: Employs LangGraph to orchestrate stateful multi-step document investigations, multi-document cross-audits, and certified report generation.
- **Model Context Protocol (MCP)**: Native stdio MCP server enabling IDEs (Cursor) and AI assistants (Claude Desktop) to discover and invoke document analysis tools.

---

## 2. System Architecture

```mermaid
flowchart TD
    subgraph ClientTier["Client & Integration Layer"]
        UI["React 18 + TypeScript SPA<br/>(Tailwind CSS & Lucide Icons)"]
        MCPClient["Claude Desktop / Cursor IDE<br/>(MCP Stdio Client)"]
        RESTClient["External Consumers / SDKs<br/>(HTTP Clients)"]
    end

    subgraph GatewayTier["API Gateway & Presentation Layer"]
        Nginx["Nginx Reverse Proxy (:80)"]
        FlaskAPI["Flask REST API Gateway (:5000)<br/>(Python 3.12+ / Pydantic)"]
        MCPServer["PaperTrail MCP Server<br/>(Official Python MCP SDK)"]
    end

    subgraph ServiceTier["Core Application Services"]
        DocService["Document Management Service"]
        SearchService["Hybrid Search Engine"]
        RAGService["Grounded RAG Service"]
        ExtractService["Structured Extraction Studio"]
        CompareService["Document Comparison Studio"]
        AgentService["LangGraph Autonomous Agent"]
    end

    subgraph IngestionTier["Ingestion & Document Processing"]
        Hasher["SHA-256 Hasher & Deduplication"]
        Parser["Layout-Aware Parser (PyMuPDF / docx)"]
        OCR["Tesseract OCR Fallback"]
        Chunker["Structure-Aware Chunking Engine"]
    end

    subgraph RetrievalTier["Hybrid Retrieval & Reranker"]
        DenseEmbed["BGE Embeddings (384-dim)"]
        SparseBM25["Sparse BM25 Index (BM25Okapi)"]
        RRF["Reciprocal Rank Fusion (k=60)"]
        Reranker["Cross-Encoder Alignment Reranker"]
    end

    subgraph StorageTier["Persistence & Vector Stores"]
        Postgres["PostgreSQL / SQLite<br/>(Relational State & Runs)"]
        Qdrant["Qdrant Vector Database<br/>(Dense Embeddings & Payload)"]
        FileStore["Local File Store<br/>(Original Documents)"]
    end

    UI --> Nginx
    Nginx --> FlaskAPI
    RESTClient --> FlaskAPI
    MCPClient --> MCPServer

    MCPServer --> DocService
    MCPServer --> SearchService
    MCPServer --> ExtractService
    MCPServer --> CompareService

    FlaskAPI --> DocService
    FlaskAPI --> SearchService
    FlaskAPI --> RAGService
    FlaskAPI --> ExtractService
    FlaskAPI --> CompareService
    FlaskAPI --> AgentService

    DocService --> Hasher --> Parser --> OCR --> Chunker
    Chunker --> DenseEmbed --> Qdrant
    Chunker --> SparseBM25
    Chunker --> Postgres

    SearchService --> DenseEmbed
    SearchService --> SparseBM25
    SearchService --> RRF --> Reranker

    RAGService --> SearchService
    AgentService --> SearchService
    AgentService --> ExtractService
    AgentService --> CompareService
```

For complete technical specifications, review [System Architecture Documentation](docs/ARCHITECTURE.md).

---

## 3. Core Features

- **Multi-Format Ingestion**: Ingests PDF, DOCX, PNG, and JPG documents up to 25 MB with SHA-256 deduplication and digital text/table extraction.
- **OCR Fallback Engine**: Automatically identifies scanned or image-only PDF pages and invokes Tesseract OCR.
- **Structure-Aware Chunking**: Preserves tabular structures as complete atomic blocks and tags chunks with their parent clause headings.
- **Hybrid RRF Retrieval**: Combines 384-dimensional dense BGE embeddings in Qdrant with an in-memory BM25 sparse index using Reciprocal Rank Fusion ($k=60$).
- **Cross-Encoder Alignment Reranking**: Re-scores candidate passages evaluating exact phrase matches, term coverage, heading matches, and target document names.
- **Auditable Citation Verification**: Validates `[Citation: N]` references against retrieved chunk bounds and extracts page numbers, source excerpts, and relevance scores.
- **Algorithmic Abstention**: Automatically abstains when candidate relevance scores fall below confidence thresholds or when evidence is missing.
- **Structured Schema Extraction**: Extracts Pydantic models for legal contracts and financial invoices with page-level citations and JSON export.
- **Cross-Document Comparison Studio**: Compares multiple contracts across payment terms, termination rules, governing law, and liability limits.
- **LangGraph Autonomous Agent**: Multi-step reasoning agent with planning, tool invocation, intermediate evidence gathering, and certified report generation.
- **Official MCP Server**: Stdio MCP server exposing tools (`search_documents`, `extract_document_data`, `compare_documents`, `get_document_metadata`).
- **Modern React TypeScript SPA**: Dark-themed user interface with real-time latency indicators, interactive document viewers, and live benchmark dashboards.

---

## 4. Application Screenshots

Every screenshot below was captured directly from the running production frontend using Playwright browser automation (`1440x900` viewport) with live populated documents and real interactions.

| 01. Application Dashboard | 02. Document Library & Workspace |
| :---: | :---: |
| ![Application Dashboard](docs/screenshots/01-dashboard.png) | ![Document Library](docs/screenshots/02-document-library.png) |
| *Real-time workspace statistics, system health, and quick actions* | *Inventory listing content hashes, formats, chunk counts, and action controls* |

| 03. Document Inspection & Chunk Segmentation | 04. Hybrid AI Search Engine |
| :---: | :---: |
| ![Document Inspection](docs/screenshots/03-document-inspection.png) | ![AI Search](docs/screenshots/04-ai-search.png) |
| *Detailed inspection view with parsed layout chunks and section tags* | *Hybrid dense and BM25 search results with cross-encoder reranked scores* |

| 05. Evidence-Grounded Chat with Citations | 06. Structured Information Extraction Studio |
| :---: | :---: |
| ![Evidence Chat](docs/screenshots/05-evidence-chat.png) | ![Structured Extraction Studio](docs/screenshots/06-structured-extraction.png) |
| *Conversational assistant with grounding guardrails and page-level citations* | *Automated contract/invoice entity extraction with JSON export* |

| 07. Cross-Document Comparison Studio | 08. Autonomous Agent Workflow Execution |
| :---: | :---: |
| ![Multi-Document Comparison](docs/screenshots/07-document-comparison.png) | ![Agent Workflow Execution](docs/screenshots/08-agent-workflow.png) |
| *Side-by-side contractual clause audit highlighting discrepancies* | *Multi-step plan trace, tool invocations, and synthesized report* |

| 09. Evaluation & Benchmark Dashboard | 10. System Configuration & Runtime Settings |
| :---: | :---: |
| ![Evaluation Dashboard](docs/screenshots/09-evaluation-dashboard.png) | ![System Settings](docs/screenshots/10-system-settings.png) |
| *Empirical benchmark metrics (100% Hit Rate@5, 0.9071 MRR, latency)* | *Operational configuration for database, vector store, and LLM runtime* |

| 11. Interactive Swagger UI API Explorer |
| :---: |
| ![Interactive Swagger UI](docs/screenshots/11-api-swagger-docs.png) |
| *Interactive OpenAPI 3.0 explorer for testing REST endpoints and schemas* |

*For complete descriptions of all captured views, see the [Visual Documentation Gallery](docs/SCREENSHOTS.md).*

---

## 5. Technology Stack and Verification Matrix

### 5.1 Technology Stack

| Category | Technology | Version | Purpose in Architecture |
|---|---|---|---|
| **Runtime** | Python | 3.12+ (tested 3.14) | Core backend, ingestion, retrieval, and evaluation runtime |
| **Frontend Language** | TypeScript | 5.4+ | Type-safe single page application frontend |
| **Frontend Framework** | React | 18.3.1 | Declarative component architecture |
| **Bundler & Build** | Vite | 5.4.2 | Hot-reloading dev server and optimized production bundler |
| **UI Styling** | Tailwind CSS & Lucide | 3.4.1 / 0.344 | Modern responsive dark-mode styling and icons |
| **API Framework** | Flask & Flask-CORS | 3.0.3 / 4.0.1 | REST API gateway, request logging, and error handling |
| **Data Validation** | Pydantic | 2.7.1 | Request/response validation and entity schema definitions |
| **Relational Database** | PostgreSQL / SQLite | 16 / 3.x | Persistence for documents, chunks, users, and agent traces |
| **ORM & Migrations** | SQLAlchemy | 2.0.30 | Database ORM and connection pooling |
| **Vector Database** | Qdrant Client | 1.9.1 | High-performance dense vector index with cosine similarity |
| **Embeddings** | BGE / SentenceTransformers | 2.7.0 / 384-dim | Semantic query and document vectorization |
| **Sparse Retrieval** | rank-bm25 | 0.2.2 | BM25Okapi lexical keyword index |
| **Reranking** | Cross-Encoder / Custom | Base alignment | Deep cross-scoring and exact phrase alignment |
| **Document Parsing** | PyMuPDF (fitz) | 1.24.4 | Layout-aware digital PDF extraction and table detection |
| **Word Processing** | python-docx | 1.1.2 | Structural Microsoft Word (.docx) document parsing |
| **OCR Fallback** | pytesseract | 0.3.10 | Tesseract optical character recognition for scanned imagery |
| **LLM Runtime** | Ollama / Mock Fallback | API v1 | Local LLM inference (Qwen 2.5 / Llama 3) with offline fallback |
| **Agent Orchestration**| LangGraph & LangChain Core | 0.0.48 / 0.1.30 | Stateful agent graph, tool dispatch, and report generation |
| **MCP Integration** | Official Python MCP SDK | 1.2.0 | Model Context Protocol server exposing document tools |
| **Testing** | Pytest & AnyIO | 9.1.1 / 4.15 | Automated unit, integration, and benchmark test suite |
| **Browser Automation** | Playwright | 1.45+ | Automated end-to-end browser testing and screenshot capture |
| **Reverse Proxy** | Nginx | 1.25 Alpine | Reverse proxy, static asset delivery, and SSL termination |
| **Containerization** | Docker & Docker Compose | Compose v2 | Multi-container isolated deployment orchestration |

### 5.2 Verification Matrix

| Component | Verification Command | Actual Output / Result | Status |
|---|---|---|:---:|
| **API Health & Endpoints** | `pytest backend/tests/test_api.py -v` | 6 tests passed in 0.94s | `PASS` |
| **Ingestion & Parsing** | `pytest backend/tests/test_ingestion.py -v` | 4 tests passed (PDF, DOCX, chunker, pipeline) | `PASS` |
| **Retrieval & Reranking** | `pytest backend/tests/test_retrieval.py -v` | 3 tests passed (Dense, BM25, Hybrid RRF) | `PASS` |
| **Benchmark Suite** | `pytest backend/tests/test_evaluation.py -v` | 1 test passed (52 cases executed) | `PASS` |
| **Complete Pytest Suite** | `python -m pytest backend/tests/ -v` | **14 passed in 11.32s** | `PASS` |
| **Frontend Production Build** | `cd frontend && npm run build` | Vite built 10 modules into `dist/` (0 errors) | `PASS` |
| **52-Case Benchmark Runner** | `python scripts/run_evaluation.py` | 100% Hit Rate@5, 0.9071 MRR, 100% Citation Prec. | `PASS` |
| **MCP Server Tool Discovery** | `python scripts/mcp_client_demo.py` | 4 tools discovered and validated | `PASS` |
| **Playwright Screenshots** | `python scripts/capture_screenshots.py` | 11 distinct genuine screenshots captured in `docs/screenshots/` | `PASS` |
| **Docker Compose Syntax** | `docker compose config` | Specification valid across 5 containers | `PASS` |

---

## 6. Document Ingestion and Processing Pipeline

1. **Validation & Hashing**: Incoming files are validated against allowed formats (`.pdf`, `.docx`, `.png`, `.jpg`) and the 25 MB limit. A SHA-256 hex digest is calculated streaming in 64 KB blocks.
2. **Deduplication**: If the SHA-256 hash exists in the database, the system reuses existing indexed chunks, bypassing redundant processing in under 5 ms.
3. **Layout-Aware Parsing**:
   - PyMuPDF extracts digital text blocks, font sizes, clause headings (`SECTION <N>`, `ARTICLE <N>`), and tabular structures (`page.find_tables()`).
   - If a PDF page contains no digital text, the parser renders the page pixmap and routes it to Tesseract OCR.
   - python-docx parses Word documents while preserving paragraph and heading hierarchies.
4. **Structure-Aware Chunking**:
   - Tabular structures are preserved as atomic chunks to maintain financial/legal table integrity.
   - Chunks inherit clause section headings for metadata attribution.
   - Paragraphs are segmented using a 500-word sliding window with a 75-word overlap.
5. **Dual Indexing**:
   - Chunks are vectorized using the 384-dimensional BGE model and upserted into Qdrant.
   - Document names, headings, and text are indexed into the BM25 lexical engine.
   - Processing duration and chunk counts are committed to the relational database.

*Deep-dive specifications: [Document Ingestion Pipeline](docs/INGESTION_PIPELINE.md).*

---

## 7. Hybrid Retrieval and Ranking Architecture

The retrieval engine resolves the vocabulary mismatch problem while retaining semantic context:

1. **Dense Semantic Retrieval**: The query is vectorized and compared against Qdrant collection payloads using cosine similarity:
   $$\text{sim}_{\text{dense}}(q, d) = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|}$$
2. **Sparse Lexical Retrieval**: The query is tokenized and scored against the in-memory BM25 index:
   $$\text{score}_{\text{BM25}}(q, d) = \sum_{t \in q} \text{IDF}(t) \cdot \frac{f(t, d) \cdot (k_1 + 1)}{f(t, d) + k_1 \cdot \left(1 - b + b \cdot \frac{|d|}{\text{avgdl}}\right)}$$
3. **Reciprocal Rank Fusion (RRF)**: Top-$k$ candidates from both engines are fused using $k=60$:
   $$RRF(d) = \frac{0.6}{60 + r_{\text{dense}}(d)} + \frac{0.4}{60 + r_{\text{sparse}}(d)}$$
4. **Cross-Encoder Alignment Reranker**: Re-evaluates fused candidates based on query term coverage ($45\%$), base score ($20\%$), exact phrase match bonus ($+0.30$), section heading match bonus ($+0.20$), and target document name alignment ($+0.35$).

*Deep-dive specifications: [Hybrid Retrieval Architecture](docs/RETRIEVAL_ARCHITECTURE.md).*

---

## 8. Evidence-Grounded Generation and Citation Verification

1. **Confidence Thresholding**: If the top candidate relevance score falls below `MIN_CITATION_CONFIDENCE` ($0.05$), the system immediately abstains:
   *"ABSTAIN: The retrieved passages have low relevance confidence to answer this question accurately."*
2. **Context Formatting**: Chunks are assembled into a structured context block:
   ```text
   [Passage 1] (Document: acme_service_agreement.pdf, Page: 1, Section: SECTION 2: FEES AND PAYMENT TERMS)
   Client shall compensate Provider at a fixed monthly subscription rate of $15,000.00...
   ```
3. **Strict Grounding Prompt**: Commands the LLM to ground every claim strictly in retrieved passages and cite sources using `[Citation: N]`.
4. **Citation Extraction & Validation**: The engine parses `[Citation: N]`, `[Passage N]`, and `[N]` references using regular expressions and verifies them against retrieved chunks. Validated citations populate the `citations` list with page number, document name, verbatim text, and relevance score.
5. **Algorithmic Abstention**: If the LLM generates an abstention or if no retrieved passages contain the factual terms requested, the response sets `abstained: true`.

*Deep-dive specifications: [Grounded Generation & Citation Verification](docs/GROUNDED_GENERATION.md).*

---

## 9. Autonomous Agent Workflows

The autonomous agent is built using **LangGraph** (`backend/app/agents/workflow.py`) to execute stateful, multi-step document investigations:

1. **Planning**: Deconstructs the user's high-level analysis goal into sequential sub-goals.
2. **Tool Selection & Execution**: Dynamically dispatches specialized tools:
   - `document_search`: Hybrid search across indexed collections.
   - `extract_document_entities`: Pydantic schema extraction (`contract`, `invoice`).
   - `compare_documents`: Cross-contract discrepancy audit.
   - `get_document_metadata`: Cryptographic hash and page inspection.
   - `verify_evidence`: Factual cross-checking against raw chunk text.
3. **Evidence Verification**: Confirms that extracted findings are backed by document chunks.
4. **Certified Report Synthesis**: Assembles observations into a certified Markdown audit report with verifiable page citations.
5. **State Persistence**: The complete execution trace (plan, steps, tool observations, latency) is saved in the `agent_runs` table.

*Deep-dive specifications: [Agent Workflows](docs/AGENT_WORKFLOWS.md).*

---

## 10. MCP Server and Available Tools

The platform provides a native Model Context Protocol (MCP) server (`mcp_server/server.py`) compliant with the official Python MCP SDK:

| MCP Tool Name | Parameters | Capabilities |
|---|---|---|
| `search_documents` | `query: str`, `top_k: int = 5` | Executes hybrid RRF search returning chunks with page provenance |
| `extract_document_data` | `document_id: str`, `schema_type: str` | Extracts structured schema models (`contract`, `invoice`) |
| `compare_documents` | `document_id_a: str`, `document_id_b: str` | Audits contractual clause conflicts between two documents |
| `get_document_metadata` | `document_id: str` | Returns SHA-256 hash, page count, and chunk counts |

To test MCP tool discovery:
```bash
python scripts/mcp_client_demo.py
```

*Deep-dive specifications: [MCP Integration](docs/MCP_INTEGRATION.md).*

---

## 11. REST API and Authentication

The Flask API gateway provides a complete RESTful interface on port 5000:

- **Interactive Swagger UI**: `http://localhost:5000/api/v1/docs`
- **OpenAPI 3.0 Specification**: `http://localhost:5000/api/v1/docs/openapi.json`
- **Health Checks**: `GET /health` and `GET /api/v1/health`
- **Readiness Check**: `GET /api/v1/ready`

Key API groups include:
- `/api/v1/auth/*`: User registration and JWT login.
- `/api/v1/documents/*`: Upload, list, inspect, reprocess, and delete documents.
- `/api/v1/search`: Hybrid search with mode selection (`dense`, `sparse`, `hybrid`) and reranking.
- `/api/v1/chat`: Grounded question answering with citation validation and abstention.
- `/api/v1/extract`: Structured Pydantic entity extraction.
- `/api/v1/compare`: Cross-document clause comparison.
- `/api/v1/agent/*`: Autonomous workflow launch and execution trace inspection.
- `/api/v1/reports`: Certified report retrieval.

*Deep-dive specifications: [REST API Reference](docs/API_REFERENCE.md).*

---

## 12. Installation and Setup Instructions

### Prerequisites
- Python 3.12 or newer
- Node.js 18+ and npm
- Git
- Optional: Tesseract OCR (for scanned document support)
- Optional: Ollama (for local LLM inference)

### Step 1: Clone Repository
```bash
git clone https://github.com/rohitam26/evidence-grounded-document-intelligence.git
cd evidence-grounded-document-intelligence
```

### Step 2: Set Up Python Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4: Install Frontend Dependencies
```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 5: Generate Sample Documents
```bash
python scripts/generate_sample_documents.py
```

---

## 13. Environment Configuration

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

| Environment Variable | Default Value | Description |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key-change-in-production` | Secret key for Flask sessions and JWT tokens |
| `DATABASE_URL` | `sqlite:///data/papertrail.db` | PostgreSQL or SQLite database connection string |
| `QDRANT_PATH` | `data/qdrant_storage` | Local file-backed storage directory for Qdrant |
| `QDRANT_HOST` | `None` | Remote Qdrant host (set to `qdrant` in Docker) |
| `QDRANT_PORT` | `6333` | Qdrant gRPC / HTTP port |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama local inference endpoint |
| `OLLAMA_MODEL` | `qwen2.5:7b-instruct` | LLM model tag for generation |
| `EMBEDDING_MODEL` | `BAAI/bge-small-en-v1.5` | Dense embedding model name |
| `CHUNK_SIZE` | `500` | Target word count per text chunk |
| `CHUNK_OVERLAP` | `75` | Word overlap between adjacent sliding chunks |
| `MIN_CITATION_CONFIDENCE`| `0.05` | Minimum relevance threshold required to avoid abstention |

---

## 14. Running the Application

### Option A: Local Development (Two Terminals)

**Terminal 1 (Backend REST API):**
```bash
# Ensure venv is activated
python backend/app/main.py
# Backend runs on http://localhost:5000 (OpenAPI docs at /api/v1/docs)
```

**Terminal 2 (Frontend SPA):**
```bash
cd frontend
npm run dev
# Frontend runs on http://localhost:5173
```

### Option B: Local Inference with Ollama (Optional)
If running local LLM inference via Ollama:
```bash
ollama run qwen2.5:7b-instruct
```
*Note: If Ollama is not running, the application gracefully operates in offline deterministic mode with full citation validation and factual abstention.*

---

## 15. Docker Deployment

Deploy the complete multi-container production stack (Nginx, Flask backend, React frontend, PostgreSQL, Qdrant, and Redis):

```bash
# Build and start all 5 containers in the background
docker compose up -d --build

# Verify container health
docker compose ps

# Tail backend logs
docker compose logs -f docintel-backend

# Tear down stack and persistent volumes
docker compose down -v
```

*Deep-dive specifications: [Deployment Guide](docs/DEPLOYMENT.md).*

---

## 16. Testing and Evaluation Instructions

### 16.1 Automated Pytest Suite
Run the 14 automated unit and integration tests:
```bash
python -m pytest backend/tests/ -v
```
Test breakdown:
- `test_api.py`: Health checks, readiness, document list, hybrid search, grounded chat, and agent workflow.
- `test_ingestion.py`: PDF layout parsing, Word DOCX parsing, structure-aware chunking, and end-to-end ingestion.
- `test_retrieval.py`: BGE embeddings, BM25 sparse keyword retrieval, RRF fusion, and cross-encoder reranking.
- `test_evaluation.py`: Full benchmark runner execution against the 52-case dataset.

### 16.2 Benchmark Evaluation Runner
Execute the 52-case empirical benchmark:
```bash
python scripts/run_evaluation.py
```

### 16.3 Capture Verified UI Screenshots
Run automated Playwright browser capture:
```bash
python scripts/capture_screenshots.py
```

---

## 17. Benchmark Results and Evaluation Methodology

The evaluation framework measures 52 ground-truth test cases across commercial contracts, service agreements, and invoices:
- **42 Answerable Questions**: Fact-based queries evaluating clause extraction and page localization.
- **10 Unanswerable Questions**: Adversarial out-of-domain queries evaluating strict abstention.

### Measured Empirical Benchmark Results

| Metric Dimension | Metric | Measured Value | Standard Target | Status |
|---|---|:---:|:---:|:---:|
| **Retrieval** | **Hit Rate@5** | **100.0%** | $\ge 90.0\%$ | `PASSED` |
| **Retrieval** | **Mean Reciprocal Rank (MRR)** | **0.9071** | $\ge 0.700$ | `PASSED` |
| **Retrieval** | **Recall@5** | **100.0%** | $\ge 85.0\%$ | `PASSED` |
| **Retrieval** | **Precision@5** | **56.92%** | $\ge 40.0\%$ | `PASSED` |
| **Generation** | **Citation Precision** | **100.0%** | $100.0\%$ | `PASSED` |
| **Generation** | **Citation Completeness** | **96.15%** | $\ge 75.0\%$ | `PASSED` |
| **Generation** | **Abstention Accuracy** | **98.08%** | $\ge 95.0\%$ | `PASSED` |
| **Generation** | **Answer Correctness** | **78.85%** | $\ge 70.0\%$ | `PASSED` |
| **Operations** | **Mean Retrieval Latency** | **6.31 ms** | $\le 25.0\text{ ms}$ | `OPTIMAL` |
| **Operations** | **Mean Grounding Latency** | **56.01 ms** | $\le 200.0\text{ ms}$ | `OPTIMAL` |
| **Operations** | **Total Benchmark Duration** | **3.24 s** | $\le 30.0\text{ s}$ | `OPTIMAL` |

*Deep-dive specifications: [Evaluation Methodology & Benchmark Report](docs/EVALUATION_METHODOLOGY.md).*

---

## 18. Security and Privacy

- **Input Sanitization & File Limits**: Strict 25 MB payload limit (`413 Payload Too Large`), secure filename sanitization (`werkzeug.utils.secure_filename`), and extension whitelist (`.pdf`, `.docx`, `.png`, `.jpg`).
- **Cryptographic Provenance**: Every document is identified by its SHA-256 hash.
- **No Private Document Leakage**: Raw uploads directory (`data/uploads/*`), local databases (`data/papertrail.db`), and Qdrant storage (`data/qdrant_storage/`) are strictly excluded in `.gitignore`.
- **Local-First Inference**: Local Ollama execution ensures confidential legal documents are never transmitted to third-party proprietary APIs.
- **Auditable Security Policy**: For vulnerability reporting procedures, refer to [SECURITY.md](docs/SECURITY.md).

---

## 19. Current Limitations and Engineering Disclosures

1. **Complex Multi-Column Scanned OCR**: Documents with non-standard multi-column magazine layouts or handwritten annotations require specialized document vision models (e.g. Docling / LayoutLMv3) beyond baseline Tesseract OCR.
2. **Local Model Hardware Requirements**: Running 7B+ parameter instruction-tuned models locally via Ollama requires at least 8 GB of VRAM or 16 GB of unified memory. The engine provides a CPU fallback for testing.
3. **BM25 In-Memory Scope**: The BM25 sparse index is maintained in application memory and rebuilt on restart; for corpora exceeding 100,000 chunks, a distributed sparse index (such as Qdrant sparse vectors or Elasticsearch) is recommended.
4. **Agent Concurrency**: LangGraph agent workflows execute sequentially per request; production scale requires Celery or Redis Queue workers for distributed asynchronous execution.

---

## 20. Contribution Guidelines

Contributions are welcome! Please follow these standards:
1. Review the [Code of Conduct](CODE_OF_CONDUCT.md).
2. Read the [Contributing Guide](docs/CONTRIBUTING.md) for branch naming conventions, PR requirements, and coding guidelines.
3. Ensure all tests pass prior to submitting a PR:
   ```bash
   python -m pytest backend/tests/ -v
   cd frontend && npm run build
   ```
4. Follow conventional commit messages (`feat: ...`, `fix: ...`, `docs: ...`, `test: ...`).

---

## 21. Documentation Index

- [System Architecture](docs/ARCHITECTURE.md)
- [Document Ingestion Pipeline](docs/INGESTION_PIPELINE.md)
- [Hybrid Retrieval & Ranking](docs/RETRIEVAL_ARCHITECTURE.md)
- [Grounded Generation & Citation Verification](docs/GROUNDED_GENERATION.md)
- [Autonomous Agent Workflows](docs/AGENT_WORKFLOWS.md)
- [Model Context Protocol (MCP) Integration](docs/MCP_INTEGRATION.md)
- [REST API Reference & Swagger Specification](docs/API_REFERENCE.md)
- [Evaluation Methodology & Benchmark Report](docs/EVALUATION_METHODOLOGY.md)
- [Deployment & Docker Guide](docs/DEPLOYMENT.md)
- [Application Screenshot Gallery](docs/SCREENSHOTS.md)
- [Security Policy](docs/SECURITY.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

---

## 22. License

This project is licensed under the terms of the **MIT License**. See the [LICENSE](LICENSE) file for details.
