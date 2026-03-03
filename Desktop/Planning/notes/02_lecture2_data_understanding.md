# Lecture 2: Data Understanding & Exploration (IS 670)

**Big picture:** Before building any ML model, you must understand your data—its structure, quality, and patterns. Data understanding (part of CRISP-DM) covers loading, inspecting, handling missing values, and visualizing distributions and relationships. This feeds into preprocessing and modeling.

---

## 1. Big Picture (Business Analytics Framing)

- **Why data understanding first?** Garbage in → garbage out. You need to know variable types, missing values, outliers, and relationships to choose the right model and features.
- **Business context:** In the Car dataset (Assignment 1), understanding that Class (good buy vs kick) is imbalanced guides how you evaluate models. In Pokemon, knowing Type2 has many missing values informs how you handle it.
- **CRISP-DM:** Data Understanding is a phase between Business Understanding and Data Preparation; exploration and visualization sit here.

---

## 2. Concepts from Scratch

### 2.1 Variable types

- **Numeric (continuous/discrete):** Attack, Defense, HP, VehicleAge, VehBCost — use histograms, boxplots, scatter plots.
- **Categorical (nominal/ordinal):** Type1, Legendary, IsBadBuy — use count plots; can group numeric by category (boxplot of Attack by Type1).

### 2.2 Missing values

- **Detection:** `df.isnull().sum()` gives count of missing per column.
- **Interpretation:** Missing can mean "not applicable" (e.g., Type2 for single-type Pokemon) or data error.
- **Handling (as taught in lab):** For categorical, `fillna('None')` to treat missing as a category; for numeric, options include drop, median/mean impute, or model-specific handling (covered later).

### 2.3 Visualization by purpose

| Goal | Numeric | Categorical | Numeric vs categorical |
|------|---------|-------------|------------------------|
| Distribution | Histogram, boxplot | Count plot | Boxplot (numeric by category) |
| Relationship (2 numerics) | Scatter plot | — | — |
| Many numerics | Pair plot | — | — |

---

## 3. Definitions (Exact + Beginner-Friendly)

| Term | Definition |
|------|------------|
| **Data exploration** | Inspecting and visualizing data to understand structure, quality, and patterns before modeling. |
| **Missing value** | No recorded value (NaN, null); must be detected and handled. |
| **Outlier** | Value far from the rest; boxplots help spot them (points beyond whiskers). |
| **Histogram** | Bars showing frequency of values in bins; shows shape of distribution. |
| **Boxplot** | Shows median, quartiles, whiskers; points beyond whiskers = potential outliers. |
| **Scatter plot** | One point per row; x and y are two numeric variables; shows relationship. |
| **Count plot** | Bars showing frequency of each category. |
| **Pair plot** | Grid of scatter (and sometimes histogram) plots for multiple numeric variables. |

---

## 4. Key Formulas

*No formulas in Lecture 2; focus is on inspection and visualization. Summary stats (mean, median) come from `df.describe()` — covered in lab.*

---

## 5. Worked Example (Mirror Lab 2 Style)

**Goal:** Load Pokemon, find missing values, handle Type2 missing, and explore numeric + categorical variables.

1. **Load and inspect:**
   ```python
   pokemon = pd.read_csv('path/to/pokemon.csv')
   pokemon.shape   # (800, 12)
   pokemon.head(); pokemon.tail()
   ```

2. **Missing values:**
   ```python
   pokemon.isnull().sum()   # Type2: 386
   pokemon = pokemon.fillna('None')   # treat as category
   pokemon.isnull().sum()   # all 0
   ```

