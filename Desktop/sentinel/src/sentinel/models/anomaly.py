"""IsolationForest scoring for per-user feature rows (Phase 4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from sentinel.features.user_behavior import FEATURE_COLUMN_NAMES

ID_COLUMN = "user_id"
SCORE_COLUMN = "anomaly_score"
FLAG_COLUMN = "is_anomaly"
EXPLAIN_COLUMN = "anomaly_explanation"

SCORE_OUTPUT_COLUMNS = [ID_COLUMN, SCORE_COLUMN, FLAG_COLUMN, EXPLAIN_COLUMN]


@dataclass
class ScoreRunResult:
    """In-memory artifacts for the current Streamlit run (no disk persistence)."""

    scaler: StandardScaler | None
    model: IsolationForest | None
    feature_columns: list[str]


def _empty_scored_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=SCORE_OUTPUT_COLUMNS)


def validate_features_for_scoring(df: pd.DataFrame | None) -> list[str]:
    """Return human-readable errors, or an empty list if the frame can be scored (or is empty)."""
    if df is None:
        return ["Feature table is missing."]
    if df.empty:
        return []
    if ID_COLUMN not in df.columns:
        return [f"Missing required column `{ID_COLUMN}`."]
    numeric = [c for c in FEATURE_COLUMN_NAMES if c in df.columns]
    if not numeric:
        return ["No known numeric feature columns found (expected Phase 3 feature names)."]
    return []


def _explain_row(
    row_numeric: pd.Series,
    population: pd.DataFrame,
    cols: list[str],
    top_k: int = 3,
) -> str:
    """Short text: which features deviate most from the population (z-score)."""
    parts: list[tuple[str, float, float]] = []
    for c in cols:
        col = population[c].astype(float)
        mu = float(col.mean())
        sigma = float(col.std(ddof=0))
        if not np.isfinite(sigma) or sigma == 0.0:
            sigma = 1.0
        v = float(row_numeric[c])
        z = (v - mu) / sigma
        parts.append((c, abs(z), z))
    parts.sort(key=lambda x: -x[1])
    top = parts[:top_k]
    if not top:
        return "No feature deviations computed."
    return "; ".join(f"{c} (z={z:+.2f})" for c, _, z in top)


def score_user_feature_table(
    features: pd.DataFrame | None,
    *,
    random_state: int = 42,
) -> tuple[pd.DataFrame, list[str], dict[str, Any]]:
    """Train IsolationForest on numeric user features and attach scores + simple explanations.

    Returns:
        (scored_table, errors, info). ``info`` may include ``run`` (ScoreRunResult) or skip reasons.
    """
    errors = validate_features_for_scoring(features)
    if errors:
        return _empty_scored_frame(), errors, {}

    if features.empty:
        return _empty_scored_frame(), [], {"skipped_model": True, "reason": "empty_features"}

    numeric_cols = [c for c in FEATURE_COLUMN_NAMES if c in features.columns]
    X = features[numeric_cols].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    n = len(features)

    base = features[[ID_COLUMN]].copy()

    if n < 2:
        base[SCORE_COLUMN] = 0.0
        base[FLAG_COLUMN] = pd.Series([False] * n, dtype=bool, index=base.index)
        base[EXPLAIN_COLUMN] = (
            "Not enough users (need at least 2) to train IsolationForest; scores are neutral."
        )
        return base, [], {"skipped_model": True, "reason": "n_users_lt_2"}

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    n_estimators = min(200, max(50, 25 * int(np.sqrt(n))))
    max_samples = min(256, n)

    model = IsolationForest(
        n_estimators=n_estimators,
        max_samples=max_samples,
        contamination="auto",
        random_state=random_state,
        n_jobs=-1,
    )
    model.fit(Xs)

    pred = model.predict(Xs)
    # sklearn: lower decision_function => more abnormal; we expose higher => more suspicious
    raw = -model.decision_function(Xs).astype(float)

    base[SCORE_COLUMN] = raw
    base[FLAG_COLUMN] = (pred == -1).astype(bool)

    explanations: list[str] = []
    for i in range(n):
        explanations.append(_explain_row(X.iloc[i], X, numeric_cols, top_k=3))
    base[EXPLAIN_COLUMN] = explanations

    run = ScoreRunResult(scaler=scaler, model=model, feature_columns=list(numeric_cols))
    return base, [], {"run": run, "feature_columns": numeric_cols}
