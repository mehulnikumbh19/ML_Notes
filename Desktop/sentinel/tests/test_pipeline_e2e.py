"""Phase 7 lightweight end-to-end pipeline test."""

from __future__ import annotations

import pandas as pd

from sentinel.features import build_user_features
from sentinel.ingest.normalize import normalize_uploaded_csv
from sentinel.ingest.synthetic import generate_demo_events
from sentinel.models import score_user_feature_table
from sentinel.reports import build_csv_bytes, build_text_summary
from sentinel.risk import prioritize_alerts


def _to_auth_source_schema(demo_df: pd.DataFrame) -> pd.DataFrame:
    """Map synthetic demo columns into the Phase 2 `auth` source schema."""
    auth_df = pd.DataFrame(
        {
            "auth_event_id": demo_df["event_id"],
            "auth_time": demo_df["timestamp"],
            "user_id": demo_df["user_id"],
            "username": demo_df["username"],
            "user_role": demo_df["role"],
            "src_ip": demo_df["source_ip"],
            "device_id": demo_df["device_id"],
            "host": demo_df["hostname"],
            "country": demo_df["geo_country"],
            "auth_action": demo_df["action"],
            "resource": demo_df["resource"],
            "approval_required": demo_df["approval_required"],
            "approval_present": demo_df["approval_present"],
            "success": demo_df["success"],
            "failure_reason": demo_df["failure_reason"],
            "raw_source": demo_df["raw_source"],
        }
    )
    return auth_df


def test_pipeline_e2e_from_synthetic_to_reports():
    # 1) Synthetic generation
    demo_df = generate_demo_events(n=120, seed=42)
    assert not demo_df.empty
    assert {"event_id", "timestamp", "user_id"}.issubset(demo_df.columns)

    # 2) Normalization from an auth-shaped source frame
    auth_source_df = _to_auth_source_schema(demo_df)
    norm_result = normalize_uploaded_csv(auth_source_df, "auth")
    assert norm_result.errors == []
    normalized_df = norm_result.normalized_df
    assert not normalized_df.empty
    assert {"event_id", "event_type", "timestamp", "user_id"}.issubset(normalized_df.columns)

    # 3) Feature engineering
    features_df, feature_errors = build_user_features(normalized_df)
    assert feature_errors == []
    assert not features_df.empty
    assert {"user_id", "failed_login_ratio", "off_hours_access_flag"}.issubset(features_df.columns)

    # 4) Anomaly scoring
    scored_df, score_errors, _ = score_user_feature_table(features_df, random_state=42)
    assert score_errors == []
    assert not scored_df.empty
    assert {"user_id", "anomaly_score", "is_anomaly"}.issubset(scored_df.columns)

    # 5) Prioritization
    alerts_df, risk_errors = prioritize_alerts(scored_df, features_df)
    assert risk_errors == []
    assert not alerts_df.empty
    assert {"user_id", "risk_level", "priority_score", "reason_summary"}.issubset(alerts_df.columns)

    # 6) Report exports
    csv_bytes = build_csv_bytes(alerts_df)
    text_summary = build_text_summary(alerts_df, run_date="20260323")
    assert isinstance(csv_bytes, bytes)
    assert len(csv_bytes) > 0
    assert isinstance(text_summary, str)
    assert len(text_summary.strip()) > 0
