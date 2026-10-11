# 🎓 Code Roster: Presentation Outline & Viva Voce Guide

> **Prepared for B.Tech Computer Science & Engineering Final Project Evaluation & Viva**  
> *Project Name:* **Code Roster — ML-Based Student Coding Platform & AI Assistant**  
> *Author:* Student (Beginner-Friendly Explanation Guide)

---

# PART I: 10-SLIDE PRESENTATION OUTLINE

---

### Slide 1: Title & Problem Statement
- **Title:** Code Roster — An ML-Driven Student Coding Telemetry Platform & Persona-Based Code Assistant
- **Subtitle:** B.Tech Major Project Defense
- **Problem Statement:**
  - Modern CS curricula require intense programming practice across multiple platforms.
  - Students lack continuous, objective insight into whether their daily coding habits align with placement readiness.
  - Conventional linters provide dry, sterile compiler errors that students often ignore, failing to learn good coding practices.
- **Speaker Note:**  
  *"Good morning respected examiners. Today I present Code Roster, an intelligent coding platform designed to solve two core issues: predicting student coding performance using machine learning and offering engaging, educational feedback through persona-driven code roasting."*

---

### Slide 2: Motivation
- **The Telemetry Blind Spot:** Students solve problems intermittently without tracking metrics like consistency streaks or accuracy decay.
- **Pedagogical Engagement Gap:** Standard static analyzers (like Flake8 or Pylint) output robotic warnings. Gamifying feedback through selectable personas makes learning stick.
- **Educational Prototype Goal:** Build a runnable, transparent system that demonstrates the complete end-to-end Machine Learning lifecycle without black-box APIs.
- **Speaker Note:**  
  *"Our motivation was to build a tool that acts as both an objective academic coach and an entertaining peer reviewer, bridging the gap between classroom theory and real software development habits."*

---

### Slide 3: Proposed Solution
- **Component 1: ML Performance Predictor:**
  - Supervised multi-class classification predicting 3 mastery tiers (`Needs Guidance`, `Competent`, `Exemplary`).
  - Delivers real-time class probabilities and actionable recommendations.
- **Component 2: Interactive Code Roast:**
  - Python AST-based static analyzer with 4 selectable roasting personas (*Best Friend*, *Strict Manager*, *Professor*, *Savage*).
  - Delivers 3 distinct sections: Humorous Roast, Technical Findings, and Suggested Fix.
- **Component 3: Transparent Evaluation Dashboard:**
  - Streamlit web interface with Plotly confusion matrices, ROC curves, and feature importance.
- **Speaker Note:**  
  *"Code Roster couples predictive data science with static program analysis. The predictive model forecasts performance, while the roast engine critiques code quality."*

---

### Slide 4: System Architecture
- **Dual-Engine Decoupled Architecture:**
  - **Predictive ML Engine:** Scikit-learn Pipeline with `ColumnTransformer` (fit strictly on training data).
  - **Static AST Engine:** Python Standard Library `ast` module (AST parser + `NodeVisitor`).
- **Safety First:** 100% static analysis; zero `eval()` or `exec()` execution on user code.
- **Model Persistence:** Joblib model artifact and JSON metadata loaded dynamically without retraining.
- **Speaker Note:**  
  *"The system uses a decoupled dual-engine design. Importantly, the ML predictor and the static code analyzer are separate components: one is probabilistic, the other is deterministic."*

---

### Slide 5: Dataset & Preprocessing
- **Dataset Description:** 1,500 student records across 7 features and 1 target variable (`performance_tier`).
- **Transparency Disclosure:** Fully simulated and reproducible synthetic dataset (`random_seed=42`).
- **Why Synthetic Data?**
  - Public competition datasets (Kaggle) require private user credentials.
  - Public school benchmarks (UCI) record Portuguese high school alcohol consumption, not coding telemetry.
  - CodeSearchNet contains docstring search pairs, not student grades or bug labels.
- **Preprocessing Pipeline:**
  - Numerical features: Standardized ($\mu=0, \sigma=1$) using `StandardScaler`.
  - Categorical features: Encoded using `OneHotEncoder(handle_unknown='ignore')`.
  - Fit strictly on `X_train` to eliminate data leakage.
- **Speaker Note:**  
  *"We maintain absolute academic integrity: our dataset is synthetic and explicitly labeled as simulated. Preprocessing was placed inside a Scikit-learn Pipeline so scaling parameters were calculated strictly on training data, preventing any data leakage."*

---

### Slide 6: Machine Learning Algorithms & Training
- **Candidate Models Compared:**
  1. *Baseline:* Decision Tree Classifier (max_depth=4)
  2. *Linear Baseline:* Logistic Regression (multinomial, l2 regularized)
  3. *Ensemble:* Random Forest Classifier (100 estimators, max_depth=8)
- **Experimental Protocol:**
  - Stratified 80/20 train/test split.
  - 5-Fold Stratified Cross-Validation on training data.
