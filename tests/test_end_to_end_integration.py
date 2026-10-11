"""
End-to-end integration tests verifying model persistence, prediction accuracy matching,
and full roasting pipeline across edge cases.
"""

import json
import joblib
import pandas as pd
import pytest

from code_analyzer import analyze_code
from roast_engine import generate_roast, PERSONAS


def test_model_matches_saved_evaluation_metrics():
    """Verify that loading the saved model from disk produces the exact test accuracy recorded in the report."""
    pipeline = joblib.load("models/best_student_performance_model.joblib")
    with open("models/model_metadata.json", "r", encoding="utf-8") as f:
        metadata = json.load(f)

    df = pd.read_csv("data/student_coding_roster.csv")
    features = metadata["numerical_features"] + metadata["categorical_features"]
    target = metadata["target_variable"]

    # Re-evaluate on test split using the exact same split parameters
    from sklearn.model_selection import train_test_split
    _, X_test, _, y_test = train_test_split(
        df[features], df[target], test_size=0.20, random_state=42, stratify=df[target]
    )

    y_pred = pipeline.predict(X_test)
    from sklearn.metrics import accuracy_score
    acc = accuracy_score(y_test, y_pred)

    assert round(acc, 4) == metadata["metrics"]["test_accuracy"]


def test_prediction_boundary_inputs():
    """Test boundary input values: minimum possible, average, and maximum possible."""
    pipeline = joblib.load("models/best_student_performance_model.joblib")

    boundaries = [
        # Minimum boundaries
        {
            "daily_coding_hours": 0.5,
            "problems_solved": 5,
            "submission_accuracy": 35.0,
            "consistency_streak_days": 1,
            "assignments_completed": 1,
            "focus_score": 1.0,
            "primary_language": "Python"
        },
        # Maximum boundaries
        {
            "daily_coding_hours": 8.0,
            "problems_solved": 450,
            "submission_accuracy": 98.0,
            "consistency_streak_days": 90,
            "assignments_completed": 15,
            "focus_score": 10.0,
            "primary_language": "C++"
        }
    ]

    for b in boundaries:
        df_input = pd.DataFrame([b])
        pred = pipeline.predict(df_input)
        probs = pipeline.predict_proba(df_input)

        assert pred[0] in ["Needs Guidance", "Competent", "Exemplary"]
        assert len(probs[0]) == 3


def test_all_personas_generate_distinct_roasts_for_same_issue():
    """Test that the 4 personas generate distinct responses for the exact same input code."""
    code = '''def solve(arr):
    for i in arr:
        for j in arr:
            pass
'''
    analysis = analyze_code(code)
    roasts = {}
    for persona in PERSONAS.keys():
        res = generate_roast(code, analysis, persona)
        roasts[persona] = res["roast_text"]
        assert "roast_text" in res
        assert "findings" in res
        assert "suggested_fix" in res
        assert len(res["findings"]) > 0

    # Ensure all roasts are distinct
    roast_texts = list(roasts.values())
    assert len(set(roast_texts)) == 4, "Each persona must generate uniquely phrased roast text."
