"""Deterministic risk prioritization from scored users + optional feature context (Phase 5)."""

from __future__ import annotations

import pandas as pd

from sentinel.models.anomaly import FLAG_COLUMN, ID_COLUMN, SCORE_COLUMN

# Phase 4 outputs required for prioritization.
REQUIRED_SCORED_COLUMNS = [ID_COLUMN, SCORE_COLUMN, FLAG_COLUMN]

# Phase 3 columns used when present on the merged feature table (optional).
CONTEXT_FEATURE_COLUMNS = [
    "failed_login_ratio",
    "off_hours_access_flag",
    "unique_resource_count",
    "ip_diversity",
]

RISK_LEVEL_COLUMN = "risk_level"
PRIORITY_SCORE_COLUMN = "priority_score"
REASON_COLUMN = "reason_summary"

# Weighted sum (capped at 100). Tunable but fixed for reproducible demos.
W_ANOMALY_NORM = 40.0
W_FAILED_LOGIN = 22.0
W_OFF_HOURS = 15.0
W_RESOURCE_SPREAD = 12.0
W_IP_SPREAD = 11.0
W_OUTLIER_BONUS = 5.0

# Bands on priority_score (inclusive thresholds for High/Medium; Critical also uses a compound rule).
THRESHOLD_HIGH = 58.0
THRESHOLD_MEDIUM = 38.0
THRESHOLD_CRITICAL = 78.0


ALERT_PREVIEW_COLUMNS = [
    ID_COLUMN,
    RISK_LEVEL_COLUMN,
    PRIORITY_SCORE_COLUMN,
    REASON_COLUMN,
    SCORE_COLUMN,
    FLAG_COLUMN,
]


def _empty_alerts() -> pd.DataFrame:
    cols = [
        *ALERT_PREVIEW_COLUMNS,
        *CONTEXT_FEATURE_COLUMNS,
    ]
    return pd.DataFrame(columns=cols)


def validate_scored_for_prioritization(df: pd.DataFrame | None) -> list[str]:
    if df is None:
        return ["Scored table is missing."]
    if df.empty:
        return []
    missing = [c for c in REQUIRED_SCORED_COLUMNS if c not in df.columns]
    if missing:
        return [f"Missing required columns: {', '.join(missing)}."]
    return []


def _band_from_score(
    priority: float,
    *,
    is_anomaly: bool,
    failed_login_ratio: float,
    off_hours_flag: float,
) -> str:
    if priority >= THRESHOLD_CRITICAL or (
        is_anomaly and failed_login_ratio >= 0.35 and off_hours_flag >= 1.0
    ):
        return "Critical"
    if priority >= THRESHOLD_HIGH:
        return "High"
    if priority >= THRESHOLD_MEDIUM:
        return "Medium"
    return "Low"


def _reasons(
    *,
    norm_anomaly: float,
    failed_login_ratio: float,
    off_hours_flag: float,
    norm_res: float,
    norm_ip: float,
    is_anomaly: bool,
) -> str:
    parts: list[str] = []
    if norm_anomaly >= 0.66:
        parts.append("Strong relative anomaly score vs cohort")
    elif norm_anomaly >= 0.33:
        parts.append("Elevated anomaly score vs cohort")
    if failed_login_ratio >= 0.25:
        parts.append("High failed-login ratio")
    elif failed_login_ratio >= 0.1:
        parts.append("Notable failed-login ratio")
    if off_hours_flag >= 1.0:
        parts.append("Off-hours activity present")
    if norm_res >= 0.66:
        parts.append("Broad resource usage vs cohort")
    elif norm_res >= 0.33:
        parts.append("Above-typical resource breadth")
    if norm_ip >= 0.66:
        parts.append("High IP diversity vs cohort")
    elif norm_ip >= 0.33:
        parts.append("Above-typical IP diversity")
    if is_anomaly:
        parts.append("IsolationForest flagged outlier")
    if not parts:
        parts.append("Low rule-signal triage; review raw metrics if needed")
    return "; ".join(parts)


