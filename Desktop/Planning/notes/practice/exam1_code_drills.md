# IS 670 — Exam 1 Code Drills

**Purpose:** Practice code-writing prompts for exam prep. Answers are minimal; extend as needed.

---

## 1. Data Loading & Inspection

1. Load a CSV from path `'/content/drive/MyDrive/data.csv'` into `df` and show rows × columns.  
   **Answer:** `df = pd.read_csv('/content/drive/MyDrive/data.csv'); df.shape`

2. Count missing values per column.  
   **Answer:** `df.isnull().sum()`

3. Fill missing in categorical column `Type2` with `'None'`.  
   **Answer:** `df['Type2'] = df['Type2'].fillna('None')` or `df = df.fillna({'Type2':'None'})`

4. One-hot encode columns `Auction` and `Color`, dropping first.  
   **Answer:** `df = pd.get_dummies(df, columns=['Auction','Color'], drop_first=True)`

---

## 2. Define X, y, Split

5. Define `y` as `Class` and `X` as all other columns from `df`.  
   **Answer:** `y = df['Class']`; `X = df.drop(columns=['Class'])`

6. Split `X` and `y` into 70% train, 30% test with `random_state=42`.  
   **Answer:** `X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)`

---

## 3. Models

7. Build a DecisionTreeClassifier with entropy and max_depth=3.  
   **Answer:** `model = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=1)`

8. Fit the model on `X_train`, `y_train` and predict on `X_test`.  
   **Answer:** `model.fit(X_train, y_train)`; `y_pred = model.predict(X_test)`

9. Build a KNN with K=5. (Assume X is already scaled.)  
   **Answer:** `model = KNeighborsClassifier(n_neighbors=5)`; `model.fit(X_train, y_train)`

10. Build a Naive Bayes model (MultinomialNB).  
    **Answer:** `model = MultinomialNB()`; `model.fit(X_train, y_train)`

11. Scale `X_train` and `X_test` with MinMaxScaler (fit on train only).  
    **Answer:**  
    `scaler = MinMaxScaler()`  
    `X_train_scaled = scaler.fit_transform(X_train)`  
    `X_test_scaled = scaler.transform(X_test)`

---

## 4. Evaluation

12. Compute the confusion matrix for `y_test` and `y_pred`.  
    **Answer:** `cm = confusion_matrix(y_test, y_pred)`

13. Print precision, recall, and F1.  
    **Answer:** `print(classification_report(y_test, y_pred))`

14. What is the correct argument order for `confusion_matrix`?  
    **Answer:** `confusion_matrix(y_true, y_pred)` — actual first, predicted second.

---

## 5. Visualization

15. Draw a histogram of column `Attack` in DataFrame `df`.  
    **Answer:** `sns.histplot(x='Attack', data=df)`

16. Draw a boxplot of `VehBCost` grouped by `Class`.  
    **Answer:** `df.boxplot(column='VehBCost', by='Class')` or `sns.boxplot(x='Class', y='VehBCost', data=df)`

17. Draw a count plot of `Legendary` in `df`.  
    **Answer:** `sns.countplot(x='Legendary', data=df)`

---

## 6. Conceptual (Short Answer)

18. Why scale before KNN?  
    **Answer:** Distance is dominated by features with larger scales; scaling makes features comparable.

19. Why does K=1 overfit?  
    **Answer:** Each point's nearest neighbor is itself → memorizes labels → 100% train, poor test.

20. Why is accuracy misleading for imbalanced data?  
    **Answer:** A model predicting only the majority class can have high accuracy but 0 recall for the minority class.

21. What does max_depth do?  
    **Answer:** Limits tree depth; smaller max_depth = simpler model, less overfitting.

22. What does "naive" mean in Naive Bayes?  
    **Answer:** Features are assumed conditionally independent given the class.
