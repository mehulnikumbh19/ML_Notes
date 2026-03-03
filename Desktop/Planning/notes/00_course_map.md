# IS 670 — Course Map & Exam 1 Roadmap

**Course:** Machine Learning for Business Analytics (IS 670)  
**Source note:** Syllabus and exam review were **not** in the provided materials. This map is built from your specified Exam 1 scope + content inferred from Labs 1–5 and Assignment 1 (Car). When you have the syllabus/exam review, add dates and exact Exam 1 scope here.

---

## 1. Course Roadmap (Inferred from Labs + Assignment)

| Week / Block | Topic | Lab | Lecture (inferred) |
|--------------|--------|-----|--------------------|
| 1 | Intro to Colab, Python, notebooks | Lab 1: Introduction to Colab | Lecture 1: Intro |
| 2 | Data understanding, exploration, visualization | Lab 2: Data Exploration | Lecture 2: Data Understanding |
| 3 | Decision trees (splits, entropy, max_depth) | Lab 3: Decision Tree | Lecture 3: Decision Trees & Metrics |
| 4 | Naive Bayes; compare with Decision Tree | Lab 4: Decision Tree vs Naive Bayes | Lecture 4: Naive Bayes |
| 5 | K-Nearest Neighbors (scaling, K) | Lab 5: K-Nearest Neighbor | Lecture 5: KNN |
| 6 | Overfitting, generalization, model choice | (Lab 6: not provided) | Lecture 6: Overfitting & Generalization |

---

## 2. Exam 1 Scope (Your Specified + Inferred)

- **Data:** Understanding/exploration, visualization, preprocessing (missing values, outliers, encoding).
- **Classification foundations:** Target variable, predictors, train vs test.
- **Metrics:** Confusion matrix; accuracy, precision, recall, F1; when to use which.
- **Decision trees:** Splits, entropy/impurity, pruning, max_depth, overfitting.
- **Naive Bayes:** Assumption, Bayes theorem, Laplace smoothing (if covered in your slides).
- **KNN:** Distance, scaling/normalization, choosing K, pros/cons.
- **Generalization vs overfitting:** Train vs test performance patterns; when to choose which model.

*Exact exam date and question formats: not specified in provided material.*

---

## 3. Prerequisite Tree ("Learn X Before Y")

```
Lecture 1 (Intro, Colab)
    → Lecture 2 (Data Understanding, Exploration)
        → Lecture 3 (Decision Trees, Metrics)
            → Lecture 4 (Naive Bayes) ——→ Compare DT vs NB
            → Lecture 5 (KNN) ————————→ Compare DT vs KNN; scaling
                    → Lecture 6 (Overfitting, Generalization)
```

- **Before Decision Trees:** Data loading, inspection, train/test split idea.
- **Before Naive Bayes / KNN:** Classification metrics (confusion matrix, precision, recall, F1).
- **Before Overfitting lecture:** Experience with max_depth (Labs 3–4, Assignment 1) and K (Lab 5).

---

## 4. Master Glossary (Course Wording)

Terms below are used in the provided labs and assignment. Add instructor definitions from lecture slides when you have them.

| Term | Brief (from labs/assignment) | Source |
|------|------------------------------|--------|
| **Target** | Variable we predict (e.g., Class, Legendary) | Lab 3–5, Assignment 1 |
| **Predictors / Features** | Variables used to predict the target | Lab 3–5 |
| **Train/test split** | Partition data for training vs evaluating; e.g. `test_size=0.3` | Lab 3–5, Assignment 1 |
| **Decision Tree** | Model that splits on features; `criterion='entropy'`, `max_depth` | Lab 3, 4, 5; Assignment 1 |
| **Entropy** | Impurity measure used for split criterion in trees | Lab 3, 4 (criterion=entropy) |
| **max_depth** | Maximum depth of tree; limits overfitting | Lab 3, 4, 5; Assignment 1 |
| **Naive Bayes** | Probabilistic classifier; "naive" = feature independence assumption | Lab 4 |
| **KNN (K-Nearest Neighbors)** | Classify by majority vote of K nearest points; needs scaling | Lab 5 |
| **Normalization / Scaling** | Scale features (e.g. 0–1) so distance-based methods (KNN) are fair | Lab 5 |
| **Confusion matrix** | Table: TN, FP, FN, TP | Assignment 1; classification_report |
| **Accuracy** | (TP+TN) / total | Assignment 1 |
| **Precision** | TP / (TP+FP) | Assignment 1 |
| **Recall** | TP / (TP+FN) | Assignment 1 |
| **F1** | Harmonic mean of precision and recall | Assignment 1 |
| **Overfitting** | Model fits training data too closely, poor on new data | Assignment 1, Lab 5 |
| **Generalization** | Model performs well on unseen (test) data | Lab 5 |
| **Good Buy / Kick** | Assignment 1: Class 0 = good buy, Class 1 = kick (bad buy) | Assignment 1 (Car) |
| **Imbalanced data** | One class much more frequent; accuracy can be misleading | Assignment 1 |

---

## 5. Provided vs Missing Materials

| Item | Status | Location / Note |
|------|--------|------------------|
| Syllabus | **Not in workspace** | Add Exam 1 date, scope, and policies when available |
| Lecture slides 1–6 | **Not in workspace** | Add slide/page refs in SOURCES_INDEX as you get them |
| Exam review | **Not in workspace** | Add "Top exam questions" to Exam guide when available |
| Lab 1–5 (HTML) | Available | `IS670_lab01 (3).html` … `IS670_lab05 (1).html` |
| Lab 6 | **Not in workspace** | Placeholder in labs folder |
| Assignment 1 (Car) | Available | `NikumbhMehul.html` (Assignment1_Car) |

---

## 6. Next Steps After Phase A

1. **Phase B:** Build lecture notes `01_lecture1_intro.md` … `06_lecture6_overfitting_generalization.md` and lab walkthroughs `01_lab1_walkthrough.md` … `06_lab6_placeholder.md` (week-by-week).
2. **Phase C:** Assignment 1 walkthrough; placeholders for other HWs if any.
3. **Phase D:** Exam 1 master study guide, Python templates, code drills.

When you add syllabus or exam review, update: Exam 1 date/scope (Section 2), glossary (Section 4), and SOURCES_INDEX.md.

---
**Sources used:** Inferred from IS670 Lab 1–5 HTML titles/sections; Assignment 1 (NikumbhMehul.html). Syllabus and exam review not in provided material.
