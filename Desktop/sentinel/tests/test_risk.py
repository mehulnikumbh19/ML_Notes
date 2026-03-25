"""Tests for Phase 5 deterministic risk prioritization."""

from __future__ import annotations

import pandas as pd

from sentinel.models.anomaly import FLAG_COLUMN, ID_COLUMN, SCORE_COLUMN
from sentinel.risk.prioritization import (
    PRIORITY_SCORE_COLUMN,
    REASON_COLUMN,
    REQUIRED_SCORED_COLUMNS,
    RISK_LEVEL_COLUMN,
    prioritize_alerts,
    validate_scored_for_prioritization,
)


def _scored_row(user_id: str, anomaly_score: float, is_anomaly: bool) -> dict:
    return {ID_COLUMN: user_id, SCORE_COLUMN: anomaly_score, FLAG_COLUMN: is_anomaly}


def test_empty_scored_no_errors():
    df = pd.DataFrame(columns=REQUIRED_SCORED_COLUMNS)
    out, errs = prioritize_alerts(df)
    assert errs == []
    assert out.empty


def test_missing_required_columns():
    bad = pd.DataFrame([{"user_id": "a", "anomaly_score": 1.0}])
    assert validate_scored_for_prioritization(bad)
    out, errs = prioritize_alerts(bad)
    assert errs
    assert out.empty


def test_none_scored_errors():
    assert validate_scored_for_prioritization(None)
    out, errs = prioritize_alerts(None)
    assert errs
    assert out.empty


def test_prioritization_stable_sorted():
    scored = pd.DataFrame(
        [
            _scored_row("z", 0.5, False),
            _scored_row("a", 0.5, False),
            _scored_row("m", 1.0, True),
        ]
    )
    feats = pd.DataFrame(
        [
            {
                ID_COLUMN: "z",
                "failed_login_ratio": 0.0,
                "off_hours_access_flag": 0,
                "unique_resource_count": 1,
                "ip_diversity": 1,
            },
            {
                ID_COLUMN: "a",
                "failed_login_ratio": 0.0,
                "off_hours_access_flag": 0,
                "unique_resource_count": 1,
                "ip_diversity": 1,
            },
            {
                ID_COLUMN: "m",
                "failed_login_ratio": 0.5,
                "off_hours_access_flag": 1,
                "unique_resource_count": 20,
                "ip_diversity": 10,
            },
        ]
    )
    out1, e1 = prioritize_alerts(scored, feats)
    out2, e2 = prioritize_alerts(scored, feats)
    assert e1 == e2 == []
    assert list(out1[ID_COLUMN]) == list(out2[ID_COLUMN])
    assert out1.iloc[0][ID_COLUMN] == "m"
    assert out1.iloc[0][RISK_LEVEL_COLUMN] in ("Critical", "High", "Medium", "Low")
    assert out1[PRIORITY_SCORE_COLUMN].is_monotonic_decreasing


def test_high_failed_and_off_hours_escalates():
    scored = pd.DataFrame(
        [
            _scored_row("quiet", 0.1, False),
            _scored_row("noisy", 0.2, True),
        ]
    )
    feats = pd.DataFrame(
        [
            {
                ID_COLUMN: "quiet",
                "failed_login_ratio": 0.0,
                "off_hours_access_flag": 0,
                "unique_resource_count": 1,
                "ip_diversity": 1,
            },
            {
                ID_COLUMN: "noisy",
                "failed_login_ratio": 0.6,
                "off_hours_access_flag": 1,
                "unique_resource_count": 50,
                "ip_diversity": 20,
            },
        ]
    )
    out, errs = prioritize_alerts(scored, feats)
    assert errs == []
    row_noisy = out.loc[out[ID_COLUMN] == "noisy"].iloc[0]
    row_quiet = out.loc[out[ID_COLUMN] == "quiet"].iloc[0]
    assert row_noisy[PRIORITY_SCORE_COLUMN] > row_quiet[PRIORITY_SCORE_COLUMN]
    assert row_noisy[RISK_LEVEL_COLUMN] in ("Critical", "High")
    assert "failed-login" in row_noisy[REASON_COLUMN].lower() or "off-hours" in row_noisy[REASON_COLUMN].lower()


def test_without_features_uses_zeros():
    scored = pd.DataFrame([_scored_row("solo", 1.0, True)])
    out, errs = prioritize_alerts(scored, None)
    assert errs == []
    assert len(out) == 1
    assert out.iloc[0][ID_COLUMN] == "solo"


def test_reason_summary_non_empty():
    scored = pd.DataFrame([_scored_row("u", 0.0, False)])
    out, errs = prioritize_alerts(scored)
    assert errs == []
    assert len(out[REASON_COLUMN].iloc[0]) > 0
