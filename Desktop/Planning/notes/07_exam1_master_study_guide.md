# IS 670 — Exam 1 Master Study Guide

**Purpose:** Consolidated study guide for Exam 1, drawing from lectures 1–6, labs 1–5, and Assignment 1. Add exam review topics and question formats when provided.

---

## 1. Exam Scope (Inferred)

- **Data:** Understanding, exploration, visualization, preprocessing (missing, outliers, encoding)
- **Classification:** Target, predictors, train/test split
- **Metrics:** Confusion matrix; accuracy, precision, recall, F1; when to use which
- **Decision trees:** Splits, entropy/impurity, max_depth, overfitting
- **Naive Bayes:** Assumption, Bayes theorem, MultinomialNB vs GaussianNB
- **KNN:** Distance, scaling, K, overfitting (K=1), underfitting (large K)
- **Overfitting vs generalization:** Train vs test; regularization (max_depth, K)

---

## 2. Concepts by Topic

### 2.1 Data & Preprocessing

| Concept | Key Points |
|---------|------------|
| Missing values | `isnull().sum()`; categorical: `fillna('None')`; numeric: median/mean impute |
| Outliers | Boxplot; IQR method |
| One-hot encoding | `pd.get_dummies(df, columns=[...], drop_first=True)` |
| Train/test split | `train_test_split(X, y, test_size=0.3, random_state=...)` |

### 2.2 Classification Metrics

| Metric | Formula | When to use |
|--------|---------|-------------|
| Accuracy | (TP + TN) / total | Baseline; misleading if imbalanced |
| Precision | TP / (TP + FP) | When false positives costly |
| Recall | TP / (TP + FN) | When missing positives costly |
| F1 | 2 × (P × R) / (P + R) | Balance precision and recall |
| Confusion matrix | TN, FP, FN, TP | Foundation for all metrics |

### 2.3 Decision Trees

- **How it works:** Splits on features; criterion = entropy or gini
- **max_depth:** Limits depth; small = less overfitting
- **Entropy:** H = −Σ p_i log₂(p_i); lower = purer
- **Code:** `DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`

### 2.4 Naive Bayes

- **Assumption:** Features conditionally independent given class
- **Bayes:** P(Class|X) ∝ P(X|Class) × P(Class)
- **sklearn:** MultinomialNB (discrete/counts), GaussianNB (continuous)
- **Typical trade-off:** Higher recall, lower precision (many false positives)

### 2.5 KNN

- **How it works:** Majority vote of K nearest neighbors; Euclidean distance
- **Scaling:** Must scale (MinMaxScaler) before KNN
- **K=1:** Overfitting; 100% train, poor test
- **Large K:** Underfitting
- **Code:** `KNeighborsClassifier(n_neighbors=5)` after scaling

### 2.6 Overfitting & Generalization

| Pattern | Interpretation |
|---------|----------------|
| High train, low test | Overfitting (e.g., K=1, deep DT) |
| Low train, low test | Underfitting |
| Similar train and test, test good | Good generalization |

---

## 3. Formulas (Memorize)

- **Accuracy:** (TP + TN) / total
- **Precision:** TP / (TP + FP)
- **Recall:** TP / (TP + FN)
- **F1:** 2 × (Precision × Recall) / (Precision + Recall)
- **Entropy:** H = −Σ p_i log₂(p_i)
- **Euclidean:** d(x,y) = √(Σ(x_i − y_i)²)

---

## 4. When to Choose Which Model (Decision Guide)

| Situation | Preferred model | Reason |
|-----------|-----------------|--------|
| Need interpretability (business explanation) | **Decision Tree** | Can visualize splits and rules |
| Many categorical features, limited data | **Naive Bayes** | Fast, works with sparse data |
| Numeric features, need distance-based logic | **KNN** | Simple; must scale first |
| Imbalanced classes, care about minority class | All three; evaluate with **precision, recall, F1** — not accuracy alone |
| Overfitting suspected | DT: limit `max_depth`; KNN: increase K; NB: usually robust |
| Very high-dimensional data | NB or DT; KNN suffers from curse of dimensionality |
| Assignment 1 (Car, Good Buy vs Kick) | **DT** with max_depth variants (3, 5, 7, 10) to compare overfitting |

