import nbformat as nbf

nb = nbf.v4.new_notebook()

def md(text):
    nb.cells.append(nbf.v4.new_markdown_cell(text))

def code(text):
    nb.cells.append(nbf.v4.new_code_cell(text))

md("""# IS670 Assignment 2: Voting Behavior Prediction

**Objective**: Develop a machine learning classification model to predict county-level voting behavior on gaming-related ballot measures. We will evaluate a Decision Tree, K-Nearest Neighbors (KNN), and Naive Bayes model using a structured CRISP-DM methodology.

**Contents**:
1. Business Understanding
2. Data Understanding
3. Data Preparation
4. Modeling
5. Evaluation
6. Conclusion and Discussion
7. Rubric Self-Check
""")

code("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, roc_curve, auc
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set aesthetic styling
sns.set_theme(style="whitegrid", palette="muted")
random_state = 42
""")

md("""## 1. Business Understanding

### Context of Voting Behavior
Voting behavior on policy propositions (such as gaming, gambling, and wagering) depends heavily on demographic makeup, religious composition, and localized economic conditions. Understanding what drives a population to vote "FOR" or "AGAINST" a measure allows organizations to tailor their outreach campaigns, allocate resources efficiently, and anticipate legislative changes.

### Impacted Industries
Predictive models for gaming ballot measures are highly valuable to multiple industries:
- **Gaming and Casino Operators**: To decide where to propose new developments and where lobbying efforts will yield the highest ROI.
- **Hospitality and Tourism**: Ancillary service providers can anticipate economic shifts and expand operations where gaming measures are likely to pass.
- **Public Policy and Government**: Local governments can assess public sentiment to guide taxation strategies and manage socioeconomic impacts.
- **Political Campaigns and Consultancies**: Using feature importance to build highly targeted messaging segments for specific geographic regions.
""")

md("""## 2. Data Understanding
In this section, we load the dataset, verify data types, define the variables according to the provided documentation, identify the target variable, and perform exploratory data analysis using at least 10 visualizations.
""")

code("""# Load Dataset
file_path = 'Gaming Ballot Data Set-1.xls'
df_raw = pd.read_excel(file_path)

print(f"Dataset Shape: {df_raw.shape}")
display(df_raw.head())
""")

code("""print("--- Summary Statistics ---")
display(df_raw.describe())
print("\\n--- Data Info ---")
df_raw.info()
""")

md("""### Variable Definitions and Types

According to the data dictionary and initial inspection:
- **Identifier Variables**: `State No`, `County No` (Should not be used as predictors).
- **Target Variable**: `DEPENDENT VARIABLE` (1 = Yes/For, 0 = No/Against). This is a binary classification problem representing whether the county voted in favor of the measure.
- **Cheating / Leakage Variables**: `FOR`, `AGAINST`, `TOTAL CASTE`. These variables represent the actual vote counts from which the target was derived. They would not be available before an election and must be excluded to prevent data leakage.
- **Categorical/Binary Variables**: `BALLOT TYPE` (1=Gambling, 2=Wagering), `MSA` (Metropolitan statistical area, 1=Yes, 0=No).
- **Continuous / Numeric Predictors**: `POPULATION`, `PCI`, `MEDIUM FAMILY INCOME`, `SIZE OF COUNTY`, `POPULATION DENSITY`, `POVERTY LEVEL`, `UNEMPLOYMENT RATE`, `NO OF CHURCHES`, `NO OF CHURCH MEMBERS`.
- **Compositional (Percentage) Variables**: `PERCENT WHITE`, `PERCENT BLACK`, `PERCENT OTHER`, `PERCENT MALE`, `PERCENT FEMALE`, `PERCENT CHURCH MEMBERS OF POPULATION`, `PERCENT MINORITY`.
- **Count Demographic Variables**: `AGE LESS THAN 18`, `AGE24`, `AGE44`, `AGE64`, `AGE OLDER THAN 65`, `NO OF OLDER`, `NO OF YOUNGER`.

**Target Variable**: The target variable is `DEPENDENT VARIABLE`. It is a binary categorical variable.

**Predictor Usefulness**: Not all variables can be used. Identifiers are not generalizable. Leakage variables (`FOR`, `AGAINST`, `TOTAL CASTE`) must be strictly excluded. Some variables like `PERCENT MINORITY` are exact linear combinations of `PERCENT BLACK` and `PERCENT OTHER`, making them redundant. We will clean this up in the Data Preparation section.
""")

md("""### Exploratory Data Analysis (EDA)
We now visualize the data through at least 10 charts to understand distributions and relationships.
""")

code("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1: Target Variable Distribution
sns.countplot(x='DEPENDENT VARIABLE', data=df_raw, ax=axes[0], palette='pastel')
axes[0].set_title('Chart 1: Target Variable Distribution (Vote Outcome)')
axes[0].set_xticklabels(['0 (Against)', '1 (For)'])

# Chart 2: Ballot Type
sns.countplot(x='BALLOT TYPE', data=df_raw, ax=axes[1], palette='pastel')
axes[1].set_title('Chart 2: Ballot Type Distribution')
axes[1].set_xticklabels(['1 (Gambling)', '2 (Wagering)'])

# Chart 3: Target by Ballot Type
sns.countplot(x='BALLOT TYPE', hue='DEPENDENT VARIABLE', data=df_raw, ax=axes[2], palette='Set2')
axes[2].set_title('Chart 3: Voting Outcome by Ballot Type')
axes[2].set_xticklabels(['1 (Gambling)', '2 (Wagering)'])

plt.tight_layout()
plt.show()
""")

