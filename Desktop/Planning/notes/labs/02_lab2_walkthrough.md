# Lab 2 Walkthrough: Data Exploration

**Lab objective:** Explore and understand tabular data: load it, check for missing values, handle them, and create visualizations (histograms, boxplots, count plots, scatter plots, pair plots, boxplots by group). Uses Pokemon and CarAuction datasets. Trains data understanding skills needed before any modeling.

---

## 1. Step-by-Step Procedure (Recipe)

1. **Part 1 — Pokemon:** Mount Drive → import → read pokemon.csv → shape, head, tail → `isnull().sum()` → `fillna('None')` → verify missing → boxplots (Attack, Defense; by Generation) → histograms (Attack, Defense) → count plots (Type1, Legendary) → scatter (Attack vs Defense) → pair plot → boxplot Attack by Type1 (overall, non-Legendary, Legendary).
2. **Part 2 — CarAuction:** Read car data → shape, head, tail → `isnull().sum()` → boxplots (VehBCost, VehicleAge) → scatter (VehBCost vs MMRCurrentAuctionAveragePrice) → boxplot VehBCost by IsBadBuy.

---

## 2. Code Blocks Explained

### 2.1 Mount Drive, import, read (same as Lab 1)

```python
from google.colab import drive
drive.mount('/content/drive')
import pandas as pd
import seaborn as sns
pokemon = pd.read_csv('/content/drive/MyDrive/IS 670/pokemon.csv')
pokemon
```

- **What:** Loads the Pokemon dataset.
- **Why:** Foundation for all exploration.

---

### 2.2 Shape, head, tail

```python
pokemon.shape    # (800, 12)
pokemon.head()   # first 5 rows
pokemon.tail()   # last 5 rows
```

- **What:** shape = (rows, cols); head/tail show sample rows.
- **Why:** Quick check of size and structure; tail often reveals encoding/format issues.

---

### 2.3 Examine missing values

```python
# Examine missing values
pokemon.isnull().sum()
```

- **What:** Returns count of missing (NaN) per column. In Pokemon, Type2 has 386 missing.
- **Why:** Must identify missing before modeling; many models/sklearn don't accept NaN.

---

### 2.4 Handle missing — fill with 'None' (categorical)

```python
# Set missing values as none
pokemon = pokemon.fillna('None')
# Examine missing values again
pokemon.isnull().sum()
```

- **What:** Replaces all NaN with the string `'None'`. Second `isnull().sum()` should show 0.
- **Why:** Type2 is categorical; "missing" often means no secondary type. Treating as category avoids dropping rows.

---

### 2.5 Boxplot (numeric) — seaborn

```python
snsplot = sns.boxplot(x='Attack', data=pokemon)
snsplot.set_title("Boxplot of Attack in the pokemon data set")
```

- **What:** Box shows median, quartiles; whiskers extend to 1.5×IQR; points beyond = outliers.
- **Why:** See spread, skew, and outliers in one plot.

---

### 2.6 Boxplot filtered by category

```python
snsplot = sns.boxplot(x='Attack', data=pokemon[pokemon['Generation']==1])
snsplot.set_title("Boxplot of Attack of the 1st generation pokemon")
```

- **What:** Same boxplot, but only rows where Generation == 1.
- **Why:** Compare distributions across subsets (e.g., by generation).

---

### 2.7 Histogram (numeric)

```python
snsplot = sns.histplot(x='Attack', data=pokemon)
snsplot.set_title("Histogram of Attack in the pokemon data set")
```

- **What:** Bars show frequency of values in bins.
- **Why:** Visualize distribution shape (symmetric, skewed, multimodal).

---

### 2.8 Count plot with rotated labels

```python
snsplot = sns.countplot(x='Type1', data=pokemon)
snsplot.set_xticklabels(snsplot.get_xticklabels(), rotation=40, ha="right")
snsplot.set_title("countplot of Type1 in the pokemon data set")
```

- **What:** Bars for each category count; labels rotated so they don't overlap.
- **Why:** Many categories (Type1) need rotation for readability.

---

### 2.9 Scatter plot (two numeric variables)

```python
# scatter plot two numeric variables: Attack and Defense
snsplot = sns.scatterplot(x='Attack', y='Defense', data=pokemon)
snsplot.set_title("Scatterplot of Attack and Defense")
```

- **What:** One point per row; x=Attack, y=Defense.
- **Why:** See relationship (correlation, clusters) between two numerics.

---

### 2.10 Pair plot

```python
# Generate 2D scatter plots
sns.pairplot(data=pokemon)
```

- **What:** Grid of scatter plots (and diagonals) for all numeric columns.
- **Why:** Quick overview of pairwise relationships; can be slow with many columns — consider `sns.pairplot(data=pokemon[['Attack','Defense','HP']])` for a subset.

---

### 2.11 Boxplot: numeric by categorical

```python
# boxplot: numeric grouped by categorical
snsplot = sns.boxplot(x='Attack', y='Type1', data=pokemon)
snsplot.set_title("Boxplot of Attack based on pokemon type")
```

- **What:** One box per category of Type1; x is Attack.
- **Why:** Compare distribution of a numeric variable across categories.

---

### 2.12 Boxplot by group (filtered)

