"""
CLI Entry Point to execute the Evidence-Grounded Document Intelligence Evaluation Benchmark.
Usage: python scripts/run_evaluation.py
"""
import sys
import os

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.evaluation.runner import evaluation_runner
from app.ingestion.pipeline import ingestion_pipeline
from app.config import settings

def ensure_documents_indexed():
    print("[*] Verifying sample documents in index...")
    sample_files = [
        "acme_service_agreement.pdf",
        "beta_master_agreement.pdf",
        "acme_invoice_1042.pdf",
        "gamma_contract_amendment.docx"
    ]
    for fn in sample_files:
        path = os.path.join(settings.SAMPLE_DOCS_DIR, fn)
        if os.path.exists(path):
            res = ingestion_pipeline.process_file(file_path=path, filename=fn, user_id="eval-user")
            print(f"  ✓ Indexed: {fn} -> status: {res.get('status')}")

def main():
    print("=" * 70)
    print("EVIDENCE-GROUNDED DOCUMENT INTELLIGENCE BENCHMARK RUNNER")
    print("=" * 70)
    ensure_documents_indexed()
    print("\n[*] Executing 52-Question Benchmark Suite...")
    summary = evaluation_runner.run_benchmark()
    m = summary["metrics"]

    print("\n" + "=" * 70)
    print("MEASURED EVALUATION RESULTS")
    print("=" * 70)
    print(f"Total Test Cases:            {summary['total_test_cases']}")
    print(f"Hit Rate@5:                  {m['retrieval']['hit_rate_at_5']}%")
    print(f"Mean Reciprocal Rank (MRR):  {m['retrieval']['mean_reciprocal_rank']}")
    print(f"Recall@5:                    {m['retrieval']['recall_at_5']}%")
    print(f"Precision@5:                 {m['retrieval']['precision_at_5']}%")
    print("-" * 70)
    print(f"Answer Correctness:          {m['generation']['answer_correctness']}%")
    print(f"Citation Precision:          {m['generation']['citation_precision']}%")
    print(f"Citation Completeness:       {m['generation']['citation_completeness']}%")
    print(f"Abstention Accuracy:         {m['generation']['abstention_accuracy']}%")
    print("-" * 70)
    print(f"Mean Retrieval Latency:      {m['operations']['mean_retrieval_latency_ms']} ms")
    print(f"Mean Generation Latency:     {m['operations']['mean_generation_latency_ms']} ms")
    print(f"Total Benchmark Duration:    {m['operations']['total_benchmark_duration_sec']} s")
    print("=" * 70)
    print("Benchmark complete! Full report generated at: evaluation/reports/EVALUATION_REPORT.md")

if __name__ == "__main__":
    main()
