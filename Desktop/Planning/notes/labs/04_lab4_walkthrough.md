# Lab 4 Walkthrough: Decision Tree vs Naive Bayes

**Lab objective:** Compare two classifiers—Decision Tree (entropy, max_depth=3) and Naive Bayes (MultinomialNB)—on the Car dataset. Preprocess, partition, fit both models, and evaluate with confusion matrix and classification_report. Understand the precision–recall trade-off between models.

---

## 1. Step-by-Step Procedure (Recipe)

1. Load car_kick data → preprocess (get_dummies, define target and predictors).
2. Train/test split (70/30).
3. **Decision Tree:** `DecisionTreeClassifier(criterion='entropy', max_depth=3)` → fit, predict, confusion matrix, classification_report.
4. **Naive Bayes:** `MultinomialNB()` → fit, predict, confusion matrix, classification_report.
5. Compare: precision, recall, F1 for both models; interpret which model is better for which goal.
6. (Optional) Plot tree for DT: `tree.plot_tree()`, `tree.export_text()`.

---

## 2. Code Blocks Explained

### 2.1 Import (includes MultinomialNB)

```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
```

- **What:** DecisionTreeClassifier, MultinomialNB, and metrics.
- **Why:** Lab 4 builds both models and compares them.

---

### 2.2 Build and fit Decision Tree (max_depth=3)

```python
model_DT = DecisionTreeClassifier(criterion='entropy', random_state=1, max_depth=3)
model_DT.fit(predictors_train, target_train)
```

- **What:** DT with entropy, depth 3.
- **Why:** Slightly deeper than Lab 3; balances expressiveness and overfitting.

---

### 2.3 Predict and evaluate DT

```python
prediction_on_test_DT = model_DT.predict(predictors_test)
cm_DT = confusion_matrix(target_test, prediction_on_test_DT)
ConfusionMatrixDisplay(confusion_matrix=cm_DT, display_labels=model_DT.classes_).plot()
print(classification_report(target_test, prediction_on_test_DT))
```

- **What:** Test predictions, confusion matrix, precision/recall/F1.
- **Why:** Baseline for comparison with NB.

---

### 2.4 Build and fit Naive Bayes

```python
model_NB = MultinomialNB()
model_NB.fit(predictors_train, target_train)
```

- **What:** Naive Bayes with default settings.
- **Why:** Fast probabilistic classifier; Lab compares it to DT.

---

### 2.5 Predict and evaluate NB

```python
prediction_on_test_NB = model_NB.predict(predictors_test)
print(classification_report(target_test, prediction_on_test_NB))
```

- **What:** Test predictions and metrics.
- **Why:** Compare with DT; typically NB has decent recall but lower precision (many false positives).

---

### 2.6 Compare train accuracy (optional)

```python
print("DT Train Accuracy:", model_DT.score(predictors_train, target_train))
print("NB Train Accuracy:", model_NB.score(predictors_train, target_train))
```

- **What:** In-sample accuracy for both.
- **Why:** Quick sanity check; test accuracy is what matters for generalization.

---

### 2.7 Plot decision tree (optional)

```python
tree.plot_tree(model_DT, feature_names=list(predictors_train.columns), ...)
tree.export_text(model_DT, feature_names=list(predictors_train.columns))
```

- **What:** Visual and text representation of the tree.
- **Why:** Interpretability; see which features drive splits.

---

## 3. Exam-Style Variants (Small Code Prompts)

1. Build a Naive Bayes model using MultinomialNB and fit it on training data.  
   *Answer:* `model = MultinomialNB()` then `model.fit(X_train, y_train)`

2. Predict on test data for both a DT and an NB model; print classification reports for each.  
   *Answer:* `y_pred_dt = model_DT.predict(X_test)`; `y_pred_nb = model_NB.predict(X_test)`; `print(classification_report(y_test, y_pred_dt))`; same for NB.

3. Which model typically has higher precision on this car dataset? Higher recall?  
   *Answer:* DT usually has higher precision; NB can have higher recall but lower precision (many false positives).

4. When would you prefer Naive Bayes over a Decision Tree?  
   *Answer:* When speed or simplicity matters, or when you care more about recall than precision. Also when data is limited.

5. What does MultinomialNB assume about the features?  
   *Answer:* Non-negative discrete/count data; features conditionally independent given the class.

---

## 4. Debugging Checklist (Common Errors)

- **MultinomialNB with negative values:** MultinomialNB expects non-negative inputs. If you have negative values after scaling, consider GaussianNB or MinMaxScaler (0–1) before NB.
- **Different metrics for DT vs NB:** Compare on the same test set; use classification_report for both.
- **Tree plot too large:** Use `max_depth` or `plt.figure(figsize=(...))` to control size.
- **Wrong target encoding:** Ensure target is 0/1 or Yes/No consistently; sklearn handles both.

---

## 5. Lab Cheat Sheet

| Task | Code |
|------|------|
| DT (Lab 4) | `DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)` |
| NB | `MultinomialNB()` |
| Fit | `model.fit(X_train, y_train)` |
| Predict | `model.predict(X_test)` |
| Classification report | `classification_report(y_test, y_pred)` |
| Train accuracy | `model.score(X_train, y_train)` |
| Tree plot | `tree.plot_tree(model, feature_names=...)` |
| Tree text | `tree.export_text(model, feature_names=...)` |

---

## 6. Key Takeaways (DT vs NB)

- **Decision Tree:** Better precision; interpretable (splits visible); may miss more bad buys (lower recall).
- **Naive Bayes:** Often higher recall; lower precision (many false alarms). Fast and simple.
- **Choosing:** If false positives are costly → prefer DT. If missing bad buys is costly → NB might be acceptable if you can tolerate more false alarms.

---

**Sources used:** IS670_lab04 (2).html — "IS 670 Lab 4: Decision Tree vs Naive Bayes"; car_kick dataset; DT (max_depth=3), MultinomialNB; confusion matrix, classification_report; DT vs NB comparison (precision, recall).
