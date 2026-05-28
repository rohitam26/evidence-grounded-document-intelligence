import os
import pytest
from app.ingestion.parser import document_parser
from app.ingestion.chunker import chunker
from app.ingestion.pipeline import ingestion_pipeline
from app.config import settings
from app.core.database import init_db, get_db_session
from app.models import User

@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    init_db()
    with get_db_session() as db:
        test_user = db.query(User).filter(User.id == "test-user-id").first()
        if not test_user:
            db.add(User(
                id="test-user-id",
                email="test@papertrail.local",
                username="testengineer",
                hashed_password="fakehashedpassword"
            ))

def test_parse_pdf():
    pdf_path = os.path.join(settings.SAMPLE_DOCS_DIR, "acme_service_agreement.pdf")
    assert os.path.exists(pdf_path)
    blocks = document_parser.parse(pdf_path, ".pdf")
    assert len(blocks) > 0
    pages = {b.page_number for b in blocks}
    assert 1 in pages
    assert 2 in pages
    assert any("MASTER SERVICES AGREEMENT" in b.text for b in blocks)

def test_parse_docx():
    docx_path = os.path.join(settings.SAMPLE_DOCS_DIR, "gamma_contract_amendment.docx")
    assert os.path.exists(docx_path)
    blocks = document_parser.parse(docx_path, ".docx")
    assert len(blocks) > 0
    assert any("RENEWAL CLAUSE" in b.text for b in blocks)

def test_structure_aware_chunker():
    pdf_path = os.path.join(settings.SAMPLE_DOCS_DIR, "acme_service_agreement.pdf")
    blocks = document_parser.parse(pdf_path, ".pdf")
    chunks = chunker.chunk_document(blocks, "doc-123", "acme_service_agreement.pdf")
    assert len(chunks) > 0
    first_chunk = chunks[0]
    assert first_chunk.document_id == "doc-123"
    assert first_chunk.page_number in [1, 2]
    assert first_chunk.content_hash is not None
    assert len(first_chunk.content_hash) == 64

def test_ingestion_pipeline():
    pdf_path = os.path.join(settings.SAMPLE_DOCS_DIR, "acme_service_agreement.pdf")
    res = ingestion_pipeline.process_file(
        file_path=pdf_path,
        filename="acme_service_agreement.pdf",
        user_id="test-user-id"
    )
    assert res["status"] in ["completed", "duplicate"]
    assert "document_id" in res
