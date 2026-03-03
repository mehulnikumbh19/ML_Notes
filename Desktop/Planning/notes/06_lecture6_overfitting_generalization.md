# Lecture 6: Overfitting & Generalization (IS 670)

**Big picture:** A model that performs well on training data may perform poorly on new data—that is **overfitting**. **Generalization** means performing well on unseen (test) data. We control overfitting through regularization (e.g., max_depth for trees, K for KNN) and by evaluating on held-out test data. Model choice (DT vs NB vs KNN) depends on the problem and trade-offs between interpretability, precision, recall, and generalization.

---

## 1. Big Picture (Business Analytics Framing)

- **Why care?** The goal is to predict well on new cars, new customers, new transactions—not just the data we trained on.
- **Business risk:** Overfit model looks great in development but fails in production → bad decisions, lost trust.
- **Lecture 6 scope:** Recognize overfitting vs underfitting; use train vs test performance; choose regularization (max_depth, K); compare models (DT, NB, KNN) and pick based on test metrics.

---

## 2. Concepts from Scratch

### 2.1 Overfitting

- **Definition:** Model fits training data too closely—captures noise, idiosyncrasies—and performs poorly on new data.
- **Signs:** High train accuracy, low test accuracy; large gap between train and test metrics.
- **Examples:** K=1 in KNN (100% train, ~55% test); very deep decision tree; model with too many parameters for the data size.

### 2.2 Underfitting

- **Definition:** Model is too simple—cannot capture real patterns—and performs poorly on both train and test.
- **Signs:** Low train and low test accuracy.
- **Examples:** K very large in KNN (predicts majority class); max_depth=1 in DT; overly restricted model.

### 2.3 Generalization

- **Definition:** Good performance on unseen (test) data.
- **How to measure:** Hold out test set; never use it during model building; report test accuracy, precision, recall, F1, AUC.
- **Sweet spot:** Balance between overfitting and underfitting—e.g., moderate max_depth, moderate K.

### 2.4 Regularization / model complexity

| Model | Parameter | Effect |
|-------|-----------|--------|
| Decision Tree | max_depth | Smaller = simpler, less overfitting; larger = more complex, more overfitting |
| KNN | n_neighbors (K) | Larger K = smoother, less overfitting; K=1 = maximum overfitting |
| Naive Bayes | (few tunable) | Generally less prone to overfitting; simple model |

---

## 3. Definitions (Exact + Beginner-Friendly)

| Term | Definition |
|------|------------|
| **Overfitting** | Model fits training data very well but performs poorly on new (test) data. |
| **Underfitting** | Model is too simple; poor performance on both train and test. |
| **Generalization** | Good performance on unseen data (test set). |
| **Regularization** | Techniques to limit model complexity (e.g., max_depth, K) to reduce overfitting. |
| **Bias–variance trade-off** | Simple models = high bias, low variance; complex models = low bias, high variance. Overfitting = high variance. |
| **Train vs test** | Fit on train; evaluate on test to estimate generalization. |

---

## 4. Key Formulas

- No single formula; concepts are diagnostic:
- **Overfitting:** train_acc >> test_acc (large gap).
- **Underfitting:** train_acc and test_acc both low.
- **Good generalization:** test_acc high, gap between train and test moderate.

---

## 5. Worked Example (Synthesis of Labs 3–5)

**Scenario:** Car dataset; predict IsBadBuy.

| Model | Train Acc | Test Acc | Interpretation |
|-------|-----------|----------|----------------|
| DT max_depth=2 | ~63% | ~63% | May underfit; simple |
| DT max_depth=3 | higher | ~63% | Moderate complexity |
| DT no limit | 100% | ~55% | Overfitting |
| NB | ~60% | ~60% | Generally stable |
| KNN K=1 | 100% | ~55% | Severe overfitting |
| KNN K=4 | ~72% | ~67% | Better generalization |

**Takeaway:** Prefer models with reasonable train–test gap and good test performance. For bad-buy detection: K=4 or DT with max_depth 3–5 often better than K=1 or unconstrained DT.

---

## 6. Common Mistakes / Misconceptions

- **Evaluating only on train:** Always evaluate on test for generalization.
- **Tuning on test:** Never tune hyperparameters using test; use validation set or cross-validation.
- **Assuming more complex = better:** More complex models overfit; prefer simpler if test performance is similar.
- **Ignoring precision/recall:** Accuracy alone can hide poor minority-class performance; use full metrics.
- **K=1 or deep tree "must be good" because train is perfect:** Train perfection often means overfitting.

---

## 7. Mini-Check Quiz (5–10 Qs) + Answers

1. What is overfitting?  
   **Answer:** Model fits training data very well but performs poorly on new (test) data.

2. How do you detect overfitting?  
   **Answer:** Large gap between train and test accuracy (e.g., 100% train, 55% test).

3. What is underfitting?  
   **Answer:** Model too simple; poor performance on both train and test.

4. How does max_depth affect a decision tree?  
   **Answer:** Smaller max_depth = simpler tree, less overfitting; larger = more complex, more overfitting.

5. Why does K=1 in KNN overfit?  
   **Answer:** Each point's nearest neighbor is itself → memorizes labels → 100% train, poor test.

6. What does generalization mean?  
   **Answer:** Good performance on unseen (test) data.

7. Should you choose a model with the highest train accuracy?  
   **Answer:** No; train accuracy can be misleading. Prefer model with best test performance (or validation).

8. When comparing DT, NB, and KNN, what should you use?  
   **Answer:** Test metrics (accuracy, precision, recall, F1, AUC) and business context (cost of FP vs FN).

---

## 8. TL;DR Cheat Sheet

- **Overfitting:** High train, low test; reduce complexity (max_depth, increase K).
- **Underfitting:** Low train and test; increase complexity or try different model.
- **Generalization:** Evaluate on test set; never tune on test.
- **Regularization:** max_depth (DT), n_neighbors (KNN).
- **Model choice:** Compare test metrics; consider interpretability, precision, recall, speed.

---

**Sources used:** Course map; Labs 3–5 (max_depth, K=1 vs K=4, overfitting patterns); Assignment 1. Lecture slides not in provided material; add slide refs when available.
