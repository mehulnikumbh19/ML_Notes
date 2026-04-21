# IS 670 — Lab Syntax Reference (All Labs)

**Source:** Labs 1–5 (IS670_lab01–lab05 HTML + walkthroughs). Each syntax appears once with a short explanation.

---

## 1. Python & Colab

| Syntax | What it does |
|--------|----------------|
| `print("text")` | Prints the string to the output; confirms runtime works. |
| `from google.colab import drive` | Imports Colab’s Drive module so you can mount Drive. |
| `drive.mount('/content/drive')` | Mounts Google Drive at `/content/drive`; paths like `/content/drive/MyDrive/...` then work. |

---

## 2. Imports (libraries)

| Syntax | What it does |
|--------|----------------|
| `import pandas as pd` | Loads pandas for DataFrames and CSV; use `pd.read_csv`, `pd.get_dummies`, etc. |
| `import seaborn as sns` | Loads seaborn for histograms, boxplots, scatter, count plots, pair plots. |
| `from matplotlib import pyplot as plt` | Loads matplotlib for custom plots (e.g. ROC curve). |
| `from sklearn.model_selection import train_test_split` | Splits data into train and test sets. |
| `from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text` | Decision tree model plus tree visualization and text export. |
| `from sklearn.naive_bayes import MultinomialNB` | Naive Bayes for discrete/count (non‑negative) features. |
| `from sklearn.naive_bayes import GaussianNB` | Naive Bayes for continuous features (alternative to MultinomialNB). |
| `from sklearn.neighbors import KNeighborsClassifier` | K‑nearest neighbors classifier. |
| `from sklearn.preprocessing import MinMaxScaler` | Scales features to [0, 1] (needed for KNN). |
| `from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report` | Confusion matrix, its plot, and precision/recall/F1 report. |
| `from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score` | Single metric functions. |
| `from sklearn.metrics import roc_curve, roc_auc_score` | ROC curve (FPR/TPR) and AUC. |

---

## 3. Pandas — Load & inspect

| Syntax | What it does |
|--------|----------------|
| `pd.read_csv('path/to/file.csv')` | Reads a CSV file into a DataFrame. |
| `df = pd.read_csv(...)` | Stores the DataFrame in `df` (or any variable name). |
| `df.shape` | Returns (number of rows, number of columns). |
| `df.head()` | Shows the first 5 rows. |
| `df.head(n)` | Shows the first n rows. |
| `df.tail()` | Shows the last 5 rows. |
| `df.columns` | Column names (Index); use to check or pass to plot_tree/get_dummies. |
| `df.dtypes` | Data type of each column. |
| `df.describe()` | Numeric summary: count, mean, std, min, 25/50/75%, max. |

---

## 4. Pandas — Select columns & rows

| Syntax | What it does |
|--------|----------------|
| `df['ColName']` | Single column as a Series. |
| `df[['Col1','Col2']]` | Multiple columns as a DataFrame (note double brackets). |
| `df[df['col'] == value]` | Rows where `col` equals `value` (boolean indexing). |
| `df[df['Legendary'] == False]` | Filter to non‑Legendary rows (example). |

---

## 5. Pandas — Missing values

| Syntax | What it does |
|--------|----------------|
| `df.isnull()` | Boolean mask: True where value is NaN. |
| `df.isnull().sum()` | Count of missing values per column (Series). |
| `df.fillna('None')` | Replaces all NaN with the string `'None'` (for categorical only). |
| `df = df.fillna('None')` | Same, and reassigns so the DataFrame is updated. |
| `df['col'].fillna(df['col'].median())` | Fills numeric column with its median. |
| `df['col'].fillna(df['col'].mean())` | Fills numeric column with its mean. |
| `df['col'].fillna(df['col'].mode()[0])` | Fills categorical column with its mode. |
| `df.dropna()` | Drops rows that contain any NaN. |

---

## 6. Pandas — Encode & drop columns

| Syntax | What it does |
|--------|----------------|
| `pd.get_dummies(df, columns=['A','B',...], drop_first=True, dtype=int)` | One‑hot encodes listed columns to 0/1; drop_first avoids multicollinearity. |
| `df.drop(['Col'], axis=1)` | Drops column(s); returns new DataFrame unless inplace=True. |
| `df.drop(columns=['Col1','Col2'])` | Same idea, using column names. |
| `df.drop(columns=lst, errors='ignore')` | Drops columns in list; ignores missing column names. |