```python
# Non-Legendary only
snsplot = sns.boxplot(x='Attack', y='Type1', data=pokemon[pokemon['Legendary']==False])
snsplot.set_title("Boxplot of Attack based on pokemon type for non-Legendary pokemon")

# Legendary only
snsplot = sns.boxplot(x='Attack', y='Type1', data=pokemon[pokemon['Legendary']==True])
snsplot.set_title("Boxplot of Attack based on pokemon type for Legendary pokemon")
```

- **What:** Same as 2.11 but only Legendary==False or Legendary==True rows.
- **Why:** Compare behavior of a subgroup.

---

### 2.13 Part 2 — CarAuction: pandas boxplot

```python
carAuction = pd.read_csv('path/to/training.csv')  # path as in lab
carAuction.shape
carAuction.head()
carAuction.isnull().sum()
carAuction.boxplot(column='VehBCost')
carAuction.boxplot(column='VehicleAge')
```

- **What:** Pandas built-in `boxplot(column=...)` for single numeric.
- **Why:** Alternative to seaborn; useful when you prefer pandas style.

---

### 2.14 Scatter (pandas)

```python
carAuction.plot.scatter(x='VehBCost', y='MMRCurrentAuctionAveragePrice')
```

- **What:** Scatter using pandas `.plot.scatter`.
- **Why:** Another way to plot; result similar to `sns.scatterplot`.

---

### 2.15 Boxplot by group (pandas)

```python
# boxplot VehBCost based on IsBadBuy
carAuction.boxplot(column='VehBCost', by='IsBadBuy')
```

- **What:** One box per value of IsBadBuy (0 vs 1); compares VehBCost across good vs bad buy.
- **Why:** See if target (IsBadBuy) relates to a predictor (VehBCost).

---

## 3. Exam-Style Variants (Small Code Prompts)

1. Count missing values per column in DataFrame `df`.  
   *Answer:* `df.isnull().sum()`

2. Replace missing values in `df` with the string `"Missing"`.  
   *Answer:* `df = df.fillna('Missing')`

3. Create a boxplot of column `Salary` in `df` using seaborn.  
   *Answer:* `sns.boxplot(x='Salary', data=df)` or `sns.boxplot(x=df['Salary'])`

4. Create a scatter plot of `Age` vs `Income` in `df` using seaborn.  
   *Answer:* `sns.scatterplot(x='Age', y='Income', data=df)`

5. Create a count plot of the categorical column `Region` in `df`, with x-axis labels rotated 45°.  
   *Answer:* `snsplot = sns.countplot(x='Region', data=df)` then `snsplot.set_xticklabels(snsplot.get_xticklabels(), rotation=45, ha='right')`

6. Create a boxplot of `Sales` grouped by `Region` (Region on y-axis, Sales on x-axis).  
   *Answer:* `sns.boxplot(x='Sales', y='Region', data=df)`

7. Filter `df` to rows where `Status` equals `"Active"` and then create a histogram of `Revenue`.  
   *Answer:* `sns.histplot(x='Revenue', data=df[df['Status']=='Active'])`

8. Use pandas to create a boxplot of `Price` grouped by `Category`.  
   *Answer:* `df.boxplot(column='Price', by='Category')`

---

## 4. Debugging Checklist (Common Errors)

- **`isnull().sum()` shows nothing or wrong type:** Ensure you're calling on a DataFrame; result is a Series. Use `df.isnull().sum()` not `df.isnull.sum()`.
- **`fillna` changes dtype:** Filling numeric with `'None'` converts to object; use only for categorical. For numeric, use `fillna(0)`, `fillna(df['col'].median())`, or `dropna()`.
- **Boxplot/scatter shows empty or wrong:** Check column names exist: `df.columns`. Ensure correct `data=df` and `x`/`y` as strings.
- **Count plot labels overlap:** Add `set_xticklabels(..., rotation=40, ha='right')`.
- **Pair plot very slow:** Use a subset of columns: `sns.pairplot(data=df[['col1','col2','col3']])`.
- **`by=` in pandas boxplot:** `df.boxplot(column='numeric_col', by='categorical_col')` — `by` must be a column name.

---

## 5. Lab Cheat Sheet

| Task | Code |
|------|------|
| Missing count | `df.isnull().sum()` |
| Fill categorical missing | `df = df.fillna('None')` |
| Boxplot (seaborn) | `sns.boxplot(x='col', data=df)` |
| Boxplot filtered | `sns.boxplot(..., data=df[df['col']==value])` |
| Boxplot numeric by categorical | `sns.boxplot(x='num', y='cat', data=df)` |
| Histogram | `sns.histplot(x='col', data=df)` |
| Count plot | `sns.countplot(x='col', data=df)` |
| Rotate labels | `snsplot.set_xticklabels(snsplot.get_xticklabels(), rotation=40, ha='right')` |
| Scatter (seaborn) | `sns.scatterplot(x='c1', y='c2', data=df)` |
| Scatter (pandas) | `df.plot.scatter(x='c1', y='c2')` |
| Pair plot | `sns.pairplot(data=df)` |
| Boxplot (pandas, single) | `df.boxplot(column='col')` |
| Boxplot (pandas, by group) | `df.boxplot(column='num', by='cat')` |
| Filter rows | `df[df['col']==value]` |

---

**Sources used:** IS670_lab02-1.html — "IS 670 Lab 2: Data Exploration"; Part 1 Pokemon (variable descriptions, upload/clean, isnull, fillna, boxplot, histogram, countplot, scatterplot, pairplot, boxplot by Type1 and by Legendary); Part 2 CarAuction (read, isnull, boxplot, scatter, boxplot by IsBadBuy).
