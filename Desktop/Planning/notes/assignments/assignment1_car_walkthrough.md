# Assignment 1 Walkthrough: Don't Get Kicked (Car)

**Assignment objective:** Apply CRISP-DM to the Don't Get Kicked car auction dataset: Business Understanding, Data Understanding, Data Preparation, Modeling (Decision Trees with varying max_depth), and Evaluation. Predict Class (0 = good buy, 1 = kick). Exam-relevant patterns throughout.

**Source:** NikumbhMehul.html (Assignment1_Car)

---

## 1. Structure (CRISP-DM)

| Phase | Content |
|-------|---------|
| **Business Understanding** | Problem framing; target (Class); goal for dealers |
| **Data Understanding** | Variable definitions; shape, dtypes; kick rate; visualizations |
| **Data Preparation** | Drop cols; handle missing (median/mode); outliers (IQR); one-hot encode |
| **Modeling** | DecisionTreeClassifier with max_depth variants |
| **Evaluation** | classification_report, confusion matrix, plot_tree |

---

## 2. Business Understanding

- **Problem:** Dealers buy cars at auction; some turn out to be "kicks" (bad buys) due to odometer tampering, title issues, engine damage, etc.
- **Target:** `Class` — 0 = good buy, 1 = kick.
- **Goal:** Build a model to flag risky cars at auction time so dealers can avoid or bid lower.

---

## 3. Data Understanding

- **Dataset:** Carvana/Kaggle "Don't Get Kicked"; ~67k rows, 31 columns.
- **Key variables:** VehicleAge, VehOdo, VehBCost, WarrantyCost, Auction, Make, Color, Size, TopThreeAmericanName, etc.
- **Imbalance:** Kick rate ~9.55% (minority class).
- **Code patterns:**
  ```python
  df.shape
  df.dtypes
  df.describe()
  df['Class'].value_counts(normalize=True)
  # Kick rate
  kick_rate = df['Class'].mean() * 100
  ```

---

## 4. Data Preparation

### 4.1 Drop columns

- Drop: PurchDate, Model, Trim, SubModel, BYRNO, VNZIP1, VehYear (redundant with VehicleAge).
- **Code:** `df_clean = df.drop(columns=drop_cols, errors='ignore')`

### 4.2 Handle missing

- Numeric: `fillna(median)`  
- Categorical: `fillna(mode)`

### 4.3 Outliers (optional)

- IQR method: `Q1 = col.quantile(0.25)`, `Q3 = col.quantile(0.75)`, `IQR = Q3 - Q1`, bounds = Q1 − 1.5×IQR, Q3 + 1.5×IQR.

### 4.4 One-hot encode categoricals

- Use `pd.get_dummies(df_clean, columns=categorical_cols, drop_first=True)` before modeling.
- Ensure no missing values remain.

---

## 5. Modeling

### 5.1 Define X and y

```python
X = df_clean.drop(columns=['Class'])
y = df_clean['Class']
```

### 5.2 Train/test split

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
```

### 5.3 Decision Tree variants

| Model | max_depth | Use |
|-------|-----------|-----|
| dt_full | None (unlimited) | Overfitting baseline |
| dt_d3 | 3 | Moderate complexity |
| dt_d5 | 5 | Moderate |
| dt_d7 | 7 | Deeper |
| dt_d10 | 10 | Deep |

```python
dt_full = DecisionTreeClassifier(random_state=42)
dt_d3 = DecisionTreeClassifier(max_depth=3, random_state=42)
dt_d5 = DecisionTreeClassifier(max_depth=5, random_state=42)
# ... fit each on X_train, y_train
```

### 5.4 Predict and evaluate

```python
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=['Good Buy', 'Kick']))
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Good Buy', 'Kick']).plot()
```

### 5.5 Plot tree (optional)

```python
from sklearn.tree import plot_tree
plot_tree(model, max_depth=3, filled=True, rounded=True, feature_names=X.columns.tolist())
```

---

## 6. Key Takeaways for Exam

- **Class imbalance:** Don't rely on accuracy; use precision, recall, F1 for minority class (Kick).
- **max_depth vs overfitting:** Full tree → overfitting; limit depth for generalization.
- **CRISP-DM:** Business → Data Understanding → Preparation → Modeling → Evaluation.
- **Metrics order:** confusion_matrix(y_true, y_pred); classification_report(y_true, y_pred).
- **One-hot before split:** Or fit encoder on train, transform both; ensure no test leakage.

---

## 7. Exam-Style Code Prompts

1. Define target and predictors from `df_clean` where target is `Class`.  
   *Answer:* `y = df_clean['Class']`; `X = df_clean.drop(columns=['Class'])`

2. Split X and y into 70% train, 30% test with random_state=42.  
   *Answer:* `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)`

3. Build a DecisionTreeClassifier with max_depth=5 and fit on train.  
   *Answer:* `dt = DecisionTreeClassifier(max_depth=5, random_state=42)`; `dt.fit(X_train, y_train)`

4. Print classification report with labels ['Good Buy', 'Kick'].  
   *Answer:* `print(classification_report(y_test, y_pred, target_names=['Good Buy', 'Kick']))`

5. Why is accuracy misleading for this dataset?  
   *Answer:* Imbalanced classes (~9% kicks); a model predicting all good buys would have ~90% accuracy but 0% recall for kicks.

---

**Sources used:** NikumbhMehul.html — Assignment 1 (Assignment1_Car); Business/Data Understanding, Data Preparation (drop, fillna, get_dummies), Modeling (DecisionTreeClassifier, max_depth 3/5/7/10, full), classification_report, confusion_matrix, plot_tree.
