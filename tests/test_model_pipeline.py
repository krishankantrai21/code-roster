"""
Unit tests for ML model loading, pipeline inference, and metadata verification.
"""

import json
import os
import joblib
import pandas as pd
import pytest


def test_artifacts_exist():
    assert os.path.exists("models/best_student_performance_model.joblib")
    assert os.path.exists("models/model_metadata.json")
    assert os.path.exists("reports/model_comparison.json")
    assert os.path.exists("reports/evaluation_report.json")
    assert os.path.exists("data/student_coding_roster.csv")


def test_model_inference():
    model_path = "models/best_student_performance_model.joblib"
    pipeline = joblib.load(model_path)

    sample_input = pd.DataFrame([{
        "daily_coding_hours": 3.5,
        "problems_solved": 200,
        "submission_accuracy": 78.5,
        "consistency_streak_days": 30,
        "assignments_completed": 10,
        "focus_score": 7.5,
        "primary_language": "Python"
    }])

    pred = pipeline.predict(sample_input)
    assert len(pred) == 1
    assert pred[0] in ["Competent", "Exemplary", "Needs Guidance"]

    probs = pipeline.predict_proba(sample_input)
    assert probs.shape == (1, 3)
    assert pytest.approx(probs.sum(), abs=1e-4) == 1.0


def test_metadata_consistency():
    with open("models/model_metadata.json", "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert "model_name" in meta
    assert "metrics" in meta
    assert meta["metrics"]["test_macro_f1"] > 0.5
    assert meta["target_variable"] == "performance_tier"
    assert len(meta["classes"]) == 3