---

## 7. Pandas — Target and predictors

| Syntax | What it does |
|--------|----------------|
| `target = df['IsBadBuy']` | Defines the target (y) column. |
| `predictors = df.drop(['IsBadBuy'], axis=1)` | All columns except target (X). |
| `predictors = df.drop(columns=['IsBadBuy'])` | Same using `columns=` argument. |
| `y_test.map({'Yes': 1, 'No': 0})` | Maps label column to numeric 0/1 for ROC/AUC. |

---

## 8. Seaborn — Plots

| Syntax | What it does |
|--------|----------------|
| `sns.histplot(x='Col', data=df)` | Histogram of a numeric column. |
| `sns.countplot(x='Col', data=df)` | Bar chart of counts per category. |
| `sns.boxplot(x='Col', data=df)` | Boxplot (median, quartiles, whiskers, outliers). |
| `sns.boxplot(x='NumCol', y='CatCol', data=df)` | Boxplot of numeric variable by category. |
| `sns.boxplot(..., data=df[df['col']==value])` | Boxplot on a filtered subset of rows. |
| `sns.scatterplot(x='Col1', y='Col2', data=df)` | Scatter plot of two numeric columns. |
| `sns.pairplot(data=df)` | Grid of scatter plots (and diagonals) for numeric columns. |
| `sns.pairplot(data=df[['A','B','C']])` | Pair plot on a subset of columns (faster). |
| `snsplot = sns.histplot(...)` | Assigns the plot object so you can call methods on it. |
| `snsplot.set_title("Title")` | Sets the plot title. |
| `snsplot.set_xticklabels(snsplot.get_xticklabels(), rotation=40, ha="right")` | Rotates x‑axis labels to avoid overlap. |

---

## 9. Pandas — Plots

| Syntax | What it does |
|--------|----------------|
| `df.boxplot(column='Col')` | Pandas boxplot for one numeric column. |
| `df.boxplot(column='NumCol', by='CatCol')` | Boxplot of numeric column grouped by category. |
| `df.plot.scatter(x='Col1', y='Col2')` | Pandas scatter plot. |

---

## 10. sklearn — Train/test split

| Syntax | What it does |
|--------|----------------|
| `train_test_split(X, y, test_size=0.3, random_state=0)` | Splits into 70% train, 30% test; random_state for reproducibility. |
| `X_train, X_test, y_train, y_test = train_test_split(...)` | Unpacks the four arrays. |
| `train_test_split(..., stratify=y)` | Keeps class proportions in train and test (good for imbalanced y). |

---

## 11. sklearn — Preprocessing (scaling)

| Syntax | What it does |
|--------|----------------|
| `MinMaxScaler()` | Creates a scaler that maps each feature to [0, 1]. |
| `scaler.fit_transform(X_train)` | Fits on train and transforms it (use for training data). |
| `scaler.transform(X_test)` | Transforms test only; do not fit on test (avoids leakage). |
| `pd.DataFrame(scaler.fit_transform(X))` | Wraps result in DataFrame (fit_transform returns ndarray). |
| `X_scaled.columns = X.columns` | Restores column names after scaling. |

---

## 12. sklearn — Decision tree

| Syntax | What it does |
|--------|----------------|
| `DecisionTreeClassifier(criterion='entropy', max_depth=2, random_state=1)` | Tree with entropy split, max depth 2; random_state for reproducibility. |
| `DecisionTreeClassifier(criterion='gini', ...)` | Uses Gini impurity instead of entropy. |
| `DecisionTreeClassifier(max_depth=3, random_state=42)` | Another common pattern (e.g. Lab 4, Assignment). |
| `DecisionTreeClassifier()` | Unconstrained tree (can overfit; 100% train possible). |
| `model.fit(X_train, y_train)` | Fits the model on training data. |
| `model.predict(X_test)` | Predicts class labels for test data. |
| `model.predict_proba(X_test)` | Predicts class probabilities; use `[:, 1]` for positive class. |
| `model.predict_proba(X_test)[:, 1]` | Probability of the positive class (for ROC/AUC). |
| `model.classes_` | Array of class labels learned by the model. |
| `model.score(X, y)` | Returns accuracy on the given X and y. |

