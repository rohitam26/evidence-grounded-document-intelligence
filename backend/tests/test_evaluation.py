import os
import json
import pytest
from app.evaluation.runner import evaluation_runner
from app.config import settings

def test_evaluation_suite_execution():
    summary = evaluation_runner.run_benchmark()
    assert summary["total_test_cases"] >= 50
    m = summary["metrics"]
    assert m["retrieval"]["hit_rate_at_5"] >= 80.0
    assert m["generation"]["citation_precision"] == 100.0
    assert m["generation"]["abstention_accuracy"] >= 85.0

    report_file = settings.EVALUATION_DIR / "reports" / "EVALUATION_REPORT.md"
    assert os.path.exists(report_file)
