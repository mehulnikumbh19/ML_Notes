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

## 4. Common Exam Questions (Conceptual)

1. Why is accuracy misleading for imbalanced data?
2. What is overfitting? How do you detect it?
3. Why must we scale for KNN?
4. What does "naive" mean in Naive Bayes?
5. What does max_depth control in a decision tree?
6. What happens with K=1 in KNN?
7. What is the order of arguments for confusion_matrix?
8. When to use precision vs recall?

---

## 5. Code Snippets to Know

- Split: `train_test_split(X, y, test_size=0.3, random_state=42)`
- DT: `DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`
- NB: `MultinomialNB()`
- KNN: `KNeighborsClassifier(n_neighbors=5)` (after MinMaxScaler)
- Metrics: `classification_report(y_test, y_pred)`, `confusion_matrix(y_test, y_pred)`
- One-hot: `pd.get_dummies(df, columns=[...], drop_first=True)`

---

## 6. Quick Review Checklist

- [ ] Define target and predictors
- [ ] Train/test split (never evaluate only on train)
- [ ] For KNN: scale first, fit scaler on train
- [ ] For imbalanced data: use precision, recall, F1
- [ ] confusion_matrix(y_true, y_pred)
- [ ] max_depth limits overfitting in DT
- [ ] K=1 overfits in KNN; larger K generalizes better

---

*Add exam review materials, sample questions, and dates when provided.*
