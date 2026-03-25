"""Tests for Phase 3 user-level behavioral features."""

from __future__ import annotations

import pandas as pd
import pytest

from sentinel.features.user_behavior import (
    FEATURE_COLUMN_NAMES,
    build_user_features,
    feature_numeric_summary,
    validate_normalized_for_features,
)


def _base_row(**overrides):
    row = {
        "event_id": "e1",
        "event_type": "auth",
        "timestamp": pd.Timestamp("2025-01-06T10:00:00Z"),  # Monday business hours
        "user_id": "u1",
        "username": "a",
        "success": True,
        "resource": "/a",
        "source_ip": "203.0.113.1",
    }
    row.update(overrides)
    return row


def test_validate_empty_dataframe_ok():
    df = pd.DataFrame(columns=["user_id", "timestamp", "event_type", "success", "resource", "source_ip"])
    assert validate_normalized_for_features(df) == []


def test_validate_missing_columns():
    df = pd.DataFrame([{"user_id": "u1"}])
    errs = validate_normalized_for_features(df)
    assert len(errs) == 1
    assert "Missing required columns" in errs[0]


def test_validate_none():
    errs = validate_normalized_for_features(None)
    assert "missing" in errs[0].lower()


def test_build_features_happy_path_counts():
    df = pd.DataFrame(
        [
            _base_row(event_id="1", success=True, source_ip="10.0.0.1", resource="/r1"),
            _base_row(event_id="2", success=False, source_ip="10.0.0.2", resource="/r2"),
            _base_row(
                event_id="3",
                event_type="access",
                success=True,
                source_ip="10.0.0.1",
                resource="/r3",
                timestamp=pd.Timestamp("2025-01-06T22:00:00Z"),
            ),
        ]
    )
    out, errs = build_user_features(df)
    assert errs == []
    assert len(out) == 1
    assert list(out.columns) == ["user_id", *FEATURE_COLUMN_NAMES]
    assert out.iloc[0]["login_count_per_user"] == 2
    assert out.iloc[0]["failed_login_ratio"] == pytest.approx(0.5)
    assert out.iloc[0]["off_hours_access_flag"] == 1
    assert out.iloc[0]["unique_resource_count"] == 3
    assert out.iloc[0]["ip_diversity"] == 2
    assert out.iloc[0]["access_frequency"] == pytest.approx(3.0)


def test_all_business_hours_flag_zero():
    df = pd.DataFrame(
        [
            _base_row(event_id="1", timestamp=pd.Timestamp("2025-01-07T12:00:00Z")),  # Tuesday
            _base_row(event_id="2", timestamp=pd.Timestamp("2025-01-07T15:00:00Z")),
        ]
    )
    out, errs = build_user_features(df)
    assert errs == []
    assert out.iloc[0]["off_hours_access_flag"] == 0


def test_empty_normalized_returns_empty_features():
    df = pd.DataFrame(
        columns=[
            "user_id",
            "timestamp",
            "event_type",
            "success",
            "resource",
            "source_ip",
        ]
    )
    out, errs = build_user_features(df)
    assert errs == []
    assert out.empty


def test_all_missing_user_id_errors():
    df = pd.DataFrame(
        [
            {
                "user_id": None,
                "timestamp": pd.Timestamp("2025-01-06T10:00:00Z"),
                "event_type": "auth",
                "success": True,
                "resource": "/x",
                "source_ip": "1.1.1.1",
            }
        ]
    )
    out, errs = build_user_features(df)
    assert out.empty
    assert any("user_id" in e.lower() for e in errs)


def test_user_with_only_access_has_zero_logins():
    df = pd.DataFrame(
        [
            {
                "event_id": "a",
                "event_type": "access",
                "timestamp": pd.Timestamp("2025-01-06T11:00:00Z"),
                "user_id": "u9",
                "username": "x",
                "success": True,
                "resource": "/z",
                "source_ip": "10.0.0.1",
            }
        ]
    )
    out, errs = build_user_features(df)
    assert errs == []
    assert out.iloc[0]["login_count_per_user"] == 0
    assert out.iloc[0]["failed_login_ratio"] == 0.0


def test_feature_numeric_summary_empty():
    empty = pd.DataFrame(columns=["user_id", *FEATURE_COLUMN_NAMES])
    assert feature_numeric_summary(empty).empty


def test_access_frequency_averages_over_active_days():
    df = pd.DataFrame(
        [
            _base_row(event_id="1", timestamp=pd.Timestamp("2025-01-06T10:00:00Z")),
            _base_row(event_id="2", timestamp=pd.Timestamp("2025-01-07T10:00:00Z")),
        ]
    )
    out, errs = build_user_features(df)
    assert errs == []
    assert out.iloc[0]["access_frequency"] == pytest.approx(1.0)