def prioritize_alerts(
    scored: pd.DataFrame | None,
    features: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, list[str]]:
    """Combine ML scores with simple security-context rules into sortable alerts.

    Merges optional ``features`` on ``user_id`` to enrich context columns when available.
    """
    errors = validate_scored_for_prioritization(scored)
    if errors:
        return _empty_alerts(), errors

    assert scored is not None
    if scored.empty:
        return _empty_alerts(), []

    work = scored[list(REQUIRED_SCORED_COLUMNS)].copy()
    if "anomaly_explanation" in scored.columns:
        work["anomaly_explanation"] = scored["anomaly_explanation"]

    merge_cols = [ID_COLUMN, *CONTEXT_FEATURE_COLUMNS]
    if features is not None and not features.empty:
        have = [c for c in merge_cols if c in features.columns]
        if len(have) > 1:
            work = work.merge(features[have], on=ID_COLUMN, how="left")

    for c in CONTEXT_FEATURE_COLUMNS:
        if c not in work.columns:
            work[c] = 0.0

    work["failed_login_ratio"] = pd.to_numeric(work["failed_login_ratio"], errors="coerce").fillna(0.0)
    work["off_hours_access_flag"] = pd.to_numeric(work["off_hours_access_flag"], errors="coerce").fillna(0.0)
    work["unique_resource_count"] = pd.to_numeric(work["unique_resource_count"], errors="coerce").fillna(0.0)
    work["ip_diversity"] = pd.to_numeric(work["ip_diversity"], errors="coerce").fillna(0.0)

    a = work[SCORE_COLUMN].astype(float)
    amin, amax = float(a.min()), float(a.max())
    if amax > amin:
        norm_a = (a - amin) / (amax - amin)
    else:
        norm_a = pd.Series(0.0, index=work.index)

    res = work["unique_resource_count"]
    ip = work["ip_diversity"]
    rmax = float(res.max()) if len(res) else 0.0
    ipmax = float(ip.max()) if len(ip) else 0.0
    norm_res = (res / rmax).clip(0.0, 1.0) if rmax > 0 else pd.Series(0.0, index=work.index)
    norm_ip = (ip / ipmax).clip(0.0, 1.0) if ipmax > 0 else pd.Series(0.0, index=work.index)

    failed = work["failed_login_ratio"].clip(0.0, 1.0)
    off = (work["off_hours_access_flag"] >= 1.0).astype(float)
    outlier = work[FLAG_COLUMN].astype(bool)

    raw_priority = (
        W_ANOMALY_NORM * norm_a
        + W_FAILED_LOGIN * failed
        + W_OFF_HOURS * off
        + W_RESOURCE_SPREAD * norm_res
        + W_IP_SPREAD * norm_ip
        + W_OUTLIER_BONUS * outlier.astype(float)
    )
    work[PRIORITY_SCORE_COLUMN] = raw_priority.clip(0.0, 100.0)

    levels: list[str] = []
    reasons: list[str] = []
    for i in work.index:
        levels.append(
            _band_from_score(
                float(work.at[i, PRIORITY_SCORE_COLUMN]),
                is_anomaly=bool(work.at[i, FLAG_COLUMN]),
                failed_login_ratio=float(work.at[i, "failed_login_ratio"]),
                off_hours_flag=float(work.at[i, "off_hours_access_flag"]),
            )
        )
        reasons.append(
            _reasons(
                norm_anomaly=float(norm_a.at[i]),
                failed_login_ratio=float(failed.at[i]),
                off_hours_flag=float(off.at[i]),
                norm_res=float(norm_res.at[i]),
                norm_ip=float(norm_ip.at[i]),
                is_anomaly=bool(work.at[i, FLAG_COLUMN]),
            )
        )
    work[RISK_LEVEL_COLUMN] = levels
    work[REASON_COLUMN] = reasons

    sort_cols = [PRIORITY_SCORE_COLUMN, ID_COLUMN]
    work = work.sort_values(sort_cols, ascending=[False, True], kind="mergesort")

    out_cols = [
        ID_COLUMN,
        RISK_LEVEL_COLUMN,
        PRIORITY_SCORE_COLUMN,
        REASON_COLUMN,
        SCORE_COLUMN,
        FLAG_COLUMN,
        *CONTEXT_FEATURE_COLUMNS,
    ]
    if "anomaly_explanation" in work.columns:
        out_cols.append("anomaly_explanation")
    return work.reset_index(drop=True)[out_cols], []