3. **Visualizations:**
   - **Histogram:** `sns.histplot(x='Attack', data=pokemon)` + `set_title(...)`
   - **Boxplot (numeric):** `sns.boxplot(x='Attack', data=pokemon)` or `df.boxplot(column='VehBCost')` (pandas)
   - **Count plot:** `sns.countplot(x='Type1', data=pokemon)`; rotate labels: `snsplot.set_xticklabels(snsplot.get_xticklabels(), rotation=40, ha='right')`
   - **Scatter:** `sns.scatterplot(x='Attack', y='Defense', data=pokemon)` or `df.plot.scatter(x='VehBCost', y='MMRCurrentAuctionAveragePrice')`
   - **Boxplot by group:** `sns.boxplot(x='Attack', y='Type1', data=pokemon)` — numeric by categorical
   - **Filter then plot:** `sns.boxplot(..., data=pokemon[pokemon['Legendary']==False])`
   - **Pair plot:** `sns.pairplot(data=pokemon)` — many numeric vars at once (can be slow for many columns)

---

## 6. Common Mistakes / Misconceptions

- **Filling numeric missing with string:** `fillna('None')` converts a column to object type; use only for categorical. For numeric, use `fillna(0)`, `fillna(median)`, or drop.
- **Overlapping variable names:** Lab uses both `sns.boxplot` and `df.boxplot`; `df.boxplot(column=..., by=...)` groups by a categorical column.
- **Pair plot on too many columns:** All numeric columns → huge grid. Select a subset: `sns.pairplot(data=df[['col1','col2','col3']])`.
- **Forgetting to check missing after cleaning:** Run `isnull().sum()` again to verify.

---

## 7. Mini-Check Quiz (5–10 Qs) + Answers

1. How do you count missing values per column?  
   **Answer:** `df.isnull().sum()`

2. What does `fillna('None')` do? When is it appropriate?  
   **Answer:** Replaces missing values with the string `'None'`. Appropriate for categorical columns (e.g., Type2) where missing means "no secondary type."

3. Which plot shows the distribution of a numeric variable?  
   **Answer:** Histogram or boxplot.

4. Which plot shows the relationship between two numeric variables?  
   **Answer:** Scatter plot.

5. How do you create a boxplot of a numeric variable grouped by a categorical variable?  
   **Answer:** `sns.boxplot(x='numeric_col', y='categorical_col', data=df)` — or `x` and `y` swapped depending on orientation desired.

6. What is a pair plot used for?  
   **Answer:** Viewing relationships between multiple numeric variables in a grid of scatter (and sometimes histogram) plots.

7. How do you rotate x-axis labels in a seaborn count plot?  
   **Answer:** `snsplot.set_xticklabels(snsplot.get_xticklabels(), rotation=40, ha='right')`

8. How do you filter a DataFrame before plotting (e.g., only non-legendary Pokemon)?  
   **Answer:** `data=df[df['Legendary']==False]` or `data=df[df['Column']==value]`

---

## 8. TL;DR Cheat Sheet

- **Load:** `pd.read_csv(path)`; **inspect:** `shape`, `head()`, `tail()`
- **Missing:** `df.isnull().sum()`; **fill categorical:** `df.fillna('None')`
- **Histogram:** `sns.histplot(x='col', data=df)`
- **Boxplot:** `sns.boxplot(x='col', data=df)` or `df.boxplot(column='col')`; by group: `sns.boxplot(x='num', y='cat', data=df)` or `df.boxplot(column='num', by='cat')`
- **Count plot:** `sns.countplot(x='col', data=df)`; rotate labels with `set_xticklabels(..., rotation=..., ha='right')`
- **Scatter:** `sns.scatterplot(x='col1', y='col2', data=df)` or `df.plot.scatter(x='c1', y='c2')`
- **Pair plot:** `sns.pairplot(data=df)` (subset columns if many)
- **Filter:** `df[df['col']==value]` for subsetting before plotting

---

**Sources used:** Lab 2 (IS670_lab02-1.html) — Part 1 Pokemon (variable descriptions, upload/clean, missing values, fillna, boxplot, histogram, countplot, scatter, pairplot, boxplot by group); Part 2 CarAuction (isnull, boxplot, scatter, boxplot by IsBadBuy). Course map. Lecture slides not in provided material; add slide refs when available.
