"""
generate_data.py - Reproducible Synthetic Student Coding Dataset Generator
===========================================================================
Generates a simulated dataset of student coding practice, lab engagement,
and performance tiers for the Code Roster project.

DISCLAIMER:
This dataset is synthetic and explicitly labeled as SIMULATED.
It does not represent real student telemetry or validate real-world ability.
It was generated because public datasets (e.g. Kaggle, UCI) either require private
credentials or only measure general secondary school demographics rather than
programming practice telemetry.
"""

import json
import os
import numpy as np
import pandas as pd


def generate_student_dataset(n_samples: int = 1500, random_seed: int = 42) -> pd.DataFrame:
    """
    Generates n_samples of student coding performance metrics with realistic correlations and noise.
    """
    np.random.seed(random_seed)

    # 1. Primary Language Distribution
    languages = ["Python", "Java", "C++", "JavaScript"]
    lang_weights = [0.45, 0.25, 0.20, 0.10]
    primary_language = np.random.choice(languages, size=n_samples, p=lang_weights)

    # 2. Daily Coding Hours (Log-normal distribution clipped to realistic student range [0.5, 8.0])
    raw_hours = np.random.lognormal(mean=0.8, sigma=0.5, size=n_samples)
    daily_coding_hours = np.clip(np.round(raw_hours, 1), 0.5, 8.0)

    # 3. Practice Consistency Streak (in days, linked partially to daily hours)
    streak_base = daily_coding_hours * 6.5 + np.random.normal(10, 8, size=n_samples)
    consistency_streak_days = np.clip(np.round(streak_base).astype(int), 1, 90)

    # 4. Total Algorithmic Problems Solved (correlated with daily hours and streak)
    problems_base = (daily_coding_hours * 35) + (consistency_streak_days * 2.2) + np.random.normal(30, 25, size=n_samples)
    problems_solved = np.clip(np.round(problems_base).astype(int), 5, 450)

    # 5. Submission Accuracy Percentage (35% to 98%, correlated with experience)
    accuracy_base = 50 + (problems_solved / 450.0) * 30 + np.random.normal(0, 8, size=n_samples)
    submission_accuracy = np.clip(np.round(accuracy_base, 1), 35.0, 98.0)

    # 6. Lab Assignments Completed (out of 15)
    assign_base = 4 + (daily_coding_hours / 8.0) * 8 + (consistency_streak_days / 90.0) * 3 + np.random.normal(0, 1.5, size=n_samples)
    assignments_completed = np.clip(np.round(assign_base).astype(int), 1, 15)

    # 7. Focus / Lab Attendance Score (1.0 to 10.0 scale)
    focus_base = 3.0 + (assignments_completed / 15.0) * 4.5 + (daily_coding_hours / 8.0) * 2.0 + np.random.normal(0, 0.8, size=n_samples)
    focus_score = np.clip(np.round(focus_base, 1), 1.0, 10.0)

    # 8. Composite Latent Proficiency Score with Gaussian noise
    # Normalized weights
    latent_score = (
        0.22 * (daily_coding_hours / 8.0) +
        0.25 * (problems_solved / 450.0) +
        0.20 * ((submission_accuracy - 35.0) / 63.0) +
        0.15 * (consistency_streak_days / 90.0) +
        0.18 * (assignments_completed / 15.0) +
        np.random.normal(0, 0.08, size=n_samples)
    )

    # 9. Categorize into 3 Performance Tiers
    # Needs Guidance (< 0.36), Competent (0.36 to 0.58), Exemplary (> 0.58)
    performance_tier = []
    for score in latent_score:
        if score < 0.36:
            performance_tier.append("Needs Guidance")
        elif score <= 0.58:
            performance_tier.append("Competent")
        else:
            performance_tier.append("Exemplary")

    df = pd.DataFrame({
        "student_id": [f"STU_{1000 + i}" for i in range(n_samples)],
        "daily_coding_hours": daily_coding_hours,
        "problems_solved": problems_solved,
        "submission_accuracy": submission_accuracy,
        "consistency_streak_days": consistency_streak_days,
        "assignments_completed": assignments_completed,
        "focus_score": focus_score,
        "primary_language": primary_language,
        "performance_tier": performance_tier
    })

    return df


def save_dataset_and_metadata(output_dir: str = "data"):
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "student_coding_roster.csv")
    meta_path = os.path.join(output_dir, "DATASET_METADATA.json")

    df = generate_student_dataset(n_samples=1500, random_seed=42)
    df.to_csv(csv_path, index=False)

    metadata = {
        "dataset_name": "Simulated Student Coding Practice & Productivity Telemetry",
        "is_synthetic": True,
        "status": "SIMULATED / SYNTHETIC",
        "license": "Creative Commons Attribution 4.0 International (CC BY 4.0) / MIT",
        "sample_size": len(df),
        "random_seed": 42,
        "date_created": "2024 / Academic Demo",
        "class_distribution": df["performance_tier"].value_counts().to_dict(),
        "features": {
            "daily_coding_hours": "Average active hours spent coding/practicing per day (0.5 - 8.0)",
            "problems_solved": "Total algorithmic/data structure challenges solved on platform (5 - 450)",
            "submission_accuracy": "Percentage of test cases passed on first 3 submissions (35.0% - 98.0%)",
            "consistency_streak_days": "Consecutive days with at least one active submission (1 - 90)",
            "assignments_completed": "Curriculum laboratory assignments submitted on time (1 - 15)",
            "focus_score": "Composite metric combining lab attendance and distraction index (1.0 - 10.0)",
            "primary_language": "Primary programming language track (Python, Java, C++, JavaScript)"
        },
        "target_variable": "performance_tier",
        "target_classes": ["Needs Guidance", "Competent", "Exemplary"],
        "justification": (
            "Public competition datasets (such as Kaggle Student Productivity) require authenticated credentials and API tokens. "
            "Public academic benchmarks (e.g., UCI Student Performance) record general secondary school demographics and alcohol consumption, "
            "not coding telemetry. CodeSearchNet is a code-docstring retrieval corpus without performance metrics. "
            "Hence, a fully reproducible, carefully controlled synthetic dataset was modeled to demonstrate end-to-end ML training."
        ),
        "ethical_disclaimer": (
            "This simulated dataset is designed strictly for educational demonstration. "
            "Measured test accuracy only reflects the mathematical data-generating process and does not validate real-world student abilities."
        )
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"Generated {len(df)} samples saved to {csv_path}")
    print(f"Class distribution:\n{df['performance_tier'].value_counts()}")
    print(f"Metadata saved to {meta_path}")


if __name__ == "__main__":
    save_dataset_and_metadata()
