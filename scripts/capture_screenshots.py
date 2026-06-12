import os
import sys
import time
import subprocess
import httpx
from playwright.sync_api import sync_playwright

REPO_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCREENSHOTS_DIR = os.path.join(REPO_DIR, "docs", "screenshots")

def wait_for_url(url: str, timeout: float = 30.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            r = httpx.get(url, timeout=2.0)
            if r.status_code < 400:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False

def clean_screenshots_dir():
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    for f in os.listdir(SCREENSHOTS_DIR):
        if f.endswith(".png"):
            os.remove(os.path.join(SCREENSHOTS_DIR, f))

def ensure_sample_documents_indexed():
    print("[*] Ensuring sample documents are indexed via clean subprocess...")
    cmd = [sys.executable, "-c", "import sys; sys.path.insert(0, 'backend'); from app.core.database import init_db; from app.ingestion.pipeline import ingestion_pipeline; from app.config import settings; import os; init_db(); [ingestion_pipeline.process_file(os.path.join(settings.SAMPLE_DOCS_DIR, fn), fn, 'screenshot-user') for fn in ['acme_service_agreement.pdf', 'beta_master_agreement.pdf', 'acme_invoice_1042.pdf', 'gamma_contract_amendment.docx']]"]
    subprocess.run(cmd, cwd=REPO_DIR, capture_output=True)

def main():
    print("[*] Starting backend and frontend services for screenshot capture...")
    clean_screenshots_dir()
    ensure_sample_documents_indexed()

    # 1. Start Backend
    backend_env = os.environ.copy()
    backend_env["PYTHONPATH"] = os.path.join(REPO_DIR, "backend")
    backend_proc = subprocess.Popen(
        [sys.executable, "backend/app/main.py"],
        cwd=REPO_DIR,
        env=backend_env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # 2. Start Frontend Dev Server
    frontend_proc = subprocess.Popen(
        "npm run dev -- --port 5173",
        cwd=os.path.join(REPO_DIR, "frontend"),
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    try:
        print("[*] Waiting for backend (http://localhost:5000/health)...")
        if not wait_for_url("http://localhost:5000/health", 25.0):
            raise RuntimeError("Backend failed to start on http://localhost:5000")

        print("[*] Waiting for frontend (http://localhost:5173)...")
        if not wait_for_url("http://localhost:5173", 25.0):
            raise RuntimeError("Frontend failed to start on http://localhost:5173")

        print("[*] Launching Chrome via Playwright...")
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="chrome", headless=True)
            context = browser.new_context(
                viewport={"width": 1440, "height": 900},
                device_scale_factor=1.5
            )
            page = context.new_page()

            # 1. Application Dashboard
            print("[1/11] Capturing 01-dashboard.png...")
            page.goto("http://localhost:5173")
            page.wait_for_selector("text=System Intelligence Dashboard", timeout=15000)
            page.wait_for_selector("text=Recent Document Pipeline", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "01-dashboard.png"))

            # 2. Document Library
            print("[2/11] Capturing 02-document-library.png...")
            page.click("text=Documents")
            page.wait_for_selector("text=Document Workspace", timeout=15000)
            page.wait_for_selector("text=acme_service_agreement.pdf", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "02-document-library.png"))

            # 3. Document Detail & Layout Inspection
            print("[3/11] Capturing 03-document-inspection.png...")
            page.locator("text=acme_service_agreement.pdf").first.click()
            page.wait_for_selector("text=SHA-256 Hash:", timeout=15000)
            page.wait_for_selector("text=Layout Chunks Sample", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "03-document-inspection.png"))

            # 4. AI Search with Hybrid Retrieval Results
            print("[4/11] Capturing 04-ai-search.png...")
            page.click("text=AI Search")
            page.wait_for_selector("input[placeholder*='Search across all contracts']", timeout=15000)
            search_input = page.locator("input[placeholder*='Search across all contracts']")
            search_input.fill("monthly fixed subscription rate Net 30 payment terms")
            search_input.press("Enter")
            page.wait_for_timeout(2500)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "04-ai-search.png"))

            # 5. Evidence Chat with Verified Citations
            print("[5/11] Capturing 05-evidence-chat.png...")
            page.click("text=Evidence Chat")
            page.wait_for_selector("input[placeholder*='Ask a question']", timeout=15000)
            chat_input = page.locator("input[placeholder*='Ask a question']")
            chat_input.fill("What is the fixed monthly subscription rate and payment terms under the Acme contract?")
            chat_input.press("Enter")
            page.wait_for_timeout(3500)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "05-evidence-chat.png"))

            # 6. Structured Information Extraction Studio
            print("[6/11] Capturing 06-structured-extraction.png...")
            page.click("text=Extraction Studio")
            page.wait_for_selector("button:has-text('Extract Entities')", timeout=15000)
            page.click("button:has-text('Extract Entities')")
            page.wait_for_selector("text=Extracted Entities", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "06-structured-extraction.png"))

            # 7. Multi-Document Comparison Studio
            print("[7/11] Capturing 07-document-comparison.png...")
            page.click("text=Doc Comparison")
            page.wait_for_selector("button:has-text('Run Audit')", timeout=15000)
            page.click("button:has-text('Run Audit')")
            page.wait_for_selector("text=Cross-Document Audit Report", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "07-document-comparison.png"))

            # 8. Autonomous Agent Workflow
            print("[8/11] Capturing 08-agent-workflow.png...")
            page.click("text=Autonomous Agent")
            page.wait_for_selector("button:has-text('Execute Workflow')", timeout=15000)
            page.click("button:has-text('Execute Workflow')")
            page.wait_for_selector("text=Execution Trace", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "08-agent-workflow.png"))

            # 9. Evaluation Dashboard
            print("[9/11] Capturing 09-evaluation-dashboard.png...")
            page.click("text=Evaluation & Benchmarks")
            page.wait_for_selector("text=RAG Evaluation & Benchmark Suite", timeout=15000)
            page.wait_for_selector("text=Hit Rate@5", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "09-evaluation-dashboard.png"))

            # 10. System Configuration & Settings
            print("[10/11] Capturing 10-system-settings.png...")
            page.click("text=Settings")
            page.wait_for_selector("text=System & Runtime Settings", timeout=15000)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "10-system-settings.png"))

            # 11. Interactive Swagger UI API Explorer
            print("[11/11] Capturing 11-api-swagger-docs.png...")
            page.goto("http://localhost:5000/api/v1/docs")
            page.wait_for_selector("#swagger-ui", timeout=10000)
            page.wait_for_timeout(2500)
            page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "11-api-swagger-docs.png"))

            browser.close()
            print("[✓] All 11 distinct, genuine screenshots captured successfully!")

    finally:
        print("[*] Terminating processes...")
        try:
            backend_proc.terminate()
        except Exception:
            pass
        try:
            frontend_proc.terminate()
        except Exception:
            pass

if __name__ == "__main__":
    main()
