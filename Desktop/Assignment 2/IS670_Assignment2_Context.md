# IS670 Assignment 2 Context - Voting Behavior Analytics Report

## 1. Project Overview
This project predicts county-level voting behavior on gaming-related ballot measures utilizing a structured CRISP-DM methodology. A fully executable, production-ready Google Colab notebook (`IS670_Assignment2_Voting_Behavior_Final.ipynb`) provides a comprehensive data parsing layer mapping demographic factors into a verified comparative modeling suite deploying Decision Tree, K-Nearest Neighbors (KNN), and Gaussian Naive Bayes classification logic. The overarching goal is to determine the statistical viability of a county supporting a gaming measure prior to an election taking place, while neutralizing inherently leaking data indicators.

## 2. Objective and Target Variable
- **Main Objective**: Develop a predictive model to classify whether a specific county will vote in favor or against a gaming-related ballot measure, mapping the operational risk footprint for hospitality, local governance, and gaming industries.
- **Target Variable**: `DEPENDENT VARIABLE`.
- **Target Variable Type**: Binary Nominal (1 = Yes/For passing the measure, 0 = No/Against passing the measure).

## 3. File Inventory and Exact File Paths
- Dataset Source: `c:\Users\mniku\Desktop\Assignment 2\Gaming Ballot Data Set-1.xls`
- Data Dictionary PDF: `c:\Users\mniku\Desktop\Assignment 2\Gaming Ballot Data Description.pdf`
- Original Assignment Requirements: `c:\Users\mniku\Desktop\Assignment 2\IS670-Assignment2-2.pdf`
- Generated Python Build Script: `c:\Users\mniku\Desktop\Assignment 2\build_detailed_nb.py`
- Final Executed Notebook Deliverable: `c:\Users\mniku\Desktop\Assignment 2\IS670_Assignment2_Voting_Behavior_Final.ipynb`
- Primary Context Sync File: `c:\Users\mniku\Desktop\Assignment 2\IS670_Assignment2_Context.md`

## 4. Dataset Schema / Column List
Original dataset contained 1287 records spanning 31 distinct columns encompassing identical variable forms (int64/float64 numerical types). 

**Variables include**: `State No`, `County No`, `FOR`, `AGAINST`, `TOTAL CASTE`, `DEPENDENT VARIABLE`, `BALLOT TYPE`, `POPULATION`, `PCI`, `MEDIUM FAMILY INCOME`, `SIZE OF COUNTY`, `POPULATION DENSITY`, `PERCENT WHITE`, `PERCENT BLACK`, `PERCENT OTHER`, `PERCENT MALE`, `PERCENT FEMALE`, `NO OF CHURCHES`, `NO OF CHURCH MEMBERS`, `PERCENT CHURCH MEMBERS OF POPULATION`, `POVERTY LEVEL`, `UNEMPLOYMENT RATE`, `AGE LESS THAN 18`, `AGE24`, `AGE44`, `AGE64`, `AGE OLDER THAN 65`, `MSA`, `PERCENT MINORITY`, `NO OF OLDER`, `NO OF YOUNGER`.

## 5. Data Quality Issues Found
- 1 single missing value isolated in `NO OF CHURCH MEMBERS`.
- 1 single missing value isolated in `PERCENT CHURCH MEMBERS OF POPULATION`.
  - *Resolution*: Imputed dynamically using robust column Medians protecting outlier shifts.
- **Data Integrity Validation**: No `#NULL!` malformed string placeholders existed inside the .xls file reading layer.
- **Imbalance**: The `DEPENDENT VARIABLE` overwhelmingly targets '1' (approximately 1140 approvals vs 147 rejections).
  - *Resolution*: Handled structurally deploying `stratify=y` splits alongside metric tracking prioritizing F1/Recall AUC instead of pure Accuracy manipulation, alongside automated `class_weight='balanced'` injection in the primary Decision Tree loop.

## 6. Variable-Type Decisions
- **Useless Identifiers**: `State No`, `County No` (Hold no statistical predictive generalization value outside their row ID bounds; actively harmful to tree splits).
- **Binary/Categorical Factors**: `DEPENDENT VARIABLE` (Target), `BALLOT TYPE` (Gambling=1, Wagering=2), `MSA` (Metropolitan).
- **Standardized Continuous Variants**: `POPULATION`, `PCI`, `POVERTY LEVEL`, `UNEMPLOYMENT RATE`, `NO OF CHURCHES` etc.
- **Compositional Percentages**: `PERCENT WHITE`, `PERCENT BLACK`, `PERCENT OTHER`, `PERCENT MALE`.
- **Absolute Counts**: Age distribution headers (`AGE LESS THAN 18`, etc.) function uniquely as absolute structural counts, *not* bounded percentages. Explored fundamentally in the EDA plots.

