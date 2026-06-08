# REST API Reference

All endpoints are versioned under `/api/v1`.

## Authentication
- `POST /api/v1/auth/register`: Register user (`email`, `username`, `password`)
- `POST /api/v1/auth/login`: Authenticate and receive JWT bearer token

## Document Management
- `POST /api/v1/documents/upload`: Upload file (multipart form with `file`). Validates extension (.pdf, .docx, .png, .jpg), computes SHA-256, chunks, and indexes.
- `GET /api/v1/documents`: List ingested documents with page counts and processing statuses.
- `GET /api/v1/documents/{id}`: Retrieve document details, metadata, and chunk contents.
- `DELETE /api/v1/documents/{id}`: Delete document, database records, and vector chunks.
- `POST /api/v1/documents/{id}/reprocess`: Reprocess existing document through parsing and indexing.

## Intelligence & Retrieval
- `POST /api/v1/search`: Hybrid search across chunks (`query`, `mode`, `top_k`, `rerank`).
- `POST /api/v1/chat`: Evidence-grounded conversational Q&A (`message`, `document_ids`, `strict_grounding`).
- `POST /api/v1/extract`: Structured extraction (`document_id`, `schema_name`: `contract` or `invoice`).
- `POST /api/v1/compare`: Cross-document difference audit (`document_a_id`, `document_b_id`, `category`).

## Workflows & Reports
- `POST /api/v1/agent/run`: Run autonomous document analysis agent (`goal`, `document_ids`).
- `GET /api/v1/agent/runs/{id}`: Retrieve agent run execution trace and output report.
- `GET /api/v1/reports`: List generated intelligence reports.
- `GET /api/v1/reports/{id}`: Retrieve markdown intelligence report by ID.

## Operations
- `GET /api/v1/health`: Liveness probe.
- `GET /api/v1/ready`: Readiness probe with database, vector store, and LLM statuses.
- `GET /api/v1/docs/openapi.json`: OpenAPI 3.0 specification.
