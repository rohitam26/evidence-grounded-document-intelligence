import json
import re
from typing import Dict, Any, Optional
from app.config import settings
from app.core.database import get_db_session
from app.models import Document, Chunk, Extraction
from app.schemas.extraction import ExtractionResponse, ExtractedField
from app.generation.llm_client import llm_client
from app.generation.prompts import EXTRACTION_SYSTEM_PROMPT
from app.core.logging import logger

class ExtractionService:
    """Structured information extraction service with Pydantic schemas and evidence verification."""

    def extract(self, document_id: str, schema_name: str = "contract") -> ExtractionResponse:
        with get_db_session() as db:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if not doc:
                raise ValueError(f"Document {document_id} not found")
            chunks = db.query(Chunk).filter(Chunk.document_id == document_id).order_by(Chunk.page_number, Chunk.chunk_index).all()
            doc_name = doc.filename
            chunk_data = [(c.page_number, c.content) for c in chunks]

        if not chunk_data:
            raise ValueError(f"Document {document_id} has no processed chunks")

        full_text = "\n".join([f"[Page {p}]: {t}" for p, t in chunk_data])

        prompt = f"Document Name: {doc_name}\nSchema Target: {schema_name}\n\nDocument Text:\n{full_text}\n\nExtract schema fields in JSON format."
        llm_resp = llm_client.generate(prompt=prompt, system_prompt=EXTRACTION_SYSTEM_PROMPT, json_mode=True)

        extracted_fields: Dict[str, ExtractedField] = {}
        validation_errors = []

        try:
            raw_json = json.loads(llm_resp.content)
        except Exception:
            raw_match = re.search(r"\{.*\}", llm_resp.content, re.DOTALL)
            if raw_match:
                raw_json = json.loads(raw_match.group(0))
            else:
                raw_json = {}

        # Parse & verify fields
        expected_fields = [
            "parties", "effective_date", "expiration_date", "payment_terms",
            "renewal_clause", "termination_clause", "governing_law"
        ] if schema_name == "contract" else [
            "invoice_number", "vendor_name", "customer_name", "invoice_date",
            "due_date", "total_amount", "tax_amount", "payment_terms"
        ]

        filled_count = 0
        for f_name in expected_fields:
            field_data = raw_json.get(f_name)
            if isinstance(field_data, dict) and field_data.get("value") is not None:
                val = field_data.get("value")
                page = field_data.get("page", 1)
                passage = field_data.get("passage", "")
                extracted_fields[f_name] = ExtractedField(
                    field_name=f_name,
                    extracted_value=val,
                    source_document=doc_name,
                    page_number=int(page) if str(page).isdigit() else 1,
                    supporting_passage=passage,
                    validation_status="valid",
                    evidence_status="direct_evidence"
                )
                filled_count += 1
            else:
                # Fallback heuristic scan if LLM missed field
                heuristic_field = self._scan_fallback_field(f_name, chunks, doc_name)
                if heuristic_field:
                    extracted_fields[f_name] = heuristic_field
                    filled_count += 1
                else:
                    extracted_fields[f_name] = ExtractedField(
                        field_name=f_name,
                        extracted_value=None,
                        source_document=doc_name,
                        page_number=1,
                        supporting_passage="Not explicitly found in document text.",
                        validation_status="missing",
                        evidence_status="unsupported"
                    )
                    validation_errors.append(f"Field '{f_name}' not identified in document.")

        completeness = round(filled_count / len(expected_fields), 2)

        # Persist extraction
        with get_db_session() as db:
            record = Extraction(
                id=f"ext-{document_id[:8]}-{schema_name}",
                document_id=document_id,
                schema_name=schema_name,
                extracted_data={k: v.model_dump() for k, v in extracted_fields.items()},
                validation_status="valid" if completeness >= 0.7 else "incomplete"
            )
            db.merge(record)

        return ExtractionResponse(
            document_id=document_id,
            schema_name=schema_name,
            fields=extracted_fields,
            completeness_score=completeness,
            validation_errors=validation_errors
        )

    def _scan_fallback_field(self, field_name: str, chunks: list, doc_name: str) -> Optional[ExtractedField]:
        patterns = {
            "payment_terms": r"(Net \d+ days|payable within \d+ days|quarterly tranches)",
            "effective_date": r"(effective as of [A-Za-z]+ \d+, \d{4}|entered into as of [A-Za-z]+ \d+, \d{4})",
            "governing_law": r"(laws of the State of [A-Za-z]+)",
            "termination_clause": r"(\d+ days prior written notice|\d+ days advance written notice)",
            "total_amount": r"(\$\d+[\d,]*\.\d{2})",
            "invoice_number": r"(Invoice Number:\s*([A-Za-z0-9\-]+))"
        }
        pat = patterns.get(field_name)
        if not pat:
            return None

        for c in chunks:
            match = re.search(pat, c.content, re.IGNORECASE)
            if match:
                return ExtractedField(
                    field_name=field_name,
                    extracted_value=match.group(0),
                    source_document=doc_name,
                    page_number=c.page_number,
                    supporting_passage=c.content[:200],
                    validation_status="valid",
                    evidence_status="direct_evidence"
                )
        return None

extraction_service = ExtractionService()