## 7. Cheating / Leakage Variables Identified and Decisions Made
- **Identified Candidates**: `FOR`, `AGAINST`, `TOTAL CASTE`.
- **Mathematical Evaluation & Decision**: A programmatic verification identified that `FOR` + `AGAINST` inherently equated sequentially to `TOTAL CASTE`, and that the `DEPENDENT VARIABLE` is a deterministic derivative tracking if `FOR` > `AGAINST`. 
- **Action Taken**: Retaining these columns guarantees perfect artificial leakage accuracy simulating the future. Consequently, `FOR`, `AGAINST`, and `TOTAL CASTE` were forcibly dropped before modeling commenced to simulate real-world prediction mechanics.

## 8. Redundant / Derived Variables Identified and Decisions Made
Redundant variables mathematically overlap generating extreme variance instability (multicollinearity).
- **Verified Exclusions**:
  - `PERCENT MINORITY` (Equal cleanly to `PERCENT BLACK` + `PERCENT OTHER`). **Dropped**.
  - `PERCENT FEMALE` (Forms perfect inverse linear dependency 1.0 logic with `PERCENT MALE`). **Dropped**.
  - Internal Age Counts: `AGE64`, `AGE OLDER THAN 65`, `AGE LESS THAN 18`, `AGE24`, `AGE44`. The overarching combinations specifically mapped by `NO OF OLDER` and `NO OF YOUNGER` structurally define the necessary polar vectors. Underlying subsets were **Dropped**.

## 9. Final Selected Feature Set
The strictly vetted target modeling dataset included explicit demographics stripped of any exact mathematical redundancy dependencies or leakage points. Dummy variables replaced the `BALLOT TYPE`, identifying "Wagering status", alongside directly non-linear features preserving unique context (e.g. `POPULATION`, `PERCENT BLACK`, `PERCENT MALE`, `NO OF CHURCH MEMBERS`, `POVERTY LEVEL`, engineered iterations). 

## 10. Engineered Features Created and Rationale
1. **`Economic_Distress_Index`**: Multiplication mapped logic `POVERTY LEVEL` * `UNEMPLOYMENT RATE`. 
   - *Rationale*: Individual variables isolate factors. The combination produces a compounding distress tracker that identifies severely suppressed local economies that may drastically vote to approve gambling for stimulus funding.
2. **`Churches_Per_1000`**: Relative metric `(NO OF CHURCHES / POPULATION) * 1000`. 
   - *Rationale*: Analyzing bulk church numbers blindly follows population size (e.g. large cities possess more churches simply due to physical mass). This engineered density factor determines true moral structuring separate from population curves.

## 11. Preprocessing Steps Completed
- Dropped all confirmed leakage components (`FOR`, `AGAINST`, `TOTAL CASTE`, `State`, `County`).
- Computed math vectors tracking exact matching compositions allowing removal of redundancies.
- Resolved Null constraints via robust Median extraction tracking.
- Performed Pandas `get_dummies` categorical transformation converting `BALLOT TYPE` variables to numerical Boolean variants matching Machine Learning intake syntax.
- Constructed standard Train/Test stratifying the imbalanced 80/20 Target distribution mapping.
- Engaged `StandardScaler` ensuring KNN multidimensional algorithms tracked localized distances efficiently avoiding continuous outlier biases.

## 12. Visualizations Completed and Their Main Findings
The executed `.ipynb` provides **13** extensive exploratory data analysis representations combining overlapping Seaborn styling frameworks targeting contextual variable subsets:
- **Countplots** confirmed Target imbalance against Ballot structural types. Voting 'Against' scales noticeably higher for 'Wagering' over standard 'Gambling'.
- Multiple **Violin and Boxplots** mapped continuous constraints, clearly depicting poverty, lower Median Incomes, and higher Unemployment mapping distinctly toward passing Gaming measures. 
- Integrated **Distribution KDE plots** for Age boundaries mapped count overlaps dynamically.
- Transformed Church totals into **Log-scale distributions**, directly identifying that "No" rejections mathematically align with severe upward bounds of religious percent adherence populations.
- An extensive **Correlation Matrix Heatmap** identified inverse correlation factors explicitly mapping Urbanization (Density) toward affirmative (`1`), and `% WHITE` toward rejection bounds (`0`).

## 13. Modeling Experiments Completed
Algorithm selection explicitly addressed the rubric comparisons matching classification variance behavior across:
1. **Decision Tree Classifier** (Class weights explicitly mapped tracking imbalanced splits).
2. **K-Nearest Neighbors Classifier** (Distance logic operating aggressively on the scaled subset arrays).
3. **Gaussian Naive Bayes** (Predicting standard normal overlaps analyzing independence arrays).

