"""Tests for Phase 4 IsolationForest scoring on user-level feature tables."""

from __future__ import annotations

import pandas as pd
import pytest

from sentinel.features.user_behavior import FEATURE_COLUMN_NAMES
from sentinel.models.anomaly import (
    SCORE_OUTPUT_COLUMNS,
    score_user_feature_table,
    validate_features_for_scoring,
)


def _feature_row(user_id: str, **kwargs) -> dict:
    base = {c: 0 for c in FEATURE_COLUMN_NAMES}
    base["user_id"] = user_id
    base.update(kwargs)
    return base


def test_score_happy_path_shape_and_finite_scores():
    df = pd.DataFrame(
        [
            _feature_row("u1", login_count_per_user=1, failed_login_ratio=0.0, access_frequency=1.0),
            _feature_row("u2", login_count_per_user=50, failed_login_ratio=0.9, access_frequency=20.0),
            _feature_row("u3", login_count_per_user=2, failed_login_ratio=0.1, access_frequency=1.5),
            _feature_row("u4", login_count_per_user=3, failed_login_ratio=0.2, access_frequency=2.0),
            _feature_row("u5", login_count_per_user=4, failed_login_ratio=0.15, access_frequency=2.5),
        ]
    )
    out, errs, info = score_user_feature_table(df, random_state=0)
    assert errs == []
    assert list(out.columns) == SCORE_OUTPUT_COLUMNS
    assert len(out) == 5
    assert out["anomaly_score"].notna().all()
    assert out["is_anomaly"].dtype == bool
    assert all(isinstance(s, str) and len(s) > 0 for s in out["anomaly_explanation"])
    assert "run" in info and info["run"].model is not None


def test_empty_features_empty_output_no_errors():
    df = pd.DataFrame(columns=["user_id", *FEATURE_COLUMN_NAMES])
    out, errs, info = score_user_feature_table(df)
    assert errs == []
    assert out.empty
    assert info.get("skipped_model") is True


def test_validate_and_score_none():
    assert validate_features_for_scoring(None)
    out, errs, _ = score_user_feature_table(None)
    assert errs
    assert out.empty


def test_missing_user_id():
    df = pd.DataFrame([{c: 0 for c in FEATURE_COLUMN_NAMES}])
    assert validate_features_for_scoring(df)
    out, errs, _ = score_user_feature_table(df)
    assert errs
    assert out.empty


def test_no_numeric_feature_columns():
    df = pd.DataFrame([{"user_id": "a", "extra": 1}])
    assert validate_features_for_scoring(df)
    out, errs, _ = score_user_feature_table(df)
    assert errs
    assert out.empty


def test_single_user_neutral_scores():
    df = pd.DataFrame(
        [_feature_row("only", login_count_per_user=10, failed_login_ratio=0.5, access_frequency=3.0)]
    )
    out, errs, info = score_user_feature_table(df, random_state=0)
    assert errs == []
    assert len(out) == 1
    assert out.iloc[0]["anomaly_score"] == 0.0
    assert not bool(out.iloc[0]["is_anomaly"])
    assert "at least 2" in out.iloc[0]["anomaly_explanation"].lower()
    assert info.get("skipped_model") is True


def test_nan_features_filled():
    df = pd.DataFrame(
        [
            _feature_row("a", login_count_per_user=1),
            _feature_row("b", login_count_per_user=2),
        ]
    )
    df.loc[0, "failed_login_ratio"] = float("nan")
    out, errs, _ = score_user_feature_table(df, random_state=1)
    assert errs == []
    assert len(out) == 2


def test_two_users_trains_model():
    df = pd.DataFrame(
        [
            _feature_row("x", login_count_per_user=1, access_frequency=1.0),
            _feature_row("y", login_count_per_user=100, access_frequency=50.0),
        ]
    )
    out, errs, info = score_user_feature_table(df, random_state=2)
    assert errs == []
    assert info.get("run") is not None
    assert len(out) == 2