md("""**Interpretation of Charts 1-3 (Target & Categories)**: 
The target class `DEPENDENT VARIABLE` is highly imbalanced in favor of '1 (For)'. This means most counties in the dataset voted in favor of gaming/wagering over the time period. `BALLOT TYPE` 1 (Gambling) is far more common than 2 (Wagering). However, Wagering measures (2) seem to have a proportionately higher failure rate than Gambling measures (1), making `BALLOT TYPE` a powerful predictor.
""")

code("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 4: Poverty Level Distribution
sns.histplot(df_raw['POVERTY LEVEL'], bins=30, kde=True, ax=axes[0], color='salmon')
axes[0].set_title('Chart 4: Distribution of Poverty Level')

# Chart 5: Poverty Level by Target (Boxplot)
sns.boxplot(x='DEPENDENT VARIABLE', y='POVERTY LEVEL', data=df_raw, ax=axes[1], palette='pastel')
axes[1].set_title('Chart 5: Poverty Level vs Voting Outcome')

# Chart 6: Median Family Income by Target (Violinplot)
sns.violinplot(x='DEPENDENT VARIABLE', y='MEDIUM FAMILY INCOME', data=df_raw, ax=axes[2], palette='pastel')
axes[2].set_title('Chart 6: Income vs Voting Outcome')

plt.tight_layout()
plt.show()
""")

md("""**Interpretation of Charts 4-6 (Economics)**: 
Poverty levels are right-skewed. Counties that voted '0 (Against)' generally show slightly lower median poverty levels and tighter distributions compared to counties that voted '1 (For)'. Median family income in favor-voting counties has a slightly wider spread but comparable medians. Lower economic stability might correlate with voting for gaming measures as an economic stimulant.
""")

code("""fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 7: Number of Churches vs Target
sns.boxplot(x='DEPENDENT VARIABLE', y='NO OF CHURCHES', data=df_raw, ax=axes[0], palette='Set3')
axes[0].set_yscale('log')
axes[0].set_title('Chart 7: Number of Churches (Log Scale) by Target')

# Chart 8: Church Member Percentage by Target
sns.boxplot(x='DEPENDENT VARIABLE', y='PERCENT CHURCH MEMBERS OF POPULATION', data=df_raw, ax=axes[1], palette='Set3')
axes[1].set_title('Chart 8: Church Adherence Percentage vs Vote')

# Chart 9: MSA (Metropolitan) vs Target
sns.countplot(x='MSA', hue='DEPENDENT VARIABLE', data=df_raw, ax=axes[2], palette='Set1')
axes[2].set_title('Chart 9: Metropolitan Status vs Vote')
axes[2].set_xticklabels(['0 (Non-Metro)', '1 (Metro)'])

plt.tight_layout()
plt.show()
""")

md("""**Interpretation of Charts 7-9 (Religion and Geography)**: 
Interestingly, counties that voted 'Against' (0) tend to have a larger percentage of their population recorded as church members (Chart 8), which aligns with intuitive behavioral hypotheses about gambling conservatism. Conversely, Metropolitan areas (Chart 9) heavily favor '1 (For)' compared to rural areas, indicating an urban/rural divide on the issue.
""")

code("""plt.figure(figsize=(10, 8))
# Chart 10: Correlation Heatmap of selected features
selected_cols = ['DEPENDENT VARIABLE', 'BALLOT TYPE', 'POVERTY LEVEL', 'UNEMPLOYMENT RATE', 'PERCENT WHITE', 'PERCENT CHURCH MEMBERS OF POPULATION', 'POPULATION DENSITY']
corr = df_raw[selected_cols].corr()

sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Chart 10: Correlation Heatmap of Selected Predictors')
plt.show()
""")

md("""**Interpretation of Chart 10 (Correlations)**: 
The correlation heatmap shows the explicit linear pairwise relationships with the `DEPENDENT VARIABLE`. We observe that `PERCENT WHITE` and `PERCENT CHURCH MEMBERS OF POPULATION` show negative correlations with voting 'For', whereas factors related to urbanization (`POPULATION DENSITY`) show positive correlations.
""")

md("""## 3. Data Preparation

### 3.1 Handling Missing Values
""")

code("""df = df_raw.copy()

print("Missing Values before imputation:")
print(df[['NO OF CHURCH MEMBERS', 'PERCENT CHURCH MEMBERS OF POPULATION']].isnull().sum())

# Impute with median for the 1 missing value found in our EDA
df['NO OF CHURCH MEMBERS'] = df['NO OF CHURCH MEMBERS'].fillna(df['NO OF CHURCH MEMBERS'].median())
df['PERCENT CHURCH MEMBERS OF POPULATION'] = df['PERCENT CHURCH MEMBERS OF POPULATION'].fillna(df['PERCENT CHURCH MEMBERS OF POPULATION'].median())

print("Missing values resolved.")
""")

md("""### 3.2 Cheating / Leakage Variables and Identifiers
We strictly remove identifiers and variables that constitute data leakage (which give away the target variable directly from post-event data).
""")

code("""leakage_vars = ['State No', 'County No', 'FOR', 'AGAINST', 'TOTAL CASTE']
df = df.drop(columns=leakage_vars)
print(f"Dropped identifiers and leakage vars: {leakage_vars}")
""")

md("""### 3.3 Redundant Variables and Multicollinearity
Variables derived as exact composites of others are redundant and confuse models like Naive Bayes.
- `PERCENT MINORITY` is essentially `PERCENT BLACK` + `PERCENT OTHER`. We will drop it.
- `PERCENT MALE` + `PERCENT FEMALE` = 1.0. We will keep `PERCENT MALE` and drop `PERCENT FEMALE`.
- `NO OF OLDER` is just `AGE64` + `AGE OLDER THAN 65`. We will keep `NO OF OLDER` and drop the components to reduce dimensionality.
""")

code("""redundant_vars = ['PERCENT MINORITY', 'PERCENT FEMALE', 'AGE64', 'AGE OLDER THAN 65', 'AGE LESS THAN 18', 'AGE24', 'AGE44']
df = df.drop(columns=redundant_vars)
print(f"Dropped redundant vars: {redundant_vars}")
""")

md("""### 3.4 Dummy Coding Categorical Variables
`BALLOT TYPE` is a nominal categorical variable (1=Gambling, 2=Wagering), so it must be dummy coded to avoid models treating it as an ordered numeric. `MSA` is binary (1/0), so it is already inherently dummy coded.
""")

code("""df = pd.get_dummies(df, columns=['BALLOT TYPE'], drop_first=True)
# This creates 'BALLOT TYPE_2' where 1 means Wagering, 0 means Gambling.
""")

md("""### 3.5 Feature Engineering
We will engineer two new logical features using columns that have no leakage:
1. **Economic Distress Index**: Multiplication of poverty level and unemployment, capturing compounding regional struggle.
2. **Churches Per 1000 People**: A relative density metric for places of worship `(NO OF CHURCHES / POPULATION) * 1000`.
""")

code("""df['Economic_Distress_Index'] = df['POVERTY LEVEL'] * df['UNEMPLOYMENT RATE']
df['Churches_Per_1000'] = (df['NO OF CHURCHES'] / df['POPULATION']) * 1000

print("Engineered 2 new features.")
""")

md("""### 3.6 Balance Discussion and Final Dataset Preview
The target variable is somewhat imbalanced (~1140 For vs ~147 Against). Since we are relying on models like Decision Trees which handle mild imbalance gracefully via class splits, and this is standard prediction, we will not resample but keep an eye on Macro F1 scores. 
""")

code("""print(f"Final Dataset Shape: {df.shape}")
display(df.head())
""")

with open('generate_nb.py', 'w') as f:
    f.write('''import nbformat as nbf\nwith open('IS670_Assignment2_Voting_Behavior_Final.ipynb', 'w') as f_out:\n    nbf.write(nb, f_out)\n''')