## 14. Best Hyperparameters Found So Far
Configured and executed entirely inside local computation leveraging internal 5-Fold `GridSearchCV` scoring exclusively on `roc_auc` arrays to avoid imbalanced skew.
- **DT**: Parameter optimization spanning deep layer foliage limits (`max_depth`: [3,4,5,7,None]) tracking 'gini' vs 'entropy' structural constraints. 
- **KNN**: Probed uniquely odd neighbors bounds (`n_neighbors`: [3,5...21]) determining optimal localized generalization curves preventing training memorization gaps.
- **NB**: Tuned `var_smoothing` iteratively across `np.logspace` configurations adapting the variance width to handle zero-probability structures organically.
- *Explicitly exact returned parameter iterations print independently inside the notebook execution blocks per algorithm.*

## 15. Best Metrics Found So Far
All metrics seamlessly evaluate output tracking on True Holdout subsets utilizing explicitly programmed custom `evaluate_model` functions. Outputs detail internal Confusion Matrices alongside master Comparison tables scaling exact Accuracy, Precision, Recall, and combined harmonic F1-score tracking. The `DecisionTreeClassifier` maintains supremacy explicitly through balanced execution mapping highest interpretable Recall coverage paired directly with peak AUC behavior plotting mapped mathematically on the inline comparative ROC Curve.

## 16. Variable Importance Findings
- Variable sensitivities rigorously extracted deploying advanced `Leave-One-Feature-Out` (LOFO) architecture scoring routines algorithmically. The script iterates through valid training features inherently dropping singular features off, rerunning Grid configurations, and charting the resulting AUC degradation difference.
- **Business Translation output**: Core population structures alongside the newly engineered `Economic_Distress_Index` significantly penalize AUC margins when removed. `BALLOT TYPE` proves undeniably predictive tracking localized intent variance. The explicit feature degradation chart is generated sorting impact dynamically inside the Evaluation notebook block.

## 17. Remaining Tasks / Next Steps
- The primary assignment deliverables (Colab fully-executed `IS670...ipynb` modeling structure + this robust Markdown Context Document) have reached final status natively completing all rubric assignments systematically. 
- No further major action sequences require computational processing. 

## 18. Assumptions and Limitations
- The models utilize standard imputation strategies; should null distributions drastically shift across new subsets, advanced predictive clustering (KNN Imputer layers) may become necessary. 
- General execution processes utilized standardized hardware dependencies mapping Scikit-learn architectures preventing external uninterpretable constraints (e.g., deep learning arrays) optimizing purely for interpretability bounds matching executive analytics logic structures.

## 19. Reproducibility Details
- Base Control Randomizations locked natively via variable constant sets initializing `random_state = 42` consistently. 
- The Notebook logic translates cross-platform safely tracking standard native `pandas`/`numpy`/`seaborn`/`scikit-learn` libraries handling internal display parameters dynamically inside Colab runtimes.
- Final output filepath explicitly bound matching: `c:\Users\mniku\Desktop\Assignment 2\IS670_Assignment2_Voting_Behavior_Final.ipynb`

## 20. Handoff Instructions for the Next Chat
The analytical iteration processing demographic ballot predictions mapping explicit dataset requirements fulfills its lifecycle. If resuming subsequent iterations checking hyperparameter sensitivities or injecting new test variables organically gathered out of band, read this document, then execute specific block subsets matching the standalone `build_detailed_nb.py` script to generate notebook alterations swiftly.

---

## Running Change Log
- **[System Time]**: Created initial Context file scaffolding.
- **[System Time]**: Completed partial script for notebook generation mapped around initial CRISP-DM criteria.
- **[System Time]**: Notebook originally successfully full-generated via `nbformat`. Code modifications requested appending internal Colab-specific HTML generation exports via `jupyter nbconvert` commands handling isolated namespace tracking.
- **[System Time]**: Converted Python build parameters creating a standalone expanded generator (`build_detailed_nb.py`). Expanding text sequences, adding statistical plots totaling 13 variations, strictly expanding variable discussions mapping categorical decisions logically natively against scoring rubric grids. Entire notebook generated, flawlessly executed via inplace pipelines rendering variables mapping, and updated this Context file into exhaustive coverage bounds summarizing technical outputs directly translating into business actions.


### Notebook V3 Updates
- Explicitly graphed Decision Tree max_depth arrays comparing Train vs Test accuracy curves to identify Overfitting/Underfitting bounds directly.
- Explicitly extracted eature_importances_ from the top-tuned DT confirming religious metrics drove prime variance matrices.
- Configured KNN evaluations executing K bounds from 1 to 31 plotting structural Euclidean variance degradation explicitly.
- Generated explicit documentation verifying Naive Bayes ar_smoothing parameters satisfying hyperparameter improvement requirements definitively.
