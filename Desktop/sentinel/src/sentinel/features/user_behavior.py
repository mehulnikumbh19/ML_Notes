"""Per-user behavioral features from normalized SENTINEL telemetry (Phase 3)."""

from __future__ import annotations

import pandas as pd

# Columns produced by :func:`build_user_features` (one row per user_id).
FEATURE_COLUMN_NAMES = [
    "login_count_per_user",
    "failed_login_ratio",
    "off_hours_access_flag",
    "unique_resource_count",
    "ip_diversity",
    "access_frequency",
]

# Minimum canonical columns needed for the Phase 3 feature set.
REQUIRED_COLUMNS_FOR_FEATURES = [
    "user_id",
    "timestamp",
    "event_type",
    "success",
    "resource",
    "source_ip",
]


def validate_normalized_for_features(df: pd.DataFrame | None) -> list[str]:
    """Return human-readable validation errors, or an empty list if input is usable."""
    if df is None:
        return ["DataFrame is missing."]
    if df.empty:
        return []
    missing = [c for c in REQUIRED_COLUMNS_FOR_FEATURES if c not in df.columns]
    if missing:
        return [f"Missing required columns: {', '.join(missing)}."]
    return []


def _empty_feature_frame() -> pd.DataFrame:
    return pd.DataFrame(columns=["user_id", *FEATURE_COLUMN_NAMES])


def _failed_login_ratio(group: pd.Series) -> float:
    """Share of auth attempts where ``success`` is explicitly False (NaN success ignored)."""
    ok = group.notna()
    if not ok.any():
        return 0.0
    return float((group[ok] == False).sum() / ok.sum())


def build_user_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Aggregate normalized events into one row per ``user_id`` with behavioral features.

    Returns:
        (feature_dataframe, errors). On validation failure, returns an empty frame and errors.
    """
    errors = validate_normalized_for_features(df)
    if errors:
        return _empty_feature_frame(), errors

    if df.empty:
        return _empty_feature_frame(), []

    work = df.dropna(subset=["user_id"]).copy()
    if work.empty:
        return _empty_feature_frame(), ["All rows have missing user_id."]

    ts = pd.to_datetime(work["timestamp"], utc=True)
    work["_business_hours"] = (ts.dt.weekday < 5) & (ts.dt.hour >= 9) & (ts.dt.hour < 18)
    work["_day"] = ts.dt.normalize()

    auth_mask = work["event_type"].astype(str) == "auth"
    auth_only = work.loc[auth_mask]

    login_count = auth_only.groupby("user_id", sort=False).size()
    failed_ratio = auth_only.groupby("user_id", sort=False)["success"].agg(_failed_login_ratio)

    off_hours_flag = work.groupby("user_id", sort=False)["_business_hours"].agg(
        lambda s: int((~s).any())
    )

    unique_resources = work.groupby("user_id", sort=False)["resource"].nunique(dropna=True)
    ip_diversity = work.groupby("user_id", sort=False)["source_ip"].nunique(dropna=True)

    event_counts = work.groupby("user_id", sort=False).size()
    active_days = work.groupby("user_id", sort=False)["_day"].nunique()
    access_frequency = event_counts / active_days.replace(0, 1)

    users = pd.Index(work["user_id"].unique())
    out = pd.DataFrame({"user_id": users}).set_index("user_id")
    out["login_count_per_user"] = login_count.reindex(out.index, fill_value=0).astype("int64")
    out["failed_login_ratio"] = failed_ratio.reindex(out.index, fill_value=0.0).astype(float)
    out["off_hours_access_flag"] = off_hours_flag.reindex(out.index, fill_value=0).astype("int64")
    out["unique_resource_count"] = unique_resources.reindex(out.index, fill_value=0).astype("int64")
    out["ip_diversity"] = ip_diversity.reindex(out.index, fill_value=0).astype("int64")
    out["access_frequency"] = access_frequency.reindex(out.index, fill_value=0.0).astype(float)

    return out.reset_index(), []


def feature_numeric_summary(features: pd.DataFrame) -> pd.DataFrame:
    """``DataFrame.describe()`` for numeric feature columns (empty if no rows)."""
    if features.empty:
        return pd.DataFrame()
    numeric_cols = [c for c in FEATURE_COLUMN_NAMES if c in features.columns]
    if not numeric_cols:
        return pd.DataFrame()
    return features[numeric_cols].describe(include="all")


def feature_distribution_counts(features: pd.DataFrame) -> dict[str, pd.Series]:
    """Simple discrete distributions for the UI (e.g. off-hours flag counts)."""
    out: dict[str, pd.Series] = {}
    if features.empty or "off_hours_access_flag" not in features.columns:
        return out
    out["off_hours_access_flag"] = features["off_hours_access_flag"].value_counts(dropna=False).sort_index()
    return out
