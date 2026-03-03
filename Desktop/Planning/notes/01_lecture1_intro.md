# Lecture 1: Introduction (IS 670)

**Big picture:** Machine learning for business analytics uses data to build models that support decisions (e.g., predict which cars are “bad buys,” which customers churn). This course starts with the environment (Colab), basic Python, and loading/inspecting data—the foundation for everything that follows.

---

## 1. Big Picture (Business Analytics Framing)

- **ML for business analytics:** Use data + algorithms to predict or classify outcomes (e.g., good buy vs kick, loyal vs churn) so the business can act.
- **Why start with Colab and data?** You need a place to run code (Colab) and data in a structured form (tables) before you can train or evaluate any model.
- **Lecture 1 scope:** Get comfortable with the notebook environment, run Python, load a dataset, and do minimal inspection (shape, head, columns, simple plots). Formal ML concepts (target, train/test, metrics) come in later lectures.

---

## 2. Concepts from Scratch

### 2.1 Notebooks (Colab)

- A **notebook** is an executable document: **cells** of text (Markdown) and code (Python) that you run in order.
- **Google Colab** runs notebooks in the browser and provides a cloud runtime so you don’t need to install Python locally.
- Notebooks are stored in Google Drive; you can download them as `.ipynb` files.

### 2.2 Data as tables

- Data is often in **tabular** form: **rows** = records (e.g., one Pokemon, one car), **columns** = variables (e.g., Attack, Type1, Class).
- In Python we use **pandas** to hold such data in a **DataFrame**: a 2D structure with column names and row indices.

### 2.3 First steps in a typical workflow

1. **Load** data (e.g., from a CSV file).
2. **Inspect** it: how many rows/columns? What do the first rows look like? What are the column names and types?
3. **Visualize** (later in more depth): e.g., distribution of a numeric variable (histogram), counts of a categorical variable (count plot).

---

## 3. Definitions (Exact + Beginner-Friendly)

| Term | Definition |
|------|------------|
| **Notebook** | Document made of cells (text + code) that can be run in order. |
| **Cell** | One unit of a notebook: either **text** (Markdown) or **code** (e.g., Python). |
| **DataFrame** | Pandas object: table with rows and columns, column names, and often a numeric index. |
| **CSV** | Comma-separated values: a text file where each line is a row and columns are separated by commas. |
| **Variable** | In Python, a name that holds a value (e.g., `pokemon` holds a DataFrame). |

---

## 4. Key Formulas

*None for Lecture 1; formulas start with metrics and decision trees in later lectures.*

---

## 5. Worked Example (Mirror Lab 1 Style)

**Goal:** Load the Pokemon dataset, check its size, show the first rows, and plot the distribution of `Attack`.

1. **Mount Drive and import libraries (in Colab):**
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   import pandas as pd
   import seaborn as sns
   ```

2. **Read the CSV into a DataFrame:**
   ```python
   pokemon = pd.read_csv('/content/drive/MyDrive/IS 670/pokemon.csv')
   ```

3. **Inspect:**
   - `pokemon.shape` → (800, 12): 800 rows, 12 columns.
   - `pokemon.head()` → first 5 rows.
   - Single column: `pokemon['Attack']`; multiple columns: `pokemon[['Attack', 'Defense']]`.

4. **Simple visualization:**
   - **Histogram** (numeric variable): `sns.histplot(x='Attack', data=pokemon)` then e.g. `snsplot.set_title("Histogram of Attack in the pokemon data set")`.
   - **Count plot** (categorical): `sns.countplot(x='Legendary', data=pokemon)`.

---

## 6. Common Mistakes / Misconceptions

- **Running cells out of order:** If you skip the cell that defines `pokemon`, a later cell that uses `pokemon` will fail. Run cells top to bottom (or ensure dependencies were run).
- **Wrong path for CSV:** In Colab, the path depends on where you mounted Drive and where the file is (e.g. `MyDrive/IS 670/pokemon.csv`). Wrong path → `FileNotFoundError`.
- **Confusing one vs multiple columns:** `df['Attack']` is one column (Series); `df[['Attack','Defense']]` is two columns (DataFrame). Double brackets for a list of column names.

---

## 7. Mini-Check Quiz (5–10 Qs) + Answers

1. What are the two main types of cells in a Colab notebook?  
   **Answer:** Text (Markdown) and code (e.g., Python).

2. What does `pokemon.shape` return?  
   **Answer:** A tuple (number of rows, number of columns), e.g. (800, 12).

3. How do you get a single column from a DataFrame? How do you get multiple columns?  
   **Answer:** Single: `df['ColName']`. Multiple: `df[['Col1','Col2']]`.

4. Which seaborn function is used for a histogram of a numeric variable? For counts of a categorical variable?  
   **Answer:** `sns.histplot(...)` for numeric; `sns.countplot(...)` for categorical.

5. What is a DataFrame?  
   **Answer:** A pandas table: rows and columns with column names and (usually) a row index.

6. Why do we use `drive.mount()` in Colab when the data is in Google Drive?  
   **Answer:** So the Colab runtime can access files in your Drive; the path `/content/drive` then points to your Drive.

---

## 8. TL;DR Cheat Sheet

- **Colab:** Notebook = cells (text + code); run in order; save (File → Save / Cmd+Ctrl+S); download as .ipynb.
- **Data:** Load with `pd.read_csv(path)`; result is a DataFrame.
- **Inspect:** `df.shape`, `df.head()`, `df['col']`, `df[['c1','c2']]`.
- **Plot:** `sns.histplot(x='col', data=df)` for numeric; `sns.countplot(x='col', data=df)` for categorical; add titles with `.set_title()`.

---

**Sources used:** Lab 1 (IS670_lab01 HTML) — Part 1 Google Colab, Part 2 Basic operators and data structures; course map. Lecture slides not in provided material; add slide refs when available.
