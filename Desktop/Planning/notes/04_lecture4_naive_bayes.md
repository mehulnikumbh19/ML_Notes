# Lecture 4: Naive Bayes (IS 670)

**Big picture:** Naive Bayes is a probabilistic classifier that uses Bayes' theorem with a strong assumption: features are conditionally independent given the class. It is fast, works with limited data, and often gives good results for text and tabular classification. Lab 4 compares it with Decision Trees.

---

## 1. Big Picture (Business Analytics Framing)

- **Why Naive Bayes?** Simple, fast, interpretable (via class probabilities). Often used for spam detection, sentiment, and similar tasks.
- **Trade-off vs Decision Tree:** NB can have high recall but low precision (many false alarms); DT can have better precision but may miss more positives. Choice depends on business cost of false positives vs false negatives.
- **"Naive" assumption:** Features are independent given the class—rarely true in practice, but the model often still works well.

---

## 2. Concepts from Scratch

### 2.1 Bayes' theorem

- P(Class | features) ∝ P(features | Class) × P(Class)
- We predict the class that maximizes this posterior probability.

### 2.2 Naive assumption

- P(features | Class) ≈ P(f1|Class) × P(f2|Class) × … × P(fn|Class)
- Assumes each feature is independent given the class. This simplification makes the math tractable and the model fast.

### 2.3 sklearn variants

| Variant | Use case |
|---------|----------|
| **GaussianNB** | Numeric features, assumed normally distributed per class |
| **MultinomialNB** | Discrete/count features (e.g., word counts) — used in Lab 4 |
| **BernoulliNB** | Binary features (0/1) |

Lab 4 uses **MultinomialNB** with default settings on the Car dataset (one-hot encoded and numeric predictors).

---

## 3. Definitions (Exact + Beginner-Friendly)

| Term | Definition |
|------|------------|
| **Naive Bayes** | Probabilistic classifier; uses Bayes' theorem; assumes features are conditionally independent given the class. |
| **Prior** | P(Class) — proportion of each class in the data. |
| **Likelihood** | P(features | Class) — modeled per feature under the naive assumption. |
| **Posterior** | P(Class | features) — what we want; we pick the class with highest posterior. |
| **MultinomialNB** | sklearn Naive Bayes for discrete/count features. |

---

## 4. Key Formulas

- **Bayes:** P(Class|X) ∝ P(X|Class) × P(Class)
- **Naive:** P(X|Class) ≈ ∏ P(x_i | Class)
- *Exact formulas for MultinomialNB / GaussianNB: see sklearn docs or lecture slides.*

---

## 5. Worked Example (Mirror Lab 4 Style)

**Goal:** Build both a Decision Tree and Naive Bayes model; compare precision, recall, and F1 on test data.

1. **Preprocess (same as Lab 3):** get_dummies, define target and predictors, train_test_split.
2. **Decision Tree (max_depth=3):**
   ```python
   model_DT = DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=3)
   model_DT.fit(predictors_train, target_train)
   prediction_on_test_DT = model_DT.predict(predictors_test)
   print(classification_report(target_test, prediction_on_test_DT))
   ```
3. **Naive Bayes:**
   ```python
   model_NB = MultinomialNB()
   model_NB.fit(predictors_train, target_train)
   prediction_on_test_NB = model_NB.predict(predictors_test)
   print(classification_report(target_test, prediction_on_test_NB))
   ```
4. **Compare:** DT typically has higher precision; NB can have higher recall but more false positives (low precision). Choose based on whether avoiding false alarms (precision) or catching more bad buys (recall) matters more.

---

## 6. Common Mistakes / Misconceptions

- **Using MultinomialNB on negative or continuous values:** MultinomialNB expects non-negative counts. For numeric data with negatives or floats, use GaussianNB or scale/discretize first.
- **Expecting NB to always beat DT:** No; each model has different strengths. Compare on your data.
- **Ignoring precision when recall is high:** NB with high recall but low precision means many false alarms—costly if acting on predictions.
- **Forgetting to encode categoricals:** Same as for DT; use get_dummies before fitting.

---

## 7. Mini-Check Quiz (5–10 Qs) + Answers

1. What does "naive" mean in Naive Bayes?  
   **Answer:** Assumption that features are conditionally independent given the class.

2. Which sklearn Naive Bayes is used in Lab 4?  
   **Answer:** MultinomialNB.

3. When does NB tend to have low precision?  
   **Answer:** When it predicts positive too often (many false positives).

4. What is the prior in Naive Bayes?  
   **Answer:** P(Class) — the proportion of each class in the training data.

5. For continuous numeric features, which NB variant is appropriate?  
   **Answer:** GaussianNB (assumes features are normally distributed per class).

6. How do you compare DT vs NB in practice?  
   **Answer:** Train both, evaluate on test with confusion matrix and classification_report; compare precision, recall, F1, and AUC; pick based on business goal.

---

## 8. TL;DR Cheat Sheet

- **Naive Bayes:** Probabilistic; assumes feature independence; fast.
- **sklearn:** `MultinomialNB()` for discrete/counts; `GaussianNB()` for continuous.
- **Fit/predict:** Same API as DT: `model.fit(X_train, y_train)`, `model.predict(X_test)`.
- **Typical trade-off:** NB can have higher recall, lower precision; DT can have higher precision, lower recall — compare on your data.

---

**Sources used:** Lab 4 (IS670_lab04 (2).html) — Decision Tree vs Naive Bayes; MultinomialNB, DT (max_depth=3), classification_report comparison; course map. Lecture slides not in provided material; add slide refs when available.