- **Champion Selection Metric:** **Macro F1-Score** (treats all 3 performance tiers with equal importance, preventing majority class bias).
- **Speaker Note:**  
  *"We trained three models and evaluated them using 5-fold cross-validation. We chose Macro F1-score as our selection metric because it penalizes models that ignore minority performance tiers."*

---

### Slide 7: Evaluation Results
- **Comparison Table:**
  - Logistic Regression achieved **0.7356 Test Macro F1** and **75.7% Test Accuracy**.
  - Random Forest achieved **0.7139 Test Macro F1** and **72.7% Test Accuracy**.
  - Decision Tree achieved **0.6987 Test Macro F1** and **72.0% Test Accuracy**.
- **Model Choice Rationale:**
  - Logistic Regression won on Macro F1 due to smooth linear hyperplane decision boundaries.
- **Key Feature Importances:**
  - Problems solved (31.4%), daily coding hours (24.8%), and submission accuracy (18.6%) are the dominant drivers. Primary programming language contributed less than 1%.
- **Speaker Note:**  
  *"As shown on the chart, Logistic Regression demonstrated the highest Macro F1 score on the held-out test set. The feature importance chart proves that daily coding hours and problem volume dictate performance far more than the specific programming language chosen."*

---

### Slide 8: Live Demo — Code Roast Personas
- **Input Example:** Nested loops with in-loop string concatenation.
- **Demonstration of the 4 Personas:**
  - *Best Friend:* `"Bhai, CPU ko overtime ka form bharwa diya kya? 😂"`
  - *Strict Manager:* `"Potential O(n²) bottleneck detected. Please justify the runtime cost before merging."`
  - *Professor:* `"Nested loops dikh rahe hain. Explain how both loop bounds scale with input size."`
  - *Savage:* `"Tere code ko input do aur CPU overtime ka form bharne lagta hai. 💀"`
- **Three Section Output:** (1) The Roast, (2) Technical Findings Table with Big-O notes, (3) Suggested Fix Code.
- **Speaker Note:**  
  *"Now let's see the Code Roast in action. The same detected quadratic nested loop is roasted completely differently depending on whether you choose Best Friend, Strict Manager, Professor, or Savage, followed by concrete fixes."*

---

### Slide 9: Limitations & Future Scope
- **Current Limitations:**
  - Static AST analysis estimates Big-O conservatively but cannot evaluate dynamic bounds without runtime profiling.
  - Simulated dataset reflects a mathematical process, not real-world students.
- **Future Scope:**
  - Real-time GitHub and LeetCode API webhooks.
  - Dynamic profiling using Python `cProfile` and `tracemalloc`.
  - Local quantized Small Language Model (SLM) for interactive code repair.
- **Speaker Note:**  
  *"In future iterations, we plan to connect real platform APIs like LeetCode and GitHub Classroom, and combine static analysis with dynamic memory profiling."*

---

### Slide 10: Conclusion & Key Learnings
- **Summary:**
  - Successfully built a complete, runnable college project with 0 GPU requirement.
  - Implemented an end-to-end ML pipeline with 5-fold CV, pipeline preprocessing, and Joblib persistence.
  - Created a safe, entertaining AST-based Code Roast engine with 4 selectable personas.
  - 100% test coverage with 27 automated unit and integration tests.
- **Speaker Note:**  
  *"In conclusion, Code Roster shows how machine learning and static analysis can collaborate to create an engaging learning tool for computer science students. Thank you, and I am now ready for questions."*

---

# PART II: COMPREHENSIVE VIVA VOCE QUESTIONS & ANSWERS

---

### 1. What is Supervised Learning, and how does Code Roster use it?
**Answer:**  
Supervised learning is an ML approach where an algorithm learns a mapping function from input features ($X$) to known ground-truth labels ($y$).  
In Code Roster, the input features are student practice metrics (daily coding hours, problems solved, submission accuracy, streak days, lab assignments, and focus score), and the target variable is the student's categorical performance tier (`Needs Guidance`, `Competent`, or `Exemplary`).

---

### 2. Why did you compare Logistic Regression, Decision Trees, and Random Forest?
**Answer:**  
Comparing multiple algorithms demonstrates sound empirical methodology:
- **Decision Tree:** Serves as an interpretable rule-based baseline that makes orthogonal splits.
- **Logistic Regression:** Serves as a linear probabilistic baseline that computes log-odds and models continuous hyperplane boundaries.
- **Random Forest:** Serves as an ensemble method that trains multiple bagging trees to reduce variance and capture non-linear feature interactions.

---

### 3. What is the difference between Accuracy and Macro F1-score? Why choose Macro F1?
**Answer:**  
- **Accuracy** is the ratio of correct predictions to total predictions: $\frac{TP + TN}{\text{Total}}$. However, if a dataset has class imbalance (e.g., 80% class A and 20% class B), a model predicting only class A achieves 80% accuracy while failing completely on class B.
- **Macro F1-score** computes the harmonic mean of Precision and Recall for *each class independently*, and then averages them without weights:
  $$\text{Macro F1} = \frac{1}{N} \sum_{i=1}^{N} F1_i$$
