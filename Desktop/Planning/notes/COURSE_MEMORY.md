# IS 670 — COURSE_MEMORY.md (Handoff Pack)

**Purpose:** Compressed running memory for New Chat handoff. Keep SHORT; update after each milestone.

---

## Definitions (course wording)

- **Target:** Variable we predict (e.g., Class, Legendary).
- **Predictors/Features:** Input variables used to predict target.
- **Train/test split:** Partition data; fit on train, evaluate on test (e.g. `test_size=0.3`, `random_state`).
- **Decision Tree:** Splits on features; `criterion='entropy'`, `max_depth` to limit depth.
- **Entropy:** Impurity measure for split criterion in trees.
- **Naive Bayes:** Probabilistic classifier; assumes feature independence.
- **KNN:** Classify by majority vote of K nearest neighbors; requires scaling.
- **Overfitting:** Good on train, poor on test (e.g., K=1, deep DT). **Underfitting:** Poor on both (e.g., very large K). **Generalization:** Good on test.

---

## Formulas (exam-relevant)

- **Accuracy:** (TP + TN) / total
- **Precision:** TP / (TP + FP)
- **Recall:** TP / (TP + FN)
- **F1:** 2 × (Precision × Recall) / (Precision + Recall)
- **Entropy:** H = −Σ p_i log₂(p_i) over classes (lower = purer)
- **Bayes:** P(Class|X) ∝ P(X|Class) × P(Class); Naive: P(X|Class) ≈ ∏ P(x_i|Class)
- **Euclidean (KNN):** d(x,y) = √(Σ(x_i − y_i)²); scale features first

---

## Metrics & When to Use

- **Imbalanced classes:** Don’t rely only on accuracy; use precision, recall, F1.
- **Confusion matrix:** TN, FP, FN, TP — foundation for precision/recall.

---

## Workflows (sklearn)

1. Load → inspect (shape, dtypes, missing).
2. Preprocess: missing values, outliers (as taught), dummy/one-hot for categoricals.
3. Define X (predictors), y (target).
4. Train/test split: `train_test_split(X, y, test_size=0.3, random_state=...)`.
5. **KNN:** Scale/normalize before split (fit on train, transform train+test).
6. Fit: `model.fit(X_train, y_train)` → `model.predict(X_test)`.
7. Evaluate: confusion matrix, `classification_report`, accuracy/precision/recall/F1.

---

## Code Templates (compact)

- **Missing:** `df.isnull().sum()`; **fill categorical:** `df.fillna('None')`
- **Viz:** histplot (numeric dist), boxplot (spread/outliers), countplot (categorical), scatter (2 numerics), pairplot (many numerics); boxplot by group: `sns.boxplot(x='num', y='cat', data=df)` or `df.boxplot(column='num', by='cat')`
- **Split:** `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)`
- **DT:** `DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`
- **NB:** `MultinomialNB()` for discrete/counts; `GaussianNB()` for continuous
- **KNN:** Scale first; `KNeighborsClassifier(n_neighbors=5)` (or as in lab).
- **Metrics:** `accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `classification_report`, `ConfusionMatrixDisplay`.

---

## Common Pitfalls

- **fillna('None')** on numeric column → converts to object; use only for categorical.
- Using accuracy only when data is imbalanced.
- Forgetting to scale for KNN.
- Evaluating on training data instead of test for generalization.
- Very deep trees (or K=1 in KNN) → overfitting.

---

## What’s Done / What’s Next

- **Done:** Phase A; Phase B (i=1–6): 01–06_lecture + labs 01–06 (Lab 6 = placeholder).
- **Next:** Phase C (Assignment walkthrough); Phase D (Exam 1 study guide, Python templates, code drills).

---
**Rule:** Always commit and push to the ML_Notes repo after completing each chunk/milestone.

*Update this file at the end of each milestone; paste into new chat when context is large.*
