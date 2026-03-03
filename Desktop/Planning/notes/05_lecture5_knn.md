# Lecture 5: K-Nearest Neighbors (KNN) (IS 670)

**Big picture:** KNN classifies by majority vote among the K nearest training points. It is non-parametric and instance-based. **Critical:** Features must be scaled (normalized) so that distance is meaningful. Small K (e.g., K=1) causes overfitting; large K causes underfitting. Lab 5 compares KNN with decision trees and explores the impact of K.

---

## 1. Big Picture (Business Analytics Framing)

- **Why KNN?** Simple, no training phase (lazy learner); adapts to local structure. Good when decision boundaries are irregular.
- **Why scaling?** KNN uses distance (e.g., Euclidean). If one feature has much larger scale (e.g., VehOdo vs VehicleAge), it dominates; scaling puts features on equal footing.
- **K choice:** K=1 → memorizes training data (100% train accuracy, poor test); larger K → smoother boundaries, better generalization but possible underfitting if K too large.

---

## 2. Concepts from Scratch

### 2.1 How KNN works

1. For a new point, find the K nearest training points (by distance, usually Euclidean).
2. Take the majority class among those K neighbors.
3. Ties: typically broken arbitrarily or by distance-weighted vote.

### 2.2 Distance (Euclidean)

- d(x, y) = √(Σ (x_i − y_i)²)
- Features with larger ranges dominate; scaling fixes this.

### 2.3 Scaling / normalization

- **MinMaxScaler:** Maps each feature to [0, 1]: (x − min) / (max − min). Fit on train, transform train and test.
- **StandardScaler:** Centers to mean 0, std 1.
- **Rule:** Fit scaler on training data only; transform both train and test (avoid leakage).

---

## 3. Definitions (Exact + Beginner-Friendly)

| Term | Definition |
|------|------------|
| **KNN** | K-Nearest Neighbors: classify by majority vote of K closest training points. |
| **K (n_neighbors)** | Number of neighbors used for the vote. |
| **Euclidean distance** | √(Σ(x_i − y_i)²); standard distance for numeric features. |
| **Scaling / Normalization** | Rescale features (e.g., 0–1) so distance is fair across features. |
| **MinMaxScaler** | Scales each feature to [0, 1] based on min/max from training data. |
| **Lazy learner** | KNN doesn't build a model at fit time; defers work to predict time. |
| **Overfitting (K=1)** | Each point's nearest neighbor is itself → 100% train accuracy; poor test. |
| **Underfitting (large K)** | Too many neighbors → overly smooth; approaches majority class everywhere. |

---

## 4. Key Formulas

- **Euclidean distance:** d(x,y) = √(Σ(x_i − y_i)²)
- **MinMax scaling:** x_scaled = (x − min) / (max − min) per feature
- *Prediction: majority class among K nearest neighbors*

---

## 5. Worked Example (Mirror Lab 5 Style)

**Goal:** Load Car data, normalize predictors, split train/test, build KNN (K=1 and K=4), compare with DT, evaluate generalization.

1. **Preprocess:** get_dummies, define target and predictors.
2. **Scale (critical):**
   ```python
   from sklearn.preprocessing import MinMaxScaler
   min_max_scaler = MinMaxScaler()
   predictors_normalized = pd.DataFrame(min_max_scaler.fit_transform(predictors))
   predictors_normalized.columns = predictors.columns
   ```
3. **Split** on normalized predictors (not raw).
4. **KNN K=1:**
   ```python
   model1 = KNeighborsClassifier(n_neighbors=1)
   model1.fit(predictors_train, target_train)
   # 100% train accuracy, ~55% test — overfitting
   ```
5. **KNN K=4:**
   ```python
   model2 = KNeighborsClassifier(n_neighbors=4)
   model2.fit(predictors_train, target_train)
   # ~72% train, ~67% test — better generalization
   ```
6. **Compare:** K=4 generalizes better; K=1 memorizes and overfits.

---

## 6. Common Mistakes / Misconceptions

- **Forgetting to scale:** KNN is very sensitive; always scale before fitting.
- **Fitting scaler on test data:** Fit on train only; transform train and test. Fitting on test = data leakage.
- **K=1 for production:** Avoid; 100% train accuracy but poor test. Use larger K (e.g., 5–20) or tune.
- **Very large K:** Approaches predicting majority class; underfitting.
- **Splitting before scaling:** Wrong. Scale the full predictor set (or fit scaler on train), then split—or split first, fit scaler on train, transform both. Lab 5: scale predictors, then split.

---

## 7. Mini-Check Quiz (5–10 Qs) + Answers

1. Why must we scale features for KNN?  
   **Answer:** Distance is dominated by features with larger ranges; scaling makes all features contribute fairly.

2. What happens with K=1?  
   **Answer:** Each point's nearest neighbor is itself → 100% train accuracy, overfitting; poor test performance.

3. What happens with very large K?  
   **Answer:** Underfitting; prediction approaches majority class; smooth but possibly poor performance.

4. Should we fit MinMaxScaler on train or test?  
   **Answer:** Fit on train only; transform both train and test. Never fit on test (leakage).

5. What distance does KNN typically use?  
   **Answer:** Euclidean (default in sklearn); can use Manhattan or others via `metric` parameter.

6. Is KNN a lazy or eager learner?  
   **Answer:** Lazy—no model built at fit; all work at predict time (finding neighbors).

7. How do you build a KNN with K=5?  
   **Answer:** `KNeighborsClassifier(n_neighbors=5)`

---

## 8. TL;DR Cheat Sheet

- **Scale first:** `MinMaxScaler().fit_transform(X)` — fit on train, transform train and test.
- **KNN:** `KNeighborsClassifier(n_neighbors=5)` (or as tuned).
- **K=1:** Overfitting; 100% train, poor test.
- **Large K:** Underfitting; smooth boundaries.
- **Rule:** Always scale before KNN; fit scaler on train only.

---

**Sources used:** Lab 5 (IS670_lab05 (1).html) — KNN, MinMaxScaler, n_neighbors=1 vs 4, overfitting (K=1), DT vs KNN; course map. Lecture slides not in provided material; add slide refs when available.
