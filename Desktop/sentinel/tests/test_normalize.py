"""Tests for Phase 2 ingestion mapping and validation."""

from __future__ import annotations

import pandas as pd
import pytest

from sentinel.ingest.normalize import (
    SOURCE_MAPPINGS,
    get_source_mapping,
    normalize_uploaded_csv,
    required_source_columns,
)
from sentinel.schemas import CANONICAL_COLUMNS


def test_get_source_mapping_supports_two_telemetry_types():
    assert set(SOURCE_MAPPINGS.keys()) >= {"auth", "access"}
    assert isinstance(get_source_mapping("auth"), dict)
    assert isinstance(get_source_mapping("access"), dict)


def test_required_source_columns_for_auth():
    cols = required_source_columns("auth")
    assert "auth_event_id" in cols
    assert "auth_time" in cols
    assert "raw_source" in cols


def test_normalize_auth_happy_path():
    source = pd.DataFrame(
        [
            {
                "auth_event_id": "a-1",
                "auth_time": "2025-01-01T01:00:00Z",
                "user_id": "u1",
                "username": "alice",
                "user_role": "analyst",
                "src_ip": "203.0.113.1",
                "device_id": "dev-1",
                "host": "host-1",
                "country": "US",
                "auth_action": "login",
                "resource": "/vpn",
                "approval_required": "false",
                "approval_present": "false",
                "success": "true",
                "failure_reason": "",
                "raw_source": "auth_csv",
            }
        ]
    )
    result = normalize_uploaded_csv(source, "auth")
    assert result.is_valid
    assert list(result.normalized_df.columns) == CANONICAL_COLUMNS
    assert result.normalized_df.loc[0, "event_type"] == "auth"
    assert str(result.normalized_df.loc[0, "timestamp"]).startswith("2025-01-01")


def test_normalize_access_happy_path():
    source = pd.DataFrame(
        [
            {
                "access_event_id": "x-1",
                "event_ts": "2025-01-01T02:00:00Z",
                "uid": "u2",
                "user_name": "bob",
                "role_name": "engineer",
                "ip_address": "203.0.113.22",
                "device": "dev-22",
                "hostname": "host-22",
                "country_code": "US",
                "operation": "read",
                "resource_name": "/reports",
                "resource_sensitivity": "medium",
                "bytes_in": "10",
                "bytes_out": "250",
                "is_success": "1",
                "dest": "db.internal",
                "raw_source": "access_csv",
            }
        ]
    )
    result = normalize_uploaded_csv(source, "access")
    assert result.is_valid
    assert result.normalized_df.loc[0, "event_type"] == "access"
    assert result.normalized_df.loc[0, "bytes_out"] == 250


def test_validation_rejects_empty_upload():
    empty = pd.DataFrame()
    result = normalize_uploaded_csv(empty, "auth")
    assert not result.is_valid
    assert "Uploaded CSV is empty." in result.errors


def test_validation_rejects_missing_required_columns():
    source = pd.DataFrame([{"auth_event_id": "a-1"}])
    result = normalize_uploaded_csv(source, "auth")
    assert not result.is_valid
    assert any("Missing required source columns" in err for err in result.errors)


def test_validation_rejects_bad_timestamp():
    source = pd.DataFrame(
        [
            {
                "auth_event_id": "a-1",
                "auth_time": "not-a-time",
                "user_id": "u1",
                "username": "alice",
                "user_role": "analyst",
                "src_ip": "203.0.113.1",
                "device_id": "dev-1",
                "host": "host-1",
                "country": "US",
                "auth_action": "login",
                "resource": "/vpn",
                "approval_required": "false",
                "approval_present": "false",
                "success": "true",
                "failure_reason": "",
                "raw_source": "auth_csv",
            }
        ]
    )
    result = normalize_uploaded_csv(source, "auth")
    assert not result.is_valid
    assert any("Invalid timestamp values found" in err for err in result.errors)


def test_validation_rejects_invalid_mapping_case(monkeypatch: pytest.MonkeyPatch):
    broken = dict(SOURCE_MAPPINGS["auth"])
    broken["username"] = broken["user_id"]
    monkeypatch.setitem(SOURCE_MAPPINGS, "auth", broken)

    source = pd.DataFrame(
        [
            {
                "auth_event_id": "a-1",
                "auth_time": "2025-01-01T01:00:00Z",
                "user_id": "u1",
                "username": "alice",
                "raw_source": "auth_csv",
            }
        ]
    )
    result = normalize_uploaded_csv(source, "auth")
    assert not result.is_valid
    assert any("Invalid mapping: source column" in err for err in result.errors)