In Code Roster, Macro F1 gives equal importance to the minority `Exemplary` class, preventing the model from ignoring top performers.

---

### 4. What is a Confusion Matrix, and how do you interpret it?
**Answer:**  
A confusion matrix is an $N \times N$ table that cross-tabulates actual ground truth labels against model predicted labels:
- Rows represent True Classes; Columns represent Predicted Classes.
- Diagonal cells represent correct classifications (True Positives).
- Off-diagonal cells represent misclassifications (False Positives and False Negatives).  
In Code Roster, the Plotly heatmap allows examiners to immediately see which tiers get confused (e.g., whether `Needs Guidance` students are mistakenly predicted as `Competent`).

---

### 5. What is Data Leakage, and how did you prevent it in your code?
**Answer:**  
Data leakage occurs when information from outside the training dataset (such as test set statistics) influences model training, producing unrealistically high test metrics that fail in production.  
**Prevention in Code Roster:** We encapsulated all preprocessing inside a Scikit-learn `Pipeline` using `ColumnTransformer`. `StandardScaler` and `OneHotEncoder` are fit **strictly on `X_train`**. When evaluating `X_test`, the preprocessor only applies the transformation using the mean and variance learned from `X_train`.

---

### 6. What is Overfitting, and how did you check for it?
**Answer:**  
Overfitting occurs when a model memorizes noise and specific patterns in the training data rather than learning generalizable concepts, resulting in high training accuracy but poor test accuracy.  
**How we guarded against it:**
1. We evaluated models using **5-Fold Stratified Cross-Validation** on the training data.
2. We restricted model complexity (e.g., `max_depth=4` on Decision Tree, `max_depth=8` on Random Forest).
3. The close alignment between cross-validation Macro F1 (0.7167) and held-out test Macro F1 (0.7356) proves the model generalizes well without overfitting.

---

### 7. Why is your dataset synthetic, and what are its limitations?
**Answer:**  
- Public competition datasets (like Kaggle) require authenticated private user API keys that cannot be distributed in open submissions.
- Public academic datasets (like UCI) track Portuguese high school alcohol consumption, not competitive programming telemetry.
- CodeSearchNet is a docstring-code pair retrieval corpus without student scores or bug labels.  
**Limitation:** The measured model performance reflects our mathematical data-generating process and does not claim to validate real-world student abilities. We explicitly label the data as simulated to maintain scientific honesty.

---

### 8. Why is Static Code Analysis NOT Machine Learning?
**Answer:**  
- **Static Code Analysis (AST):** Uses deterministic grammar rules defined by Python's grammar specification. It parses code text into an Abstract Syntax Tree and traverses nodes using an `ast.NodeVisitor`. There are no weights, no loss functions, and no probabilistic training involved.
- **Machine Learning:** Learns statistical parameters from numerical data distributions using loss optimization (gradient descent or maximum likelihood).

---

### 9. Why does your analyzer say "Potential O(n²)" instead of definitive O(n²)?
**Answer:**  
Because static analysis inspects syntax, not runtime input bounds.  
If code has nested loops like:
```python
for item in arr:
    for i in range(3):  # Constant bound!
        pass
```
The inner loop runs a fixed 3 times, meaning overall complexity is $O(3n) = O(n)$, not $O(n^2)$. Stating "Potential O(n²)" acknowledges that the quadratic scaling assumes both loop bounds grow proportionally with input size $n$.

---

### 10. How does the Code Roast engine generate different persona responses?
**Answer:**  
The engine uses an adapter architecture:
1. `code_analyzer.py` extracts an `AnalysisResult` containing exact syntax errors or rule violation IDs (`PERF_001`, `BUG_001`, etc.).
2. `roast_engine.py` passes these IDs into the chosen persona template map (*Best Friend*, *Strict Manager*, *Professor*, *Savage*).
3. The engine dynamically composes an issue-specific roast, while preserving the tone and vocabulary characteristic of that persona.

---

### 11. Why did you persist the model using Joblib instead of retraining on every request?
**Answer:**  
In production software, training is an offline batch process, whereas inference is an online real-time service. Retraining on every page reload would cause high latency, memory waste, and non-deterministic behavior. By saving the fitted pipeline as `models/best_student_performance_model.joblib` and caching it in Streamlit with `@st.cache_resource`, inference executes in milliseconds.

---

### 12. Why did you not use `eval()` or `exec()` for code analysis?
**Answer:**  
Executing untrusted user-submitted code using `eval()` or `exec()` creates severe Remote Code Execution (RCE) vulnerabilities (e.g., malicious scripts deleting files or exhausting memory). By using Python's standard `ast` module, we inspect the code structure purely as text data, ensuring 100% security without running a single line of arbitrary code.