**Summary:** DT = interpretable; NB = fast, probabilistic; KNN = lazy learner, needs scaling; all need train/test split and proper metrics.

---

## 5. Top Exam Questions (Conceptual) + Sample Answers

| # | Question | Sample Answer |
|---|----------|---------------|
| 1 | Why is accuracy misleading for imbalanced data? | A model predicting only majority class has high accuracy but 0 recall for minority. E.g., 90% good buys → predict all good buys → 90% accuracy, 0% recall for kicks. |
| 2 | What is overfitting? How do you detect it? | Model fits training data too closely; poor on new data. Detect: high train accuracy, low test accuracy (e.g., K=1 in KNN, very deep DT). |
| 3 | Why must we scale for KNN? | KNN uses distance; features with larger scales dominate. Scaling (e.g., MinMaxScaler) makes features comparable. |
| 4 | What does "naive" mean in Naive Bayes? | Features are assumed conditionally independent given the class. Simplifies P(X|Class) to product of P(x_i|Class). |
| 5 | What does max_depth control in a decision tree? | Maximum depth of the tree; smaller = simpler model, less overfitting. |
| 6 | What happens with K=1 in KNN? | Each point's nearest neighbor is itself → 100% train accuracy; memorizes labels → poor test (overfitting). |
| 7 | What is the order of arguments for confusion_matrix? | `confusion_matrix(y_true, y_pred)` — actual first, predicted second. |
| 8 | When to use precision vs recall? | Precision: when false positives are costly (e.g., spam filters—don't want to miss real emails). Recall: when missing positives is costly (e.g., Don't Get Kicked—don't want to miss bad buys). |
| 9 | What is AUC? | Area under ROC curve; 0.5 = random, 1.0 = perfect; threshold-independent ranking measure. |
| 10 | Why drop_first in get_dummies? | Avoids multicollinearity (one category can be inferred from others); keeps fewer columns. |

---

## 6. Code Snippets to Know

- Split: `train_test_split(X, y, test_size=0.3, random_state=42)`
- DT (Labs 3–4): `DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`
- DT (Assignment 1): `DecisionTreeClassifier(max_depth=3, random_state=42)` — criterion optional (default gini)
- NB: `MultinomialNB()`; `GaussianNB()` for continuous features
- KNN: `KNeighborsClassifier(n_neighbors=5)` (after MinMaxScaler)
- Metrics: `classification_report(y_test, y_pred)`, `confusion_matrix(y_test, y_pred)`, `accuracy_score`, `roc_auc_score`
- One-hot: `pd.get_dummies(df, columns=[...], drop_first=True)`
- Scale (KNN): `scaler.fit_transform(X_train)`, `scaler.transform(X_test)` — fit on train only

---

## 7. Quick Review Checklist (Pre-Exam)

- [ ] Define target and predictors
- [ ] Train/test split (never evaluate only on train)
- [ ] For KNN: scale first, fit scaler on train
- [ ] For imbalanced data: use precision, recall, F1
- [ ] confusion_matrix(y_true, y_pred)
- [ ] max_depth limits overfitting in DT
- [ ] K=1 overfits in KNN; larger K generalizes better
- [ ] ROC/AUC: threshold-independent; 0.5 = random, 1.0 = perfect

---

## 8. Worked Scenario: Interpreting Results

**Given:** K=1 KNN → train 100%, test 55%; K=4 KNN → train 72%, test 67%.  
**Interpret:** K=1 overfits (memorizes train); K=4 generalizes better (closer train/test, reasonable test).

**Given:** max_depth=10 DT → train 99%, test 70%; max_depth=3 DT → train 75%, test 72%.  
**Interpret:** Deeper tree overfits; shallow tree generalizes better (slightly lower train, similar test).

---

*Add exam review materials, sample questions, and dates when provided.*
