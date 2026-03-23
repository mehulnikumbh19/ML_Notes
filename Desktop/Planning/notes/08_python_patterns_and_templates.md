# IS 670 — Python Patterns & Templates

**Purpose:** Reusable code patterns from Labs 1–5 and Assignment 1 for exam and project work.

---

## 1. Data Loading & Inspection

```python
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

# Load
df = pd.read_csv('path/to/file.csv')
df.shape
df.head()
df.dtypes
df.describe()
df.isnull().sum()
```

---

## 2. Preprocessing

```python
# Fill categorical missing
df = df.fillna('None')  # for categorical only

# Fill numeric missing
df['col'] = df['col'].fillna(df['col'].median())

# One-hot encode
df = pd.get_dummies(df, columns=['Auction','Color','Size'], drop_first=True)

# Drop columns
df = df.drop(columns=['id','date_col'], errors='ignore')
```

---

## 3. Define X and y

```python
target = df['IsBadBuy']  # or 'Class'
predictors = df.drop(columns=['IsBadBuy'], axis=1)
# Or: X = df.drop(columns=['Class']); y = df['Class']
```

---

## 4. Train/Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(
    predictors, target, test_size=0.3, random_state=42
)
```

---

## 5. Decision Tree

```python
model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

---

## 6. Naive Bayes

```python
model = MultinomialNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
```

---

## 7. KNN (with scaling)

```python
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # transform only, not fit

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)
```

---

## 8. Evaluation

```python
# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_).plot()

# Classification report
print(classification_report(y_test, y_pred))

# Single metrics (pos_label for minority class in imbalanced data)
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
accuracy_score(y_test, y_pred)
precision_score(y_test, y_pred, pos_label=1)
recall_score(y_test, y_pred, pos_label=1)
f1_score(y_test, y_pred, pos_label=1)

# ROC/AUC (Lab 3) — needs numeric y (0/1) and probabilities
from sklearn.metrics import roc_curve, roc_auc_score
y_prob = model.predict_proba(X_test)[:, 1]  # probability of positive class
auc_score = roc_auc_score(y_test, y_prob)
# roc_curve for plotting: fpr, tpr, _ = roc_curve(y_test, y_prob)
```

---

## 9. Visualization (Data Understanding)

```python
# Histogram
sns.histplot(x='Attack', data=df)

# Boxplot
sns.boxplot(x='col', data=df)
sns.boxplot(x='num', y='cat', data=df)  # by group
df.boxplot(column='VehBCost', by='Class')

# Count plot
sns.countplot(x='Legendary', data=df)

# Scatter
sns.scatterplot(x='Attack', y='Defense', data=df)

# Pair plot
sns.pairplot(data=df[['col1','col2','col3']])
```

---

## 10. Plot Decision Tree

```python
from sklearn.tree import plot_tree
plot_tree(model, feature_names=X_train.columns.tolist(), max_depth=3, filled=True, rounded=True)
```

---

## 11. Full Pipeline (End-to-End Reference)

```python
# 1. Load & inspect
df = pd.read_csv('data.csv')
df.shape; df.dtypes; df.isnull().sum()

# 2. Preprocess
df = df.fillna({'cat_col': 'None'})
df['num_col'] = df['num_col'].fillna(df['num_col'].median())
df = pd.get_dummies(df, columns=['A','B'], drop_first=True)

# 3. X, y
X = df.drop(columns=['target'])
y = df['target']

# 4. Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 5. (KNN only) Scale
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 6. Model
model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)
model.fit(X_train, y_train)

# 7. Predict & evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
cm = confusion_matrix(y_test, y_pred)
```

---

**Sources used:** Lab 1–5 HTML; Assignment 1 (NikumbhMehul.html); Lecture notes 1–6.