---

## 13. sklearn — Naive Bayes

| Syntax | What it does |
|--------|----------------|
| `MultinomialNB()` | Naive Bayes for discrete/count (non‑negative) features. |
| `GaussianNB()` | Naive Bayes for continuous features. |
| `model.fit(X_train, y_train)` | Same fit interface as other classifiers. |
| `model.predict(X_test)` | Same predict interface. |

---

## 14. sklearn — KNN

| Syntax | What it does |
|--------|----------------|
| `KNeighborsClassifier(n_neighbors=1)` | K=1; each point’s nearest neighbor is itself (overfits). |
| `KNeighborsClassifier(n_neighbors=4)` | K=4 (or 5) for better generalization. |
| `model.fit(X_train, y_train)` | Fit on scaled training data. |
| `model.predict(X_test)` | Predict on scaled test data. |

---

## 15. sklearn — Metrics

| Syntax | What it does |
|--------|----------------|
| `confusion_matrix(y_true, y_pred)` | Returns [[TN, FP], [FN, TP]]; order is (actual, predicted). |
| `ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_).plot()` | Plots confusion matrix as heatmap with model’s class labels. |
| `ConfusionMatrixDisplay.from_predictions(y_test, y_pred)` | Builds and can plot from y_test and y_pred directly. |
| `display_labels=['Good Buy','Kick']` | Custom labels on the confusion matrix plot. |
| `classification_report(y_test, y_pred)` | Prints precision, recall, F1 per class and accuracy. |
| `classification_report(y_test, y_pred, target_names=['A','B'])` | Same with custom class names. |
| `print(classification_report(...))` | Use print to see the report in output. |
| `accuracy_score(y_true, y_pred)` | Proportion of correct predictions. |
| `precision_score(y_test, y_pred, pos_label=1, zero_division=0)` | Precision for the positive class. |
| `recall_score(y_test, y_pred, pos_label=1)` | Recall for the positive class. |
| `f1_score(y_test, y_pred, pos_label=1)` | F1 for the positive class. |
| `roc_curve(y_true, y_prob)` | Returns fpr, tpr, thresholds; y_prob from predict_proba. |
| `roc_auc_score(y_test, y_prob)` | Area under ROC curve; y_test must be numeric 0/1. |

---

## 16. sklearn — Tree visualization

| Syntax | What it does |
|--------|----------------|
| `plot_tree(model, feature_names=X_train.columns.tolist(), max_depth=3, filled=True, rounded=True)` | Draws the decision tree; feature_names and max_depth control display. |
| `plot_tree(model, feature_names=list(X.columns), ...)` | Same with list of column names. |
| `export_text(model, feature_names=list(X.columns))` | Text representation of the tree rules. |

---

## 17. Matplotlib (with ROC)

| Syntax | What it does |
|--------|----------------|
| `plt.plot(fpr, tpr, label=f"AUC = {auc_score:.3f}")` | Plots ROC curve and adds a legend label. |
| `plt.legend()` | Shows legend (e.g. for multiple curves). |
| `plt.show()` | Displays the figure (in notebooks often automatic). |

---

## 18. Common patterns (no new syntax)

- **Filter then plot:** `sns.histplot(x='Revenue', data=df[df['Status']=='Active'])`
- **Scale then split:** Create `predictors_normalized`, then `train_test_split(predictors_normalized, target, ...)`
- **AUC workflow:** Map labels to 0/1 → get `y_prob = model.predict_proba(X_test)[:, 1]` → `roc_auc_score(y_test_bin, y_prob)` and optionally `roc_curve` for plotting.

---

**Lab coverage:** Lab 1 (Colab, pandas, seaborn basics); Lab 2 (missing values, fillna, boxplot, scatter, pairplot, filter); Lab 3 (get_dummies, train_test_split, DecisionTreeClassifier, confusion matrix, classification_report, ROC/AUC); Lab 4 (Decision Tree vs MultinomialNB, plot_tree, export_text, model.score); Lab 5 (MinMaxScaler, KNN n_neighbors=1 and 4, accuracy_score, overfitting vs generalization).  
**Note:** Lab 6 is not in the provided materials; this reference covers Labs 1–5 only.
