# Evaluation Methodology & Empirical Benchmark

## 1. Evaluation Dataset Composition

The evaluation dataset (`evaluation/datasets/evaluation_dataset.json`) contains **52 verified ground-truth test cases** constructed across real commercial agreements and invoices:
- **42 Answerable Questions**: Fact-based questions testing exact clause extraction (payment terms, late fees, SLA uptime, dispute jurisdictions, termination notices, cure periods, invoice amounts, line items).
- **10 Unanswerable / Hallucination Trap Questions**: Out-of-domain, adversarial questions (e.g. quantum computing clauses, extraterrestrial mining, personal home addresses) designed to test the model's abstention discipline.

---

## 2. Metric Formulations

### 2.1 Retrieval Metrics
- **Hit Rate@5**: Percentage of queries where the expected document page appears in the top-5 retrieved chunks:
  $$\text{Hit Rate@5} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\text{target\_page}_i \in \text{retrieved\_pages}_{i, 1..5})$$
- **Mean Reciprocal Rank (MRR)**: Evaluates ranking position of the first correct passage:
  $$\text{MRR} = \frac{1}{N} \sum_{i=1}^N \frac{1}{\text{rank}_i}$$
- **Recall@5**: Fraction of relevant passages retrieved.
- **Precision@5**: Fraction of retrieved candidates that are directly relevant.

### 2.2 Generation & Factual Grounding Metrics
- **Citation Precision**: Proportion of citations in the generated answer that directly corroborate the claim with verified status:
  $$\text{Citation Precision} = \frac{|\text{Citations}_{\text{verified}}|}{|\text{Citations}_{\text{total}}|}$$
- **Citation Completeness**: Whether the expected source page is explicitly cited.
- **Abstention Accuracy**: Evaluates correct abstention on unanswerable queries and answering on answerable queries:
  $$\text{Abstention Accuracy} = \frac{1}{N} \sum_{i=1}^N \mathbb{I}(\text{is\_unanswerable}_i = \text{did\_abstain}_i)$$
- **Answer Correctness**: Token overlap between generated answer and ground-truth reference fact.

---

## 3. Measured Empirical Results

Executing `python scripts/run_evaluation.py` produces empirical results written to `evaluation/reports/EVALUATION_REPORT.md`:

```text
======================================================================
EVIDENCE-GROUNDED DOCUMENT INTELLIGENCE BENCHMARK RUNNER
======================================================================
Total Test Cases:            52
Hit Rate@5:                  100.0%
Mean Reciprocal Rank (MRR):  0.9071
Recall@5:                    100.0%
Precision@5:                 56.92%
----------------------------------------------------------------------
Answer Correctness:          78.85%
Citation Precision:          100.0%
Citation Completeness:       96.15%
Abstention Accuracy:         98.08%
----------------------------------------------------------------------
Mean Retrieval Latency:      6.31 ms
Mean Generation Latency:     56.01 ms
Total Benchmark Duration:    3.24 s
======================================================================
```
