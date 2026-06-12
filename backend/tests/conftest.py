import os
import sys
import pytest

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import create_app
from app.core.database import init_db
from app.ingestion.pipeline import ingestion_pipeline
from app.config import settings

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Ensure database schema is created and sample documents are indexed before tests run."""
    init_db()

    sample_files = [
        "acme_service_agreement.pdf",
        "beta_master_agreement.pdf",
        "acme_invoice_1042.pdf",
        "gamma_contract_amendment.docx"
    ]
    for fn in sample_files:
        path = os.path.join(settings.SAMPLE_DOCS_DIR, fn)
        if os.path.exists(path):
            ingestion_pipeline.process_file(file_path=path, filename=fn, user_id="test-user")

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
