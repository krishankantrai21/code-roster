"""
train_model.py - Supervised ML Training Pipeline for Student Performance Prediction
==================================================================================
Trains and compares:
1. Baseline: Decision Tree Classifier
2. Linear: Logistic Regression
3. Ensemble: Random Forest Classifier

Uses:
- Scikit-learn Pipeline and ColumnTransformer (prevents data leakage)
- Stratified 80/20 train/test split with fixed random seed (42)
- 5-Fold Stratified Cross-Validation
- Comprehensive evaluation: Accuracy, Macro Precision, Macro Recall, Macro F1
- Saves best model with joblib and full metadata in JSON
"""

import json
import os
import warnings
import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier


NUMERICAL_FEATURES = [
    "daily_coding_hours",
    "problems_solved",
    "submission_accuracy",
    "consistency_streak_days",
    "assignments_completed",
    "focus_score",
]

CATEGORICAL_FEATURES = ["primary_language"]

TARGET_COLUMN = "performance_tier"
CLASS_NAMES = ["Competent", "Exemplary", "Needs Guidance"]


def load_and_validate_data(data_path: str = "data/student_coding_roster.csv") -> pd.DataFrame:
    """Loads dataset and checks for missing values, duplicates, and class balance."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}. Run generate_data.py first.")

    df = pd.read_csv(data_path)
    print("=== DATA HEALTH CHECK ===")
    print(f"Total Rows: {len(df)}, Total Columns: {len(df.columns)}")

    missing_count = df.isnull().sum().sum()
    print(f"Missing Values: {missing_count}")
    if missing_count > 0:
        print("Handling missing values...")
        df = df.dropna()

    duplicate_count = df.duplicated().sum()
    print(f"Duplicate Rows: {duplicate_count}")
    if duplicate_count > 0:
        df = df.drop_duplicates()

    print("\nClass Distribution:")
    print(df[TARGET_COLUMN].value_counts(normalize=True).round(3))
    print("=========================\n")
    return df


def build_preprocessor() -> ColumnTransformer:
    """Builds a Scikit-learn ColumnTransformer for numerical and categorical features."""
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numerical_transformer, NUMERICAL_FEATURES),
            ("cat", categorical_transformer, CATEGORICAL_FEATURES),
        ]
    )
    return preprocessor


def train_and_evaluate(data_path: str = "data/student_coding_roster.csv"):
    """Executes the full ML pipeline, compares models, and saves the best model."""
    os.makedirs("models", exist_ok=True)
    os.makedirs("reports", exist_ok=True)

    df = load_and_validate_data(data_path)

    X = df[NUMERICAL_FEATURES + CATEGORICAL_FEATURES]
    y = df[TARGET_COLUMN]

    # 1. Stratified Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training Samples: {len(X_train)} | Test Samples: {len(X_test)}")

    preprocessor = build_preprocessor()

    # 2. Candidate Models
    candidate_models = {
        "Decision Tree (Baseline)": DecisionTreeClassifier(max_depth=4, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(
            n_estimators=100, max_depth=8, min_samples_split=4, random_state=42
        ),
    }

    comparison_results = []
    trained_pipelines = {}
    detailed_reports = {}

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    for name, model in candidate_models.items():
        print(f"\n--- Training & Cross-Validating: {name} ---")

        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])

        # 5-Fold Stratified Cross-Validation on Training data
        cv_f1_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="f1_macro")
        cv_acc_scores = cross_val_score(pipeline, X_train, y_train, cv=cv, scoring="accuracy")

        # Fit on entire training set
        pipeline.fit(X_train, y_train)
        trained_pipelines[name] = pipeline

        # Predict on held-out test set
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        macro_prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
        macro_rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
        macro_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)

        clf_rep = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_test, y_pred, labels=CLASS_NAMES)

        comparison_results.append({
            "model_name": name,
            "cv_f1_macro_mean": round(float(np.mean(cv_f1_scores)), 4),
            "cv_f1_macro_std": round(float(np.std(cv_f1_scores)), 4),
            "cv_acc_mean": round(float(np.mean(cv_acc_scores)), 4),
            "test_accuracy": round(float(acc), 4),
            "test_macro_precision": round(float(macro_prec), 4),
            "test_macro_recall": round(float(macro_rec), 4),
            "test_macro_f1": round(float(macro_f1), 4),
        })

        detailed_reports[name] = {
            "classification_report": clf_rep,
            "confusion_matrix": cm.tolist(),
            "labels": CLASS_NAMES,
        }

        print(
            f"CV Macro F1: {np.mean(cv_f1_scores):.4f} (+/- {np.std(cv_f1_scores):.4f}) | "
            f"Test Acc: {acc:.4f} | Test Macro F1: {macro_f1:.4f}"
        )

    # 3. Model Comparison Table
    comparison_df = pd.DataFrame(comparison_results)
    comparison_df.sort_values(by="test_macro_f1", ascending=False, inplace=True)
    comparison_csv_path = "reports/model_comparison.csv"
    comparison_json_path = "reports/model_comparison.json"
    comparison_df.to_csv(comparison_csv_path, index=False)
    with open(comparison_json_path, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=4)

    print("\n=== MODEL COMPARISON TABLE ===")
    print(comparison_df.to_string(index=False))

    # 4. Model Selection Criterion: Highest Test Macro F1-Score
    best_row = comparison_df.iloc[0]
    best_model_name = best_row["model_name"]
    best_pipeline = trained_pipelines[best_model_name]
    print(f"\nSelected Best Model: '{best_model_name}' (Test Macro F1: {best_row['test_macro_f1']})")

    # 5. Extract Feature Importance and Model Explainability
    rf_pipeline = trained_pipelines.get("Random Forest Classifier")
    num_names = NUMERICAL_FEATURES
    cat_encoder = best_pipeline.named_steps["preprocessor"].named_transformers_["cat"]
    cat_names = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    all_features = num_names + cat_names

    feature_importances = {}
    if rf_pipeline:
        rf_clf = rf_pipeline.named_steps["classifier"]
        importances = rf_clf.feature_importances_
        feature_importances = dict(
            sorted(
                {f: round(float(imp), 4) for f, imp in zip(all_features, importances)}.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )
        with open("reports/feature_importance.json", "w", encoding="utf-8") as f:
            json.dump(feature_importances, f, indent=4)

    # If best is Logistic Regression, extract multiclass coefficients
    model_coefficients = {}
    if "Logistic Regression" in best_model_name:
        lr_clf = best_pipeline.named_steps["classifier"]
        classes = list(lr_clf.classes_)
        for i, cls_name in enumerate(classes):
            coefs = lr_clf.coef_[i]
            model_coefficients[cls_name] = {f: round(float(c), 4) for f, c in zip(all_features, coefs)}
        with open("reports/model_coefficients.json", "w", encoding="utf-8") as f:
            json.dump(model_coefficients, f, indent=4)

    # 6. Save Model and Metadata
    model_save_path = "models/best_student_performance_model.joblib"
    joblib.dump(best_pipeline, model_save_path)
    print(f"Saved best model pipeline to {model_save_path}")

    # Metadata
    metadata = {
        "model_name": best_model_name,
        "selection_metric": "test_macro_f1",
        "best_metric_value": best_row["test_macro_f1"],
        "metrics": {
            "test_accuracy": best_row["test_accuracy"],
            "test_macro_precision": best_row["test_macro_precision"],
            "test_macro_recall": best_row["test_macro_recall"],
            "test_macro_f1": best_row["test_macro_f1"],
            "cv_f1_macro_mean": best_row["cv_f1_macro_mean"],
        },
        "target_variable": TARGET_COLUMN,
        "classes": CLASS_NAMES,
        "numerical_features": NUMERICAL_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "random_state": 42,
        "dataset_type": "Simulated Student Coding Telemetry",
        "feature_importances": feature_importances,
        "pipeline_stages": [
            "ColumnTransformer(StandardScaler for num, OneHotEncoder for cat)",
            best_model_name,
        ],
    }

    metadata_path = "models/model_metadata.json"
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    # Save detailed evaluation reports
    eval_report_path = "reports/evaluation_report.json"
    with open(eval_report_path, "w", encoding="utf-8") as f:
        json.dump(detailed_reports, f, indent=4)

    print(f"Model metadata saved to {metadata_path}")
    print(f"Detailed evaluation report saved to {eval_report_path}")
    print("\nTraining Pipeline Completed Successfully.")


if __name__ == "__main__":
    train_and_evaluate()
