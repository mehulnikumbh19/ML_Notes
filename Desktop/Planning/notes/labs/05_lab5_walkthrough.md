# Lab 5 Walkthrough: K-Nearest Neighbor (KNN)

**Lab objective:** Build KNN models on the Car dataset: normalize predictors with MinMaxScaler, train/test split, fit KNN with n_neighbors=1 and n_neighbors=4, compare with Decision Tree, and understand overfitting (K=1) vs generalization (K=4). Emphasizes the importance of scaling for distance-based methods.

---

## 1. Step-by-Step Procedure (Recipe)

1. Load car data → preprocess (get_dummies, target, predictors).
2. **Normalize predictors:** MinMaxScaler, fit_transform on predictors, keep column names.
3. Train/test split on normalized predictors.
4. **KNN K=1:** fit, predict; report train and test accuracy — expect 100% train, ~55% test (overfitting).
5. **KNN K=4:** fit, predict; report train and test — expect ~72% train, ~67% test (better generalization).
6. **Compare:** K=1 vs K=4; when K is very large (underfitting).
7. **DT vs KNN:** Build deep DT to match K=1 train performance; compare test accuracy and interpretability.

---

## 2. Code Blocks Explained

### 2.1 Import (includes KNN and preprocessing)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
# or: from sklearn import preprocessing
# min_max_scaler = preprocessing.MinMaxScaler()
```

- **What:** KNeighborsClassifier, MinMaxScaler.
- **Why:** KNN requires scaling; MinMaxScaler maps features to [0,1].

---

### 2.2 Normalize predictors

```python
min_max_scaler = MinMaxScaler()
predictors_normalized = pd.DataFrame(min_max_scaler.fit_transform(predictors))
predictors_normalized.columns = predictors.columns
```

- **What:** Fit scaler on predictors, transform to [0,1] range; preserve column names.
- **Why:** KNN uses distance; unscaled features (e.g., VehOdo vs VehicleAge) would be unfair. **Important:** In production, fit on train only, then transform train and test—Lab may fit on full predictors before split; both approaches valid if no leakage (split before fit, or fit on train only).

---

### 2.3 Train/test split (on normalized data)

```python
predictors_train, predictors_test, target_train, target_test = train_test_split(
    predictors_normalized, target, test_size=0.3, random_state=0
)
```

- **What:** 70/30 split on scaled predictors.
- **Why:** Same workflow as Labs 3–4; evaluate on held-out test.

---

### 2.4 KNN with n_neighbors=1

```python
model1 = KNeighborsClassifier(n_neighbors=1)
model1.fit(predictors_train, target_train)
prediction_on_train = model1.predict(predictors_train)
prediction_on_test = model1.predict(predictors_test)
print(classification_report(target_train, prediction_on_train))  # 100% accuracy
print(classification_report(target_test, prediction_on_test))   # ~55%
```

- **What:** K=1 → each point's nearest neighbor is itself → perfect train, poor test.
- **Why:** Classic overfitting; model memorizes training data.

---

### 2.5 KNN with n_neighbors=4

```python
model2 = KNeighborsClassifier(n_neighbors=4)
model2.fit(predictors_train, target_train)
print(classification_report(target_train, model2.predict(predictors_train)))  # ~72%
print(classification_report(target_test, model2.predict(predictors_test)))    # ~67%
```

- **What:** K=4 → smoother boundaries; smaller gap between train and test.
- **Why:** Better generalization; K=4 preferred over K=1 for identifying bad buys.

---

### 2.6 Compare train vs test accuracy

```python
from sklearn.metrics import accuracy_score
train_acc1 = accuracy_score(target_train, model1.predict(predictors_train))
test_acc1 = accuracy_score(target_test, model1.predict(predictors_test))
print(f"K=1: Train {train_acc1:.2%}, Test {test_acc1:.2%}")
# Similar for K=4
```

- **What:** Explicit accuracy comparison.
- **Why:** Shows overfitting (K=1: high train, low test) vs generalization (K=4: closer train/test).

---

### 2.7 Very large K (underfitting)

```python
model_large_k = KNeighborsClassifier(n_neighbors=500)
# ...
```

- **What:** K near dataset size → almost always predicts majority class.
- **Why:** Underfitting; model too smooth.

---

### 2.8 DT to match K=1 train performance (Q2)

```python
model_dt = DecisionTreeClassifier(criterion='entropy', random_state=1)  # no max_depth
model_dt.fit(predictors_train, target_train)
# Depth ~33, 100% train; test ~55%
```

- **What:** Unconstrained DT can reach 100% train (like K=1) but poor test.
- **Why:** Both K=1 and very deep DT overfit; prefer simpler models (K=4, max_depth limited) for generalization.

---

## 3. Exam-Style Variants (Small Code Prompts)

1. Normalize a DataFrame `predictors` using MinMaxScaler and assign to `predictors_norm` with same column names.  
   *Answer:* `scaler = MinMaxScaler()`; `predictors_norm = pd.DataFrame(scaler.fit_transform(predictors))`; `predictors_norm.columns = predictors.columns`

2. Build a KNN with K=5 and fit on training data.  
   *Answer:* `model = KNeighborsClassifier(n_neighbors=5)`; `model.fit(X_train, y_train)`

3. Why does K=1 give 100% training accuracy?  
   *Answer:* Each point's nearest neighbor is itself (distance 0), so it always predicts its own label.

4. Why scale before KNN?  
   *Answer:* Distance is dominated by features with larger scales; scaling makes all features contribute fairly.

5. Fit MinMaxScaler on X_train and transform both X_train and X_test.  
   *Answer:* `scaler = MinMaxScaler()`; `X_train_scaled = scaler.fit_transform(X_train)`; `X_test_scaled = scaler.transform(X_test)` (do NOT fit on X_test)

6. What happens if K is very large (e.g., 500)?  
   *Answer:* Underfitting; predictions approach majority class; model too smooth.

---

## 4. Debugging Checklist (Common Errors)

- **KNN performs poorly:** Likely forgot to scale. Scale predictors before split (or fit scaler on train, transform both).
- **Fitting scaler on test:** Never fit on test; use `scaler.fit(X_train)` then `scaler.transform(X_train)` and `scaler.transform(X_test)`.
- **fit_transform vs transform:** fit_transform on train; transform only on test.
- **Column names lost:** After `fit_transform`, result is ndarray; reassign: `predictors_normalized.columns = predictors.columns`.
- **K=1 "perfect" on train:** Expected; check test accuracy to see overfitting.

---

## 5. Lab Cheat Sheet

| Task | Code |
|------|------|
| MinMaxScaler | `scaler = MinMaxScaler()` |
| Scale (fit on train) | `X_train_scaled = scaler.fit_transform(X_train)`; `X_test_scaled = scaler.transform(X_test)` |
| KNN K=1 | `KNeighborsClassifier(n_neighbors=1)` |
| KNN K=4 | `KNeighborsClassifier(n_neighbors=4)` |
| Fit/predict | Same as DT/NB |
| Compare accuracy | `accuracy_score(y_true, y_pred)` |

---

## 6. Key Takeaways

- **Scale before KNN:** MinMaxScaler (or StandardScaler); fit on train, transform train and test.
- **K=1:** Overfitting; 100% train, poor test. Do not use for production.
- **K=4 (or similar):** Better generalization; Lab 5 prefers K=4 for bad-buy identification.
- **Large K:** Underfitting.
- **DT vs KNN:** Both can overfit (deep DT, K=1); prefer constrained models (max_depth, larger K) for test performance.

---

**Sources used:** IS670_lab05 (1).html — "IS 670 Lab 5: K Nearest Neighbor"; MinMaxScaler, predictors_normalized, train_test_split; KNN n_neighbors=1 and 4; classification_report; overfitting (K=1), underfitting (large K); DT vs KNN (depth 33, 100% train); K=4 better for bad buys.
