# Lab 1 Walkthrough: Introduction to Colab

**Lab objective:** Use Google Colab, run Python in cells, load a CSV into a pandas DataFrame, inspect it, and create simple visualizations (histogram and count plot). This trains the environment and basic data-inspection skills used in every later lab.

---

## 1. Step-by-Step Procedure (Recipe)

1. Open a new Colab notebook (or the lab notebook).
2. **Part 1 — Colab:** Create text and code cells; run a code cell; add/move/delete cells; save and download.
3. **Part 2 — Python & data:** Mount Drive → import pandas and seaborn → read `pokemon.csv` → inspect (shape, head, single column, multiple columns) → plot Attack (histogram) and Legendary (count plot).

---

## 2. Code Blocks Explained

### 2.1 Run a simple print (verify runtime)

```python
print("IS670 lab1")
```

- **What it does:** Prints the string to the output area below the cell.
- **Why:** Confirms the notebook is connected to a Python runtime and that execution works.

---

### 2.2 Mount Google Drive (Colab only)

```python
# Mounting Google Drive
from google.colab import drive
drive.mount('/content/drive')
```

- **What it does:** Asks for permission to access your Google Drive and mounts it at `/content/drive`. After that, paths like `/content/drive/MyDrive/...` point to your Drive files.
- **Why:** The lab assumes `pokemon.csv` is in Drive (e.g. `MyDrive/IS 670/pokemon.csv`). Without mounting, `read_csv` cannot see that path.

---

### 2.3 Import libraries

```python
# Import libraries
import pandas as pd
import seaborn as sns
```

- **What it does:** Loads the `pandas` library (as `pd`) for DataFrames and the `seaborn` library (as `sns`) for plots.
- **Why:** `pd.read_csv` and `sns.histplot` / `sns.countplot` are used next. Run this cell before any cell that uses `pd` or `sns`.

---

### 2.4 Read CSV into a DataFrame

```python
# Read data (with assignment operator)
pokemon = pd.read_csv('/content/drive/MyDrive/IS 670/pokemon.csv')
# pokemon is a dataframe
pokemon
```

- **What it does:** Reads the CSV file from the given path and stores the table in the variable `pokemon`. The last line `pokemon` displays the DataFrame in the output.
- **Why:** All later steps (shape, head, plots) use this DataFrame. Adjust the path if your file is in a different folder in Drive.

---

### 2.5 Number of rows and columns

```python
# Examine the number of rows and cols
pokemon.shape
```

- **What it does:** Returns a tuple `(rows, columns)`, e.g. `(800, 12)`.
- **Why:** Quick check that the data loaded correctly and how big it is.

---

### 2.6 First rows

```python
# Show the head rows of a data frame
pokemon.head()
```

- **What it does:** Shows the first 5 rows of the DataFrame.
- **Why:** Lets you see column names and sample values without printing the whole table.

---

### 2.7 One column / two columns

```python
# Obtain the Attack value for every pokemon
pokemon['Attack']

# Obtain the Attack and Defense values for every pokemon
pokemon[['Attack', 'Defense']]
```

- **What it does:** `pokemon['Attack']` returns a single column (Series); `pokemon[['Attack', 'Defense']]` returns a DataFrame with two columns.
- **Why:** Selecting columns is needed for plotting and later for defining predictors. Single bracket = one column; double brackets = list of columns.

---

### 2.8 Histogram of a numeric variable

```python
# Histogram of Attack
snsplot = sns.histplot(x='Attack', data=pokemon)
snsplot.set_title("Histogram of Attack in the pokemon data set")
```

- **What it does:** Builds a histogram of the `Attack` column and sets the plot title.
- **Why:** Histograms show the distribution of a numeric variable; essential for data understanding and later for checking scaling/outliers.

---

### 2.9 Count plot of a categorical variable

```python
# Plot a categorical variable: Legendary
snsplot = sns.countplot(x='Legendary', data=pokemon)
snsplot.set_title("Countplot of Legendary in the pokemon data set")
```

- **What it does:** Counts how many rows fall in each category of `Legendary` (True/False) and shows bars.
- **Why:** For categorical variables, counts (or proportions) are the main summary; this matches Lab 2 “Data Exploration” and any binary target (e.g. Legendary vs not).

---

## 3. Exam-Style Variants (Small Code Prompts)

1. **Load a CSV** from path `'/content/drive/MyDrive/data.csv'` into a variable `df` and display the number of rows and columns.  
   *Answer:* `df = pd.read_csv('/content/drive/MyDrive/data.csv'); df.shape`

2. **Show the first 3 rows** of a DataFrame `df`.  
   *Answer:* `df.head(3)`

3. **Select two columns** named `Age` and `Income` from `df`.  
   *Answer:* `df[['Age', 'Income']]`

4. **Draw a histogram** of the column `Income` in DataFrame `df`.  
   *Answer:* `sns.histplot(x='Income', data=df)` (optionally assign to a variable and add a title).

5. **Draw a count plot** of the column `Region` in `df`.  
   *Answer:* `sns.countplot(x='Region', data=df)`

6. **What is the difference** between `df['A']` and `df[['A']]`?  
   *Answer:* `df['A']` is a Series (one column); `df[['A']]` is a DataFrame with one column. Both contain the same data; the second keeps it as a table.

---

## 4. Debugging Checklist (Common Errors)

- **`FileNotFoundError`:** Path to CSV is wrong or Drive is not mounted. Check mount ran and the file path (folder names, spaces, e.g. `IS 670`).
- **`NameError: name 'pd' is not defined`:** Import cell was not run or was run after the cell that uses `pd`. Run the import cell first.
- **`NameError: name 'pokemon' is not defined`:** The cell that does `read_csv` and assigns to `pokemon` was not run. Run cells in order.
- **Plot shows nothing or wrong variable:** Ensure column name is a string and exists in the DataFrame (e.g. `pokemon.columns` to list names). For histplot/countplot, use `data=df` and `x='ColumnName'`.
- **Colab “Disconnected” or session expired:** Rerun from the top (mount Drive, imports, then data load). Variables are lost when the runtime is restarted.

---

## 5. Lab Cheat Sheet

| Task | Code |
|------|------|
| Mount Drive (Colab) | `from google.colab import drive` then `drive.mount('/content/drive')` |
| Import | `import pandas as pd` and `import seaborn as sns` |
| Load CSV | `df = pd.read_csv('path/to/file.csv')` |
| Rows × cols | `df.shape` |
| First 5 rows | `df.head()` |
| One column | `df['ColName']` |
| Multiple columns | `df[['Col1','Col2']]` |
| Histogram (numeric) | `sns.histplot(x='Col', data=df)` then e.g. `.set_title("...")` |
| Count plot (categorical) | `sns.countplot(x='Col', data=df)` |

---

**Sources used:** IS670_lab01 (3).html — "IS 670 Lab 1: Introduction to Colab"; Part 1 Google Colab (cells, save, download); Part 2 Basic operators and data structures (Drive mount, pandas, seaborn, pokemon.csv, shape, head, column selection, histplot, countplot).
