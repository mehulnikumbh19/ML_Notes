# IS 670 — Exam 1 Code Drills

**Purpose:** Practice code-writing prompts for exam prep (Canvas Part 3 style). Answers include short reasoning. Base: Labs 1–5 + Assignment 1.

---

## 1. Data Loading & Inspection

1. **Load a CSV from path `'/content/drive/MyDrive/data.csv'` into `df` and show rows × columns.**  
   - **Answer:** `df = pd.read_csv('/content/drive/MyDrive/data.csv'); df.shape`
   - **Reasoning:** `read_csv` loads CSV into a DataFrame; `shape` returns (rows, cols).

2. **Count missing values per column.**  
   - **Answer:** `df.isnull().sum()`
   - **Reasoning:** `isnull()` marks NaNs; `sum()` aggregates per column.

3. **Fill missing in categorical column `Type2` with `'None'`.**  
   - **Answer:** `df['Type2'] = df['Type2'].fillna('None')` or `df = df.fillna({'Type2':'None'})`
   - **Reasoning:** Never use `fillna` on numeric columns with strings—converts to object.

4. **One-hot encode columns `Auction` and `Color`, dropping first.**  
   - **Answer:** `df = pd.get_dummies(df, columns=['Auction','Color'], drop_first=True)`
   - **Reasoning:** sklearn needs numeric inputs; `drop_first` avoids multicollinearity.

---

## 2. Define X, y, Split

5. **Define `y` as `Class` and `X` as all other columns from `df`.**  
   - **Answer:** `y = df['Class']`; `X = df.drop(columns=['Class'])`
   - **Reasoning:** Target = what we predict; predictors = everything else.

6. **Split `X` and `y` into 70% train, 30% test with `random_state=42`.**  
   - **Answer:** `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)`
   - **Reasoning:** Fit on train, evaluate on test; `random_state` ensures reproducibility.

---

## 3. Models

7. **Build a DecisionTreeClassifier with entropy and max_depth=3.**  
   - **Answer:** `model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`
   - **Reasoning:** Lab 3–4 use `criterion='entropy'`; Assignment 1 may omit (default gini).

8. **Fit the model on `X_train`, `y_train` and predict on `X_test`.**  
   - **Answer:** `model.fit(X_train, y_train)`; `y_pred = model.predict(X_test)`
   - **Reasoning:** Always fit on train; predict on test for evaluation.

9. **Build a KNN with K=5. (Assume X is already scaled.)**  
   - **Answer:** `model = KNeighborsClassifier(n_neighbors=5)`; `model.fit(X_train, y_train)`
   - **Reasoning:** KNN uses distance; must scale before fitting if not pre-scaled.

10. **Build a Naive Bayes model (MultinomialNB).**  
    - **Answer:** `model = MultinomialNB()`; `model.fit(X_train, y_train)`
    - **Reasoning:** Lab 4 uses MultinomialNB for discrete/count features; use GaussianNB for continuous.

11. **Scale `X_train` and `X_test` with MinMaxScaler (fit on train only).**  
    - **Answer:**  
      `scaler = MinMaxScaler()`  
      `X_train_scaled = scaler.fit_transform(X_train)`  
      `X_test_scaled = scaler.transform(X_test)`
    - **Reasoning:** Fit only on train to avoid data leakage; transform test with same scaler.

12. **Build a Decision Tree with max_depth=5 (Assignment 1 style, no criterion).**  
    - **Answer:** `dt = DecisionTreeClassifier(max_depth=5, random_state=42)`
    - **Reasoning:** Assignment 1 uses default criterion (gini); explicit max_depth limits overfitting.

---

## 4. Evaluation

13. **Compute the confusion matrix for `y_test` and `y_pred`.**  
    - **Answer:** `cm = confusion_matrix(y_test, y_pred)`
    - **Reasoning:** Order is (y_true, y_pred)—actual first, predicted second.

14. **Print precision, recall, and F1.**  
    - **Answer:** `print(classification_report(y_test, y_pred))`
    - **Reasoning:** One call returns precision, recall, F1 per class and overall accuracy.

15. **What is the correct argument order for `confusion_matrix`?**  
    - **Answer:** `confusion_matrix(y_true, y_pred)` — actual first, predicted second.
    - **Reasoning:** sklearn convention: ground truth first.

16. **Compute AUC given `model` and `X_test`, `y_test` (binary 0/1).**  
    - **Answer:** `roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])`
    - **Reasoning:** AUC needs probabilities of positive class; `[:, 1]` is the positive-class column.

17. **Display a confusion matrix heatmap with labels ['Good Buy', 'Kick'].**  
    - **Answer:**  
      `cm = confusion_matrix(y_test, y_pred)`  
      `ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Good Buy', 'Kick']).plot()`
    - **Reasoning:** `ConfusionMatrixDisplay` produces a heatmap; `display_labels` names the classes.

---

## 5. Visualization

18. **Draw a histogram of column `Attack` in DataFrame `df`.**  
    - **Answer:** `sns.histplot(x='Attack', data=df)`
    - **Reasoning:** histplot shows distribution of a single numeric variable.

19. **Draw a boxplot of `VehBCost` grouped by `Class`.**  
    - **Answer:** `df.boxplot(column='VehBCost', by='Class')` or `sns.boxplot(x='Class', y='VehBCost', data=df)`
    - **Reasoning:** Boxplot by group shows spread and outliers per class.

20. **Draw a count plot of `Legendary` in `df`.**  
    - **Answer:** `sns.countplot(x='Legendary', data=df)`
    - **Reasoning:** Count plot for categorical frequencies.

21. **Plot a decision tree `model` with feature names (show first 3 levels).**  
    - **Answer:** `plot_tree(model, feature_names=X_train.columns.tolist(), max_depth=3, filled=True, rounded=True)`
    - **Reasoning:** `plot_tree` visualizes splits; `max_depth` limits displayed depth.

---

## 6. Conceptual (Short Answer)

22. **Why scale before KNN?**  
    - **Answer:** Distance is dominated by features with larger scales; scaling (e.g., MinMaxScaler) makes features comparable.
    - **Reasoning:** KNN uses Euclidean distance; unscaled features like VehicleAge vs VehOdo would be unfair.

23. **Why does K=1 overfit?**  
    - **Answer:** Each point's nearest neighbor is itself → memorizes labels → 100% train, poor test.
    - **Reasoning:** Lab 5: K=1 gives ~100% train, ~55% test; K=4 generalizes better.

24. **Why is accuracy misleading for imbalanced data?**  
    - **Answer:** A model predicting only the majority class can have high accuracy but 0 recall for the minority class.
    - **Reasoning:** E.g., 90% good buys → predict all good → 90% accuracy, 0% recall for kicks.

25. **What does max_depth do?**  
    - **Answer:** Limits tree depth; smaller max_depth = simpler model, less overfitting.
    - **Reasoning:** Deep trees memorize training data; shallow trees generalize better.

26. **What does "naive" mean in Naive Bayes?**  
    - **Answer:** Features are assumed conditionally independent given the class.
    - **Reasoning:** P(X|Class) ≈ product of P(x_i|Class); simplifies computation.

27. **Why fit the scaler on train only, not on the full dataset?**  
    - **Answer:** To avoid data leakage; test data must not influence preprocessing.
    - **Reasoning:** Fit on train, transform both train and test; test should be "unseen" until evaluation.

---

**Sources used:** Lab 1–5 walkthroughs; Assignment 1 walkthrough; Lecture 3–5 notes.
