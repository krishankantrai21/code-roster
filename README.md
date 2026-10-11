# 💻 Code Roster: ML-Based Student Coding Platform & AI Assistant

> **B.Tech Computer Science & Engineering — Major / Capstone Project Prototype**  
> *Developed as a dual-engine platform combining Supervised Machine Learning for student productivity prediction and Abstract Syntax Tree (AST) static code roasting.*

---

## 📌 1. Project Motivation & Objectives

Computer Science students often struggle with two fundamental challenges during their coding journey:
1. **Lack of Performance Telemetry & Foresight:** Students practice irregularly across competitive coding platforms and lab coursework without knowing whether their current engagement pattern will lead to course mastery or placement readiness.
2. **Impersonal, Boring Code Feedback:** Standard IDE compiler errors or linters are dry and uninspiring, discouraging beginners from iteratively debugging and refactoring anti-patterns.

**Code Roster** bridges this gap by providing:
- **A Supervised Machine Learning Model** that forecasts student coding performance tiers (`Needs Guidance`, `Competent`, `Exemplary`) using practice telemetry, providing personalized recommendations.
- **An Interactive Code Roast System** with 4 distinct personas (*Best Friend*, *Strict Manager*, *Professor*, *Savage*) that makes static code review fun, educational, and constructive.
- **A Modern Streamlit Dashboard** featuring real-time predictions, transparent evaluation metrics (Plotly confusion matrices, ROC/F1 benchmarks), and safe static AST parsing.

---

## 🏛️ 2. System Architecture & Workflow

The platform follows a strictly modular, decoupled dual-engine architecture:

```
                          ┌──────────────────────────────────────────────┐
                          │         Code Roster Web Application          │
                          │             (Streamlit Dashboard)            │
                          └──────┬────────────────────────────────┬──────┘
                                 │                                │
                 [Telemetry Data Inputs]                 [Python Code Input]
                                 │                                │
                                 ▼                                ▼
              ┌──────────────────────────────────────┐  ┌───────────────────────────────────┐
              │     Predictive Machine Learning      │  │        Static Code Roast          │
              │             Engine (ML)              │  │          Engine (AST)             │
              ├──────────────────────────────────────┤  ├───────────────────────────────────┤
              │ • 1,500 Telemetry Records            │  │ • Python Standard Library `ast`   │
              │ • ColumnTransformer Preprocessor     │  │ • NodeVisitor Traversal Rules     │
              │   (StandardScaler + OneHotEncoder)   │  │ • Cautious Big-O Bounds Estimator │
              │ • Trained Logistic Regression        │  │ • Zero `eval()` / `exec()` calls  │
              │   Pipeline (Joblib Artifact)         │  │ • 4 Persona Roast Adapters        │
              └──────────────────┬───────────────────┘  └─────────────────┬─────────────────┘
                                 │                                        │
                                 ▼                                        ▼
                   [Performance Tier Badge,                 [The Roast, Issue Badges,
                   Probabilities & Action Plan]             & Refactored Suggested Fix]
```

### Critical Architectural Distinction: ML vs. Rule-Based Analysis
| Feature Component | Underlying Mechanism | Learning Paradigm | Determinism |
| :--- | :--- | :--- | :--- |
| **Student Tier Predictor** | Scikit-learn Pipeline (Logistic Regression) | **Supervised Machine Learning** ($X \to y$) | Probabilistic ($P(\text{class} \mid X)$) |
| **Code Roast & Linter** | Python Standard Library `ast` Module | **Rule-Based Deterministic Grammar Parsing** | 100% Deterministic & Safe |

---

## 📂 3. Repository Directory Structure

```text
code roster/
├── app.py                     # Main Streamlit web dashboard (5 interactive tabs)
├── generate_data.py           # Reproducible synthetic student telemetry generator
├── train_model.py             # Supervised ML training, 5-fold CV & evaluation pipeline
├── code_analyzer.py           # AST-based static code analyzer & cautious complexity checker
├── roast_engine.py            # Persona-driven humorous roast generator (4 personas)
├── requirements.txt           # Python dependency specifications
├── README.md                  # Complete architectural & viva documentation
├── PRESENTATION_AND_VIVA.md   # 10-slide presentation deck & viva Q&A guide
├── data/
│   ├── student_coding_roster.csv   # Generated dataset (1,500 samples, 9 columns)
│   └── DATASET_METADATA.json       # Dataset provenance, schema & ethical disclosure
├── models/
│   ├── best_student_performance_model.joblib # Saved trained scikit-learn pipeline
│   └── model_metadata.json                  # Model hyperparams, classes & metrics
├── reports/
│   ├── model_comparison.csv       # Benchmark comparison table (DT vs LR vs RF)
│   ├── model_comparison.json      # Structured benchmark data
│   ├── evaluation_report.json     # Detailed classification reports & confusion matrices
│   ├── feature_importance.json    # Random Forest feature importance rankings
│   └── model_coefficients.json    # Logistic Regression class coefficients
└── tests/
    ├── conftest.py                # Pytest configuration & sys.path setup
    ├── test_code_analyzer.py      # Unit tests for AST parsing & issue rules
    ├── test_roast_engine.py       # Unit tests for 4 personas & output structure
    ├── test_model_pipeline.py     # Unit tests for model loading & schema inference
    └── test_end_to_end_integration.py # Integration tests for boundary inputs & metrics
```

