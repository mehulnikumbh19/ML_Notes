"""Tests for Phase 6 reporting exports."""

from __future__ import annotations

import pandas as pd

from sentinel.reports import build_csv_bytes, build_text_summary


def _minimal_alerts_df() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "user_id": "alice",
                "risk_level": "High",
                "priority_score": 84.2,
                "reason_summary": "High failed-login ratio; Off-hours activity present",
                "anomaly_score": 1.2,
                "is_anomaly": True,
                "failed_login_ratio": 0.72,
                "off_hours_access_flag": 1,
                "unique_resource_count": 8,
                "ip_diversity": 4,
                "anomaly_explanation": "Top factor: failed_login_ratio",
            }
        ]
    )


def test_build_csv_bytes_non_empty():
    alerts = _minimal_alerts_df()
    out = build_csv_bytes(alerts)
    assert isinstance(out, bytes)
    assert len(out) > 0


def test_build_text_summary_non_empty():
    alerts = _minimal_alerts_df()
    out = build_text_summary(alerts, run_date="20260323")
    assert isinstance(out, str)
    assert len(out.strip()) > 0


def test_build_text_summary_contains_key_fields():
    alerts = _minimal_alerts_df()
    out = build_text_summary(alerts, run_date="20260323")
    assert "Total users analyzed" in out
    assert ("Critical" in out) or ("High" in out) or ("Medium" in out) or ("Low" in out)
