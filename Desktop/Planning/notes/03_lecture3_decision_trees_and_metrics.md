# Lecture 3: Decision Trees & Classification Metrics (IS 670)

**Big picture:** Decision trees predict by repeatedly splitting data on features (e.g., VehicleAge ≤ 4.5). The choice of splits uses an impurity measure (entropy or gini). Classification metrics—confusion matrix, accuracy, precision, recall, F1, and AUC—tell you how well the model performs on test data, especially when classes are imbalanced.

---

## 1. Big Picture (Business Analytics Framing)

- **Why decision trees?** Interpretable: you can see which features (e.g., VehicleAge, VehBCost) drive predictions. Useful for business “don’t get kicked” decisions (Assignment 1).
- **Why metrics beyond accuracy?** When one class dominates (e.g., few bad buys), high accuracy can hide poor performance on the minority class. Precision, recall, and F1 give a fuller picture.
- **Train/test split:** Fit the model on training data; evaluate on held-out test data to estimate generalization.

---

## 2. Concepts from Scratch

### 2.1 Decision trees

- A **decision tree** splits the data on features (e.g., VehicleAge ≤ 4.5 → left branch, else right).
- Each split aims to make child nodes more **pure** (more of one class). Purity is measured by **entropy** or **gini**.
- **max_depth** limits how many levels the tree can grow; small depth reduces overfitting.
- **criterion:** `'entropy'` or `'gini'` (both measure impurity; entropy is common in the course).

### 2.2 Entropy (impurity)

- **Entropy** H = −Σ p_i log₂(p_i) over classes. Higher entropy = more mixed; lower = purer.
- At a split, pick the feature and threshold that **reduce entropy** (or equivalently maximize information gain) in the child nodes.
- A leaf with one class has entropy 0.

### 2.3 Classification metrics

| Metric | Formula | When it matters |
|--------|---------|------------------|
| **Accuracy** | (TP + TN) / total | Baseline; misleading if imbalanced |
| **Precision** | TP / (TP + FP) | How many predicted positives are correct |
| **Recall** | TP / (TP + FN) | How many actual positives we catch |
| **F1** | 2 × (P × R) / (P + R) | Balance of precision and recall |
| **AUC** | Area under ROC curve | Overall ranking ability; threshold-independent |

**Confusion matrix:** TN, FP, FN, TP — foundation for precision, recall, and accuracy.

---

## 3. Definitions (Exact + Beginner-Friendly)

| Term | Definition |
|------|------------|
| **Decision tree** | Model that splits on features; each node asks a yes/no question; leaves assign a class. |
| **Entropy** | Impurity measure for splits: H = −Σ p_i log₂(p_i); lower = purer. |
| **max_depth** | Maximum depth of the tree; limits overfitting. |
| **Train/test split** | Random partition: fit on train, evaluate on test (e.g., 70/30). |
| **Confusion matrix** | Table of actual vs predicted: TN, FP, FN, TP. |
| **Precision** | TP / (TP + FP) — of predicted positives, how many are correct. |
| **Recall** | TP / (TP + FN) — of actual positives, how many we found. |
| **F1** | Harmonic mean of precision and recall. |
| **AUC** | Area under the ROC curve; 0.5 = random, 1.0 = perfect. |

---

## 4. Key Formulas

- **Accuracy:** (TP + TN) / total  
- **Precision:** TP / (TP + FP)  
- **Recall:** TP / (TP + FN)  
- **F1:** 2 × (Precision × Recall) / (Precision + Recall)  
- **Entropy:** H = −Σ p_i log₂(p_i) over classes in a node  

---

## 5. Worked Example (Mirror Lab 3 Style)

**Goal:** Load CarAuction, one-hot encode categoricals, partition into train/test, build a decision tree, and evaluate with confusion matrix, classification_report, and AUC.

1. **Preprocess (one-hot encode categoricals):**
   ```python
   carAuction = pd.get_dummies(carAuction, columns=['Auction','Color','Size','TopThreeAmericanName','WheelType'], drop_first=True, dtype=int)
   ```

2. **Define target and predictors:**
   ```python
   target = carAuction['IsBadBuy']
   predictors = carAuction.drop(['IsBadBuy'], axis=1)
   ```

3. **Train/test split:**
   ```python
   predictors_train, predictors_test, target_train, target_test = train_test_split(predictors, target, test_size=0.3, random_state=0)
   ```

4. **Build decision tree:**
   ```python
   model = DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=2)
   model.fit(predictors_train, target_train)
   ```

5. **Evaluate:**
   ```python
   prediction_on_test = model.predict(predictors_test)
   cm = confusion_matrix(target_test, prediction_on_test)
   ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_).plot()
   print(classification_report(target_test, prediction_on_test))
   auc_score = roc_auc_score(target_test_bin, model.predict_proba(predictors_test)[:, 1])
   ```

---

## 6. Common Mistakes / Misconceptions

- **Evaluating only on training data:** Always evaluate on test data to estimate generalization.
- **Using accuracy when classes are imbalanced:** A model that always predicts the majority class can have high accuracy but zero recall for the minority class.
- **Forgetting to encode categorical predictors:** Decision trees need numeric inputs; use `pd.get_dummies()` or `OneHotEncoder`.
- **Very deep trees:** `max_depth` too large → overfitting; poor test performance.
- **Wrong argument order for confusion_matrix:** sklearn uses `confusion_matrix(y_true, y_pred)`.

---

## 7. Mini-Check Quiz (5–10 Qs) + Answers

1. What does entropy measure in a decision tree?  
   **Answer:** Impurity of a node; lower entropy = purer (more of one class).

2. Why use max_depth?  
   **Answer:** To limit tree depth and reduce overfitting; smaller trees generalize better.

3. What is precision? Recall?  
   **Answer:** Precision = TP / (TP + FP); Recall = TP / (TP + FN).

4. When is accuracy misleading?  
   **Answer:** When classes are imbalanced; a model predicting only the majority class can have high accuracy but poor recall for the minority class.

5. What does AUC measure?  
   **Answer:** Area under ROC curve; overall ranking ability; 0.5 = random, 1.0 = perfect.

6. What is the correct order of arguments for confusion_matrix?  
   **Answer:** `confusion_matrix(y_true, y_pred)` — actual first, predicted second.

7. How do you one-hot encode categorical columns for sklearn?  
   **Answer:** `pd.get_dummies(df, columns=[...], drop_first=True)` before defining X.

8. What does criterion='entropy' do in DecisionTreeClassifier?  
   **Answer:** Uses entropy (information gain) to choose the best split at each node.

---

## 8. TL;DR Cheat Sheet

- **Split:** `train_test_split(X, y, test_size=0.3, random_state=0)`
- **DT:** `DecisionTreeClassifier(criterion='entropy', max_depth=2, random_state=1)`
- **Fit/predict:** `model.fit(X_train, y_train)` → `model.predict(X_test)`
- **Confusion matrix:** `confusion_matrix(y_true, y_pred)`; `ConfusionMatrixDisplay(...).plot()`
- **Metrics:** `classification_report(y_true, y_pred)`; `roc_auc_score(y_true, y_prob)`
- **One-hot:** `pd.get_dummies(df, columns=[...], drop_first=True)`

---

**Sources used:** Lab 3 (IS670_lab03 (1) (1).html) — partition, DecisionTreeClassifier, entropy, max_depth, confusion_matrix, classification_report, ROC/AUC; course map. Lecture slides not in provided material; add slide refs when available.
