# Lab 3 Walkthrough: Decision Tree

**Lab objective:** Build a decision tree on the CarAuction (Don't Get Kicked) dataset: preprocess (one-hot encode), partition into train/test, fit a DecisionTreeClassifier with entropy and max_depth, and evaluate with confusion matrix, classification_report, and AUC. Introduces the core classification workflow.

---

## 1. Step-by-Step Procedure (Recipe)

1. Load car data → preprocess (IsBadBuy 0/1 → Yes/No; one-hot encode categorical columns).
2. Define target (IsBadBuy) and predictors (all except target).
3. Partition: `train_test_split` (70/30, random_state=0); optionally balance training set.
4. Build DecisionTreeClassifier (criterion='entropy', max_depth=2).
5. Fit on train, predict on test.
6. Evaluate: confusion_matrix, ConfusionMatrixDisplay, classification_report, ROC curve, AUC.
7. Experiment: vary max_depth (2 vs 3); try criteria (gini, entropy, log_loss) and depths for best AUC.

---

## 2. Code Blocks Explained

### 2.1 One-hot encode categorical columns

```python
carAuction = pd.get_dummies(carAuction, columns=['Auction','Color','Size','TopThreeAmericanName','WheelType'], drop_first=True, dtype=int)
```

- **What:** Converts categorical columns to numeric 0/1 columns; drop_first avoids multicollinearity.
- **Why:** sklearn classifiers need numeric inputs; decision trees can't use raw text categories.

---

### 2.2 Define target and predictors

```python
target = carAuction['IsBadBuy']
predictors = carAuction.drop(['IsBadBuy'], axis=1)
```

- **What:** target = column to predict; predictors = all other columns.
- **Why:** Standard X/y setup for classification.

---

### 2.3 Train/test split

```python
predictors_train, predictors_test, target_train, target_test = train_test_split(predictors, target, test_size=0.3, random_state=0)
```

- **What:** 70% train, 30% test; random_state for reproducibility.
- **Why:** Fit on train; evaluate on test to measure generalization.

---

### 2.4 Build and fit DecisionTreeClassifier

```python
model = DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=2)
model.fit(predictors_train, target_train)
```

- **What:** Tree with entropy as split criterion; max_depth=2 limits overfitting.
- **Why:** entropy measures impurity; max_depth prevents very deep trees that memorize noise.

---

### 2.5 Predict on test

```python
prediction_on_test = model.predict(predictors_test)
```

- **What:** Class labels for each test row.
- **Why:** Needed for confusion matrix and classification_report.

---

### 2.6 Confusion matrix and display

```python
cm = confusion_matrix(target_test, prediction_on_test)
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_).plot()
```

- **What:** Confusion matrix (TN, FP, FN, TP); display shows a heatmap.
- **Why:** Foundation for precision, recall, accuracy; order is (y_true, y_pred).

---

### 2.7 Classification report (accuracy, precision, recall, F1)

```python
print(classification_report(target_test, prediction_on_test))
```

- **What:** Prints precision, recall, f1-score per class and overall accuracy.
- **Why:** Single call for all key metrics.

---

### 2.8 ROC curve and AUC

```python
target_test_bin = target_test.map({'Yes': 1, 'No': 0})
target_prob = model.predict_proba(predictors_test)[:, 1]
fpr, tpr, thresholds = roc_curve(target_test_bin, target_prob)
auc_score = roc_auc_score(target_test_bin, target_prob)
plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")
```

- **What:** ROC plots TPR vs FPR; AUC = area under curve; needs binary numeric y and probabilities.
- **Why:** AUC summarizes ranking ability; robust when classes are imbalanced.

---

### 2.9 Compare depth-2 vs depth-3

```python
model_d2 = DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=2)
model_d3 = DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=3)
model_d2.fit(predictors_train, target_train)
model_d3.fit(predictors_train, target_train)
# Compare classification_report and AUC on predictors_test
```

- **What:** Deeper tree often improves minority-class recall and AUC; can also overfit.
- **Why:** Lab explores the tradeoff between model complexity and generalization.

---

## 3. Exam-Style Variants (Small Code Prompts)

1. Split `predictors` and `target` into train (70%) and test (30%) with `random_state=0`.  
   *Answer:* `X_train, X_test, y_train, y_test = train_test_split(predictors, target, test_size=0.3, random_state=0)`

2. Build a DecisionTreeClassifier with entropy and max_depth=3.  
   *Answer:* `model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`

3. Fit the model and predict on test data.  
   *Answer:* `model.fit(X_train, y_train)` then `y_pred = model.predict(X_test)`

4. Compute the confusion matrix for test predictions.  
   *Answer:* `cm = confusion_matrix(y_test, y_pred)`

5. Print precision, recall, and F1 for test predictions.  
   *Answer:* `print(classification_report(y_test, y_pred))`

6. Compute AUC (assume y_test is numeric 0/1).  
   *Answer:* `roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])`

7. One-hot encode columns `A` and `B` in DataFrame `df`, dropping first.  
   *Answer:* `df = pd.get_dummies(df, columns=['A','B'], drop_first=True)`

---

## 4. Debugging Checklist (Common Errors)

- **`ValueError: could not convert string to float`:** Categorical columns not encoded; use `pd.get_dummies()`.
- **Wrong confusion_matrix layout:** Use `confusion_matrix(y_true, y_pred)` — actual first.
- **AUC needs numeric y:** If target is 'Yes'/'No', map to 0/1: `y_test.map({'Yes':1, 'No':0})`.
- **predict_proba for AUC:** Use `model.predict_proba(X_test)[:, 1]` (probability of positive class).
- **Train/test leakage:** Don't fit scaler or encoder on test; fit on train only, transform both.

---

## 5. Lab Cheat Sheet

| Task | Code |
|------|------|
| One-hot encode | `pd.get_dummies(df, columns=[...], drop_first=True)` |
| Train/test split | `train_test_split(X, y, test_size=0.3, random_state=0)` |
| Decision tree | `DecisionTreeClassifier(criterion='entropy', max_depth=2, random_state=1)` |
| Fit | `model.fit(X_train, y_train)` |
| Predict | `model.predict(X_test)` |
| Confusion matrix | `confusion_matrix(y_test, y_pred)` |
| Display confusion | `ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_).plot()` |
| Classification report | `classification_report(y_test, y_pred)` |
| AUC | `roc_auc_score(y_test_bin, model.predict_proba(X_test)[:, 1])` |

---

**Sources used:** IS670_lab03 (1) (1).html — "IS 670 Lab 3: Decision Tree"; get_dummies, target/predictors, train_test_split, balanced training, DecisionTreeClassifier(criterion='entropy', max_depth=2/3), confusion_matrix, ConfusionMatrixDisplay, classification_report, ROC/AUC, criterion and max_depth experiment.
