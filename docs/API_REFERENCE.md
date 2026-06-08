# REST API Reference & Swagger Specification

## 1. Overview
The platform exposes a standard RESTful API on port 5000 with interactive Swagger UI at `/api/v1/docs` and OpenAPI 3.0 specification at `/api/v1/docs/openapi.json`.

All endpoints use JSON payloads (except `multipart/form-data` on upload) and return standard HTTP status codes (`200`, `400`, `401`, `404`, `413`, `500`).

---

## 2. API Endpoints

### 2.1 Authentication & System
| Method | Endpoint | Description | Auth Required |
|---|---|---|:---:|
| `GET` | `/health` | Root system liveness health check | No |
| `GET` | `/api/v1/health` | Service component health (DB, Vector Store, Ollama) | No |
| `GET` | `/api/v1/ready` | Readiness check confirming vector and relational storage | No |
| `POST` | `/api/v1/auth/register` | Register new user account | No |
| `POST` | `/api/v1/auth/login` | Authenticate user and issue JWT bearer token | No |
| `GET` | `/api/v1/docs` | Interactive Swagger UI documentation | No |
| `GET` | `/api/v1/docs/openapi.json` | OpenAPI 3.0 specification | No |

### 2.2 Documents
| Method | Endpoint | Description | Payload / Query |
|---|---|---|---|
| `POST` | `/api/v1/documents/upload` | Ingest document (PDF, DOCX, PNG, JPG) | `multipart/form-data` with `file` |
| `GET` | `/api/v1/documents` | List all ingested documents with metadata | `?page=1&page_size=20` |
| `GET` | `/api/v1/documents/{id}` | Get document metadata and layout chunks | None |
| `DELETE` | `/api/v1/documents/{id}` | Delete document, chunks, and Qdrant vectors | None |
| `POST` | `/api/v1/documents/{id}/reprocess` | Re-run ingestion and re-index vectors | None |

### 2.3 Search & Grounded Chat
| Method | Endpoint | Description | Payload |
|---|---|---|---|
| `POST` | `/api/v1/search` | Hybrid RRF search with cross-encoder reranking | `{"query": "payment terms", "top_k": 5, "mode": "hybrid"}` |
| `POST` | `/api/v1/chat` | Evidence-grounded QA with verified citations | `{"message": "What is the fee?", "strict_grounding": true}` |

### 2.4 Structured Extraction & Comparison
| Method | Endpoint | Description | Payload |
|---|---|---|---|
| `POST` | `/api/v1/extract` | Extract schema entities (`contract`, `invoice`) | `{"document_id": "uuid", "schema_type": "contract"}` |
| `POST` | `/api/v1/compare` | Audit differences across two agreements | `{"document_id_a": "uuid", "document_id_b": "uuid"}` |

### 2.5 Autonomous Agent & Reports
| Method | Endpoint | Description | Payload |
|---|---|---|---|
| `POST` | `/api/v1/agent/run` | Launch LangGraph autonomous agent workflow | `{"goal": "Audit late payment clauses"}` |
| `GET` | `/api/v1/agent/runs/{id}` | Inspect agent run steps, observations, and report | None |
| `GET` | `/api/v1/reports` | List generated audit reports | None |
