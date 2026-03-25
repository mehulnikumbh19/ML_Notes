"""Phase 6 report export helpers."""

from __future__ import annotations

from io import StringIO

import pandas as pd


RISK_ORDER = ["Critical", "High", "Medium", "Low"]


def _sorted_alerts(alerts_df: pd.DataFrame) -> pd.DataFrame:
    """Return alerts sorted for analyst triage readability."""
    if alerts_df is None or alerts_df.empty:
        return pd.DataFrame()
    work = alerts_df.copy()
    if "risk_level" in work.columns:
        work["risk_level"] = pd.Categorical(work["risk_level"], categories=RISK_ORDER, ordered=True)
    sort_cols: list[str] = []
    ascending: list[bool] = []
    if "risk_level" in work.columns:
        sort_cols.append("risk_level")
        ascending.append(True)
    if "priority_score" in work.columns:
        sort_cols.append("priority_score")
        ascending.append(False)
    if "user_id" in work.columns:
        sort_cols.append("user_id")
        ascending.append(True)
    if sort_cols:
        work = work.sort_values(sort_cols, ascending=ascending, kind="mergesort")
    if "risk_level" in work.columns:
        work["risk_level"] = work["risk_level"].astype(str)
    return work.reset_index(drop=True)


def build_csv_bytes(alerts_df: pd.DataFrame) -> bytes:
    """Build UTF-8 CSV bytes for the full sorted alerts table."""
    sorted_df = _sorted_alerts(alerts_df)
    return sorted_df.to_csv(index=False).encode("utf-8")


def build_text_summary(alerts_df: pd.DataFrame, run_date: str) -> str:
    """Build a plain-text analyst narrative summary."""
    sorted_df = _sorted_alerts(alerts_df)
    total = len(sorted_df)
    counts = {level: 0 for level in RISK_ORDER}
    if "risk_level" in sorted_df.columns and not sorted_df.empty:
        vc = sorted_df["risk_level"].value_counts()
        for level in RISK_ORDER:
            counts[level] = int(vc.get(level, 0))

    lines = [
        f"SENTINEL Triage Report - {run_date}",
        "================================",
        f"Total users analyzed: {total}",
        (
            f"Critical: {counts['Critical']} | High: {counts['High']} | "
            f"Medium: {counts['Medium']} | Low: {counts['Low']}"
        ),
        "Top 5 Critical/High Users:",
    ]

    if sorted_df.empty:
        lines.append("No prioritized alerts available.")
    else:
        if "risk_level" in sorted_df.columns:
            top = sorted_df[sorted_df["risk_level"].isin(["Critical", "High"])].head(5)
        else:
            top = sorted_df.head(5)
        if top.empty:
            lines.append("No Critical/High users in this run.")
        else:
            for _, row in top.iterrows():
                user_id = row.get("user_id", "unknown")
                risk_level = row.get("risk_level", "Unknown")
                score = float(row.get("priority_score", 0.0))
                reason = row.get("reason_summary", "No reason provided.")
                ml_flag = bool(row.get("is_anomaly", False))
                failed_ratio = float(row.get("failed_login_ratio", 0.0))
                lines.append(f"{user_id} - Risk: {risk_level} - Score: {score:.1f}")
                lines.append(f"  Reason: {reason}")
                lines.append(f"  ML Flag: {ml_flag} | Failed Login Ratio: {failed_ratio:.2f}")

    # StringIO keeps this explicit and easy to read for beginners.
    buffer = StringIO()
    buffer.write("\n".join(lines))
    return buffer.getvalue()
