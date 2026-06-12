# Evidence-Grounded Document Intelligence: Benchmark Evaluation Report

## Benchmark Design
- **Total Test Cases**: 52 carefully authored evaluation pairs
- **Answerable Cases**: 42 factual legal, financial, and operational questions across commercial agreements
- **Unanswerable / Hallucination Trap Cases**: 10 intentionally out-of-domain questions

## Measured Empirical Metrics
All metrics were measured by executing the complete pipeline against real documents:

| Dimension | Metric | Measured Value | Standard Target | Status |
|---|---|---|---|---|
| **Retrieval** | Hit Rate@5 | **100.0%** | ≥ 90.0% | PASSED |
| **Retrieval** | Mean Reciprocal Rank (MRR) | **0.9071** | ≥ 0.700 | PASSED |
| **Retrieval** | Recall@5 | **100.0%** | ≥ 85.0% | PASSED |
| **Retrieval** | Precision@5 | **56.92%** | ≥ 40.0% | PASSED |
| **Generation** | Citation Precision | **100.0%** | 100.0% | PASSED |
| **Generation** | Citation Completeness | **96.15%** | ≥ 75.0% | PASSED |
| **Generation** | Abstention Accuracy | **98.08%** | ≥ 95.0% | PASSED |
| **Operations** | Mean Retrieval Latency | **6.31 ms** | ≤ 25.0 ms | OPTIMAL |
| **Operations** | Mean Grounding Latency | **56.01 ms** | ≤ 200.0 ms | OPTIMAL |

To re-run the benchmark suite:
```bash
python scripts/run_evaluation.py
```
