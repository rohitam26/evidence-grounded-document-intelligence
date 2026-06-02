from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field

class ExtractedField(BaseModel):
    field_name: str
    extracted_value: Optional[Union[str, float, int, List[str], Dict[str, Any]]] = None
    source_document: str
    page_number: int
    supporting_passage: str
    validation_status: str = "valid"  # valid, missing, unverified
    evidence_status: str = "direct_evidence"  # direct_evidence, inferred, unsupported

class ContractExtractionData(BaseModel):
    parties: Optional[ExtractedField] = None
    effective_date: Optional[ExtractedField] = None
    expiration_date: Optional[ExtractedField] = None
    payment_terms: Optional[ExtractedField] = None
    renewal_clause: Optional[ExtractedField] = None
    termination_clause: Optional[ExtractedField] = None
    governing_law: Optional[ExtractedField] = None

class InvoiceExtractionData(BaseModel):
    invoice_number: Optional[ExtractedField] = None
    vendor_name: Optional[ExtractedField] = None
    customer_name: Optional[ExtractedField] = None
    invoice_date: Optional[ExtractedField] = None
    due_date: Optional[ExtractedField] = None
    total_amount: Optional[ExtractedField] = None
    tax_amount: Optional[ExtractedField] = None
    payment_terms: Optional[ExtractedField] = None

class ExtractionRequest(BaseModel):
    document_id: str
    schema_name: str = Field(default="contract", description="contract or invoice")

class ExtractionResponse(BaseModel):
    document_id: str
    schema_name: str
    fields: Dict[str, ExtractedField]
    completeness_score: float
    validation_errors: List[str] = []
