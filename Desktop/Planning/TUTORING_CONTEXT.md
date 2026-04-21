# IS 670 — Tutoring Context (Lectures 7–11)

> **How to use this file:** Paste the path `TUTORING_CONTEXT.md` (or its contents) into any new chat. This is the *single source of truth* for the tutoring session so context is never lost or mixed. Update the **Progress Tracker** section after each lecture is finished.

---

## 1. The Mission (what the user wants)

I (the user) want a **personal, step-by-step tutor** for IS 670 Lectures 7–11 and Labs 7–10, taught as if I know *nothing*. Every concept, formula, code block, visual, metric, algorithm, and example from the specified files must be covered. No assumed knowledge. No shortcuts.

The tutor must teach **one lecture at a time**, quiz me at the end, wait for my answers, correct them, then proceed.

---

## 2. Source Files (must read before teaching each lecture)

All files are in the workspace root `c:\Users\mniku\Desktop\Planning\`.

| # | File | Role |
|---|------|------|
| L7 | `IS670_Lecture7.pdf` (41 slides) | Numeric Prediction — Regression |
| L8 | `IS670_Lecture8.pdf` (29 slides) | Black Box Methods — SVM + Neural Networks |
| L9 | `IS670_Lecture9.pdf` (38 slides) | Unsupervised — Clustering (K-Means) |
| L10 | `IS670_Lecture10.pdf` (43 slides) | Unsupervised — Association Rule Mining (Apriori) |
| L11 | `IS670_Lecture11.pdf` (37 slides) | Improving Performance — Ensembles (Bagging, Boosting) |
| Lab 7 | `IS670_lab07_Solved (1) (1).html` | Linear Regression, Regression Tree, KNN Regression on insurance data |
| Lab 8 | `IS670_lab08 (1).html` | SVM/SVR + MLP Regressor/Classifier (insurance, car auction) |
| Lab 9 | `IS670_lab09 (1).html` | K-Means clustering on BART Rider data |
| Lab 10 | `IS670_lab10 (1).html` | Apriori association rules on grocery transactions |
| Lab 11 | **Not provided** — skip lab for Lecture 11 |

### How to read the labs (HTML is large)
Use a small Python `HTMLParser` script to strip everything except `jp-CodeCell`, `jp-MarkdownCell`, and `jp-OutputArea-output` text. Save to `.txt` then read. Delete temp files after. (Script was used previously — see the prior transcript if needed.)

---

## 3. Teaching Style Contract (MANDATORY — every lecture)

For **each lecture**, follow this exact structure in order:

1. **Big-picture overview** — what this lecture is about in plain English and why it matters in business.
2. **List of concepts** — bullet list of every concept to be covered.
3. **In-depth teaching of each concept** using this per-concept structure:
   - Jargon defined in plain English
   - Problem it solves / when to use
   - Input → Output
   - How it works (step-by-step, numbered)
   - Why it works (intuition)
   - When to use / When NOT to use
   - Strengths and weaknesses
   - Assumptions
   - Common mistakes
4. **Formulas** — every formula broken down **symbol by symbol**.
5. **Visuals** — for every chart/graph/table: what it is, what it means, why it matters.
6. **Lab application** — read the matching lab and explain it.
7. **Code line-by-line** — what each line does, why, what it outputs, how to interpret the output, and which lecture concept it demonstrates.
8. **Beginner examples** — small, concrete, walk-through numbers.
9. **Exam-style interpretation** — how this would be asked on an exam / lab question.
10. **Concluding section**:
    - Simple summary (plain English)
    - Technical summary
    - Key formulas recap
    - Key definitions recap
    - Common mistakes
    - Common exam traps
    - **5 practice questions WITH answers**
    - **5 practice questions WITHOUT answers** — then **stop and wait** for the user's answers before moving on.

### Overall flow (first turn only)
1. List all attached files.
2. Build a **master roadmap** of all topics across L7–L11.
3. List **prerequisites** (in plain English) the user needs to know before L7.
4. Then teach Lecture 7.

### Per-lecture flow
Teach → quiz → wait for user's answers → grade → connect to next lecture → teach next lecture.

---

## 4. Concept Inventory (so I never forget scope)

### Lecture 7 — Numeric Prediction
- Supervised vs unsupervised (framing), regression vs classification
- Simple Linear Regression, Multiple Linear Regression
- Ordinary Least Squares (OLS)
- Dummy coding / binary indicators (`pd.get_dummies(..., drop_first=True, dtype=int)`)
- Train/Test split
- Residuals, coefficients (β), intercept, p-values, R², Adjusted R²
- Assumptions: linearity, independence, homoscedasticity, no perfect multicollinearity, zero conditional mean, normality of errors
- Metrics: MAE, RMSE
- Non-linear terms (polynomial) and interaction effects
- Regression Trees (split criterion: SDR / squared error reduction)
- KNN Regression

### Lecture 8 — Black Box Methods
- Hyperplanes, maximum margin, support vectors
- Cost parameter C (soft margin)
- Kernel trick: linear, polynomial, RBF, sigmoid
- SVR (regression version)
- Artificial neurons, weights, bias
- Activation functions (sigmoid, tanh, ReLU, etc.)
- Forward pass, backward pass, epochs
- Network topology (layers, hidden units)
- Recurrent Neural Networks (idea only)
- Why deep learning wins on complex data
- Feature scaling (`MinMaxScaler`) is mandatory for SVM & NN
- Handling class imbalance via undersampling (`df.sample()`)

### Lecture 9 — Clustering
- Unsupervised learning concept
- Distance (Euclidean) + why scaling matters
- K-Means algorithm (initialize → assign → update → repeat)
- K-Means++ initialization
- Centroids, cluster sizes, cluster interpretation
- Choosing K: Elbow method (SSE / `inertia_`), Silhouette score

### Lecture 10 — Association Rule Mining
- Market basket analysis
- Item, itemset, transaction, LHS/RHS
- Association rule format: {A} → {B}
- Apriori algorithm (anti-monotonicity: supersets of infrequent sets are infrequent)
- Metrics: **Support**, **Confidence**, **Lift**, **Leverage**
- Interpreting rules for business action

### Lecture 11 — Ensembles
- Why ensembles beat single models (bias/variance, error diversification)
- Voting (hard vs soft)
- **Bagging**: bootstrap sampling, averaging/voting, OOB (out-of-bag) estimate
- Random Forest (as bagging of trees with feature randomness)
- **Boosting**: AdaBoost, weak learners, reweighting mistakes
- Bagging vs Boosting (parallel vs sequential; variance vs bias)

---

## 5. Key Code Patterns by Lab

### Lab 7 (regression on insurance)
```python
pd.read_csv(...)
df.astype('category')
pd.get_dummies(df, drop_first=True, dtype=int)
train_test_split(X, y, test_size=0.3, random_state=42)
from sklearn.linear_model import LinearRegression
LinearRegression().fit(X_train, y_train)
import statsmodels.api as sm
sm.OLS(y_train, sm.add_constant(X_train)).fit().summary()
from sklearn.metrics import mean_absolute_error, mean_squared_error
# RMSE = mean_squared_error(...)**0.5
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.neighbors import KNeighborsRegressor
```

### Lab 8 (SVM + NN)
```python
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR, SVC
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
# Undersample majority class:
majority.sample(n=len(minority), random_state=1)
pd.concat([minority, majority_sample])
```

### Lab 9 (K-Means)
```python
from sklearn.cluster import KMeans
from collections import Counter
km = KMeans(n_clusters=4, random_state=1, n_init=10).fit(X_scaled)
km.labels_; km.cluster_centers_; km.inertia_
# Elbow: loop K=1..10, plot inertia_
```

### Lab 10 (Apriori)
```python
import csv
from apyori import apriori
rules = apriori(transactions, min_support=0.01, min_confidence=0.2, min_lift=1)
# each rule has .support, .ordered_statistics[0].confidence, .lift
```

---

## 6. Key Formulas (memorize)

- **OLS coefficient (simple):** β̂₁ = Σ(xᵢ − x̄)(yᵢ − ȳ) / Σ(xᵢ − x̄)²; β̂₀ = ȳ − β̂₁x̄
- **MAE:** (1/n) Σ |yᵢ − ŷᵢ|
- **RMSE:** √[(1/n) Σ (yᵢ − ŷᵢ)²]
- **R²:** 1 − SSR/SST = 1 − Σ(yᵢ − ŷᵢ)² / Σ(yᵢ − ȳ)²
- **Euclidean:** d(x,y) = √Σ(xᵢ − yᵢ)²
- **SVM margin:** maximize 2/‖w‖ s.t. yᵢ(w·xᵢ + b) ≥ 1
- **RBF kernel:** K(x,y) = exp(−γ‖x − y‖²)
- **Sigmoid activation:** σ(z) = 1 / (1 + e^(−z))
- **Support(A):** #transactions containing A / N
- **Confidence(A→B):** Support(A ∪ B) / Support(A)
- **Lift(A→B):** Confidence(A→B) / Support(B)
- **Leverage(A→B):** Support(A ∪ B) − Support(A)·Support(B)
- **AdaBoost weight update (idea):** increase weight on misclassified points each round.

---

## 7. Final Deliverables (build at the very end, after Lecture 11)

1. **Master cheat sheet** — one-page quick reference across all 5 lectures.
2. **Comparison table of all methods** — problem type, how it works, strengths, weaknesses, when to use, key hyperparameter.
3. **Formulas sheet** — every formula with symbol legend.
4. **Memorize vs Understand guide** — what to rote-memorize vs what to just conceptually grasp.
5. **Final cumulative quiz** — mixed across all 5 lectures.
6. **Most important outputs/plots/tables to interpret** — e.g., OLS summary, confusion matrix, regression tree plot, elbow plot, silhouette plot, association rules table, feature importance.

---

## 8. Progress Tracker (update after each milestone)

| Step | Status | Notes |
|------|--------|-------|
| Read all files | Done | Lectures 7–11 PDFs + Labs 7–10 HTML |
| Master roadmap | Done | Delivered in first turn |
| Prerequisites list | Done | Delivered in first turn |
| **Lecture 7 — teach** | **Done** | Full structure followed |
| Lecture 7 — quiz given | Done | 5 Qs with answers + 5 Qs without answers |
| Lecture 7 — user answers | **Pending — waiting for user** | ← next step |
| Lecture 8 — teach | Pending | After grading L7 answers |
| Lecture 9 — teach | Pending | |
| Lecture 10 — teach | Pending | |
| Lecture 11 — teach | Pending | No lab file |
| Final deliverables | Pending | 6 items listed in §7 |

**Next immediate action:** Grade the user's answers to Lecture 7's 5 practice questions, then start Lecture 8.

---

## 9. Hard Rules (do not violate)

- NEVER assume prior knowledge.
- NEVER skip a formula, code line, or visual from the source files.
- ALWAYS cite the source file (e.g., "Lecture 7, slide on OLS" or "Lab 7, regression tree cell").
- ALWAYS wait for the user's quiz answers before moving to the next lecture.
- ALWAYS follow the per-lecture structure in §3 exactly.
- NEVER merge two lectures into one response — each lecture is its own deep dive.
- At the end, DO produce all 6 final deliverables in §7.

---

## 10. Related existing notes (Lectures 1–6, already complete)

Already in `notes/` folder — do **not** re-teach these, only reference if a prerequisite is needed:
- `01_lecture1_intro.md`, `02_lecture2_data_understanding.md`, `03_lecture3_decision_trees_and_metrics.md`, `04_lecture4_naive_bayes.md`, `05_lecture5_knn.md`, `06_lecture6_overfitting_generalization.md`
- `07_exam1_master_study_guide.md`, `08_python_patterns_and_templates.md`
- `COURSE_MEMORY.md` — compressed memory for L1–L6
- `SOURCES_INDEX.md` — source map for L1–L6

---

*Last updated: end of Lecture 7 teaching turn. Update the Progress Tracker after each lecture.*