---

## 📊 4. Dataset Source, License & Preprocessing

### Dataset Transparency Disclosure
- **Dataset Nature:** Explicitly labeled as **SIMULATED / SYNTHETIC**.
- **Sample Count:** 1,500 student records.
- **License:** Open Educational Resource (OER) / MIT License.
- **Why Synthetic Data Was Selected:**
  1. **Kaggle Student Productivity Challenges:** Require authenticated private API tokens (`kaggle.json`) or manual web logins, making automated reproduction impossible without user credentials.
  2. **CodeSearchNet:** Is a code-to-docstring search corpus (~20GB) with **no** labels for code bugs, runtime complexity, or student grades.
  3. **UCI Student Performance Benchmark:** Only captures high school secondary school math/language grades and family alcohol consumption, rather than programming telemetry (git commits, daily coding hours, test cases passed).
- **Ethical AI Disclaimer:** *This dataset is designed for educational demonstration. The measured test accuracy reflects the simulated data-generating process and does not establish real-world predictive validity on actual human students.*

### Feature Schema & Data Dictionary

| Feature Name | Data Type | Range | Description |
| :--- | :--- | :--- | :--- |
| `student_id` | String | `STU_1000`–`STU_2499` | Unique anonymized student identifier |
| `daily_coding_hours` | Float | 0.5 – 8.0 hrs | Active hours spent coding/practicing per day |
| `problems_solved` | Integer | 5 – 450 | Total algorithmic challenges solved on platform |
| `submission_accuracy` | Float | 35.0% – 98.0% | Percentage of test cases passed on first 3 tries |
| `consistency_streak_days` | Integer | 1 – 90 days | Consecutive days maintaining active submissions |
| `assignments_completed`| Integer | 1 – 15 | Lab assignments completed on time (out of 15) |
| `focus_score` | Float | 1.0 – 10.0 | Composite lab attendance & distraction index |
| `primary_language` | Category | Python, Java, C++, JS | Primary programming curriculum track |
| **`performance_tier`** *(Target)* | Category | 3 Classes | `Needs Guidance` (45.5%), `Competent` (44.9%), `Exemplary` (9.7%) |

### Preprocessing & Data Leakage Prevention
Preprocessing is encapsulated inside a Scikit-learn `Pipeline` using `ColumnTransformer`:
- **Numerical Features (6):** Standardized using `StandardScaler` ($\mu=0, \sigma=1$).
- **Categorical Feature (1):** One-hot encoded using `OneHotEncoder(handle_unknown='ignore')`.
- **Strict Leakage Guard:** The transformer is fitted **strictly on the training split (`X_train`)** during cross-validation and final training. The test split (`X_test`) is only transformed.

---

## 🤖 5. Machine Learning Pipeline & Benchmark Results

### Experimental Setup
- **Train/Test Split:** 80% Train (1,200 samples), 20% Test (300 samples)
- **Stratification:** Enabled on `performance_tier` to preserve class ratios.
- **Random Seed:** Fixed seed `random_state=42` across all splits and algorithms.
- **Cross-Validation:** 5-Fold Stratified K-Fold CV on training split.
- **Champion Selection Metric:** **Test Macro F1-Score** (treats all classes equally, preventing majority class bias).

### Actual Measured Model Benchmark Results

| Model Algorithm | CV Macro F1 (Mean ± Std) | CV Accuracy | Test Accuracy | Test Macro Precision | Test Macro Recall | **Test Macro F1 (Selection Metric)** |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression (Selected)** | **0.7167 ± 0.0223** | **0.7308** | **0.7567 (75.7%)** | **0.7714** | **0.7119** | **0.7356** |
| Random Forest Classifier | 0.7137 ± 0.0189 | 0.7308 | 0.7267 (72.7%) | 0.7501 | 0.6898 | 0.7139 |
| Decision Tree (Baseline) | 0.6906 ± 0.0343 | 0.7092 | 0.7200 (72.0%) | 0.7356 | 0.6760 | 0.6987 |

### Why Logistic Regression Outperformed the Decision Tree
1. The simulated proficiency target is generated from a linear composite function with additive Gaussian noise.
2. Logistic Regression forms continuous hyperplane boundaries, which naturally model smooth transitions between student performance tiers better than axis-aligned orthogonal splits of shallow Decision Trees.

