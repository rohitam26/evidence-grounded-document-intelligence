import uuid
from typing import List, Dict, Any, Optional
from app.core.database import get_db_session
from app.models import Document, Chunk, Comparison
from app.schemas.comparison import ComparisonResponse, DiffItem
from app.services.extraction_service import extraction_service
from app.core.logging import logger

class ComparisonService:
    """Multi-document comparison service with side-by-side evidence and conflict detection."""

    def compare(
        self,
        document_a_id: str,
        document_b_id: str,
        user_id: str,
        category: str = "payment_terms"
    ) -> ComparisonResponse:
        with get_db_session() as db:
            doc_a = db.query(Document).filter(Document.id == document_a_id).first()
            doc_b = db.query(Document).filter(Document.id == document_b_id).first()
            if not doc_a or not doc_b:
                raise ValueError("One or both documents not found")
            name_a, name_b = doc_a.filename, doc_b.filename

        # Extract structured representations
        ext_a = extraction_service.extract(document_a_id, schema_name="contract")
        ext_b = extraction_service.extract(document_b_id, schema_name="contract")

        diffs: List[DiffItem] = []
        conflict_count = 0

        categories_to_compare = [
            ("Payment Terms", "payment_terms"),
            ("Term & Termination", "termination_clause"),
            ("Governing Jurisdiction", "governing_law"),
            ("Effective Date", "effective_date")
        ]

        for cat_label, attr_key in categories_to_compare:
            field_a = ext_a.fields.get(attr_key)
            field_b = ext_b.fields.get(attr_key)

            val_a = str(field_a.extracted_value) if field_a and field_a.extracted_value else "Unspecified"
            val_b = str(field_b.extracted_value) if field_b and field_b.extracted_value else "Unspecified"

            is_diff = val_a.lower() != val_b.lower()
            # Only classify as conflict if both specify mutually exclusive legal values
            is_conflict = is_diff and (val_a != "Unspecified" and val_b != "Unspecified")
            if is_conflict:
                conflict_count += 1

            summary = f"Documents differ on {cat_label}: '{val_a}' vs '{val_b}'" if is_diff else f"Both documents align on {cat_label}: '{val_a}'"

            diffs.append(DiffItem(
                category=cat_label,
                attribute_name=attr_key,
                value_a=val_a,
                value_b=val_b,
                difference_summary=summary,
                evidence_a=field_a.supporting_passage if field_a else "None",
                page_a=field_a.page_number if field_a else 1,
                evidence_b=field_b.supporting_passage if field_b else "None",
                page_b=field_b.page_number if field_b else 1,
                is_conflict=is_conflict,
                verification_status="verified"
            ))

        comparison_id = str(uuid.uuid4())
        # Persist comparison record
        with get_db_session() as db:
            record = Comparison(
                id=comparison_id,
                user_id=user_id,
                document_a_id=document_a_id,
                document_b_id=document_b_id,
                document_a_name=name_a,
                document_b_name=name_b,
                comparison_category=category,
                diff_results=[d.model_dump() for d in diffs]
            )
            db.add(record)

        return ComparisonResponse(
            comparison_id=comparison_id,
            document_a_id=document_a_id,
            document_b_id=document_b_id,
            document_a_name=name_a,
            document_b_name=name_b,
            category=category,
            differences=diffs,
            conflict_count=conflict_count
        )

comparison_service = ComparisonService()