### Feature Importances (Random Forest Gini Impurity)
1. `problems_solved` (31.4%)
2. `daily_coding_hours` (24.8%)
3. `submission_accuracy` (18.6%)
4. `assignments_completed` (14.2%)
5. `consistency_streak_days` (8.1%)
6. `focus_score` (2.5%)
7. `primary_language` (< 0.5% — confirms algorithmic dedication matters more than language choice)

---

## 🔥 6. Code Roast: Personas & Static Analysis Engine

### Selectable Personas
Users select from 4 distinct personas via the selector **"How do you want to roast?"**:
1. 🤝 **Best Friend:** Friendly, casual Hinglish, funny teasing (*"Bhai, CPU ko overtime ka form bharwa diya kya? 😂"*).
2. 👔 **Strict Manager:** Professional, sarcastic, corporate SLA-obsessed (*"Potential O(n²) bottleneck detected. Please justify the runtime cost before merging."*).
3. 👨‍🏫 **Professor:** Pedagogical, fundamentals-driven, viva-style grilling (*"Nested loops dikh rahe hain. Explain how both loop bounds scale with input size."*).
4. 🔥 **Savage:** High-voltage wit, sharp punchlines, constructive yet roasting (*"Tere code ko input do aur CPU overtime ka form bharne lagta hai. 💀"*).

### Static Analysis Safety & Heuristic Rules
- **100% Static:** Code is converted into an Abstract Syntax Tree using `ast.parse()`. Arbitrary code is **NEVER executed**.
- **Detected Anti-Patterns:**
  - `SYNTAX_001`: Syntax errors with line, column, and exact grammar failure.
  - `PERF_001`: Nested loops with cautious Big-O caveats (distinguishes scaling loops from constant ranges).
  - `PERF_002`: Repeated quadratic string concatenation (`s += ...` inside loop bodies).
  - `PERF_003`: O(n) calls like `.index()` or `.count()` inside loops yielding O(n²).
  - `BUG_001`: Mutable default arguments (`def fn(lst=[]):`).
  - `BUG_002`: Potential infinite loops (`while True:` without break).
  - `BUG_003`/`BUG_004`: Bare `except:` or silent exception swallowing (`except: pass`).
  - `STYLE_001`–`STYLE_003`: Non-snake_case functions, `== None`, and `== True` comparisons.
- **Suggested Fix Generator:** Produces safe, idiomatic refactored Python snippets.

---

## 🚀 7. Installation & Execution Guide

### Prerequisites
- Python 3.9+ (Python 3.9, 3.10, 3.11, or 3.12 supported).
- Any standard Windows, macOS, or Linux laptop (No GPU required).

### Windows Setup Instructions (PowerShell / Command Prompt)

```powershell
# 1. Open Terminal and navigate to the project directory
cd "code roster"

# 2. Create a virtual environment
python -m venv venv

# 3. Activate the virtual environment
.\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate the synthetic dataset
python generate_data.py

# 6. Train the ML models and generate evaluation reports
python train_model.py

# 7. Run the automated test suite (27 unit & integration tests)
pytest -v tests/

# 8. Launch the Streamlit dashboard
streamlit run app.py
```

### macOS / Linux Setup Instructions (Terminal / Bash / Zsh)

```bash
# 1. Open Terminal and navigate to the project directory
cd "code roster"

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Generate the synthetic dataset
python3 generate_data.py

# 6. Train the ML models and generate evaluation reports
python3 train_model.py

# 7. Run the automated test suite (27 unit & integration tests)
pytest -v tests/

# 8. Launch the Streamlit dashboard
streamlit run app.py
```

After launching, open your browser at: **`http://localhost:8501`**

---

## 🧪 8. Automated Testing & Reliability

The project includes 27 comprehensive automated tests across 4 test suites:
- `tests/test_code_analyzer.py`: Validates syntax errors, nested loops, mutable defaults, and fix generation.
- `tests/test_roast_engine.py`: Validates distinct persona output across syntax errors, clean code, and bugs.
- `tests/test_model_pipeline.py`: Validates Joblib artifact loading, inference probability shapes, and metadata.
- `tests/test_end_to_end_integration.py`: Validates boundary inputs and verifies test accuracy exactly matches reports.

Run tests anytime with:
```bash
pytest -v tests/
```
*Current test status: 27/27 PASSED (100% passing).*

---

## ⚠️ 9. Known Limitations & Future Scope

1. **Complexity Inference Limitations:** Static AST analysis inspects loop depth, but cannot deduce dynamic bounds without symbolic mathematical solvers or runtime profilers.
2. **Simulated Telemetry:** Does not incorporate qualitative code review feedback, peer discussions, or Git commit messages.
3. **Future Work:**
   - Add dynamic runtime CPU/Memory micro-benchmarking using `tracemalloc` and `cProfile`.
   - Webhook integration with GitHub Classroom and LeetCode APIs for automated student synchronization.
   - Optional fine-tuned local Small Language Model (SLM) for interactive semantic code repair.
