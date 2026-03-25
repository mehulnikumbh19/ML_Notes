"""CSV normalization and validation for Phase 2 ingestion."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from sentinel.schemas import CANONICAL_COLUMNS

TELEMETRY_TYPES = ("auth", "access")

SOURCE_MAPPINGS: dict[str, dict[str, str]] = {
    "auth": {
        "event_id": "auth_event_id",
        "timestamp": "auth_time",
        "user_id": "user_id",
        "username": "username",
        "role": "user_role",
        "source_ip": "src_ip",
        "device_id": "device_id",
        "hostname": "host",
        "geo_country": "country",
        "action": "auth_action",
        "resource": "resource",
        "approval_required": "approval_required",
        "approval_present": "approval_present",
        "success": "success",
        "failure_reason": "failure_reason",
        "raw_source": "raw_source",
    },
    "access": {
        "event_id": "access_event_id",
        "timestamp": "event_ts",
        "user_id": "uid",
        "username": "user_name",
        "role": "role_name",
        "source_ip": "ip_address",
        "device_id": "device",
        "hostname": "hostname",
        "geo_country": "country_code",
        "action": "operation",
        "resource": "resource_name",
        "resource_sensitivity": "resource_sensitivity",
        "bytes_in": "bytes_in",
        "bytes_out": "bytes_out",
        "success": "is_success",
        "network_destination": "dest",
        "raw_source": "raw_source",
    },
}

REQUIRED_CANONICAL_FIELDS = ("event_id", "timestamp", "user_id", "username", "raw_source")
BOOL_FIELDS = ("approval_required", "approval_present", "success")
NUMERIC_FIELDS = ("bytes_in", "bytes_out")


@dataclass
class NormalizationResult:
    normalized_df: pd.DataFrame
    errors: list[str]

    @property
    def is_valid(self) -> bool:
        return not self.errors


def get_source_mapping(telemetry_type: str) -> dict[str, str]:
    """Return canonical-to-source mapping for the given telemetry type."""
    if telemetry_type not in SOURCE_MAPPINGS:
        supported = ", ".join(TELEMETRY_TYPES)
        raise ValueError(f"Unsupported telemetry type '{telemetry_type}'. Supported: {supported}.")
    return SOURCE_MAPPINGS[telemetry_type]


def required_source_columns(telemetry_type: str) -> list[str]:
    """Required source columns that must exist for normalization."""
    mapping = get_source_mapping(telemetry_type)
    required = [mapping[field] for field in REQUIRED_CANONICAL_FIELDS]
    return sorted(set(required))


def normalize_uploaded_csv(df: pd.DataFrame, telemetry_type: str) -> NormalizationResult:
    """Normalize a source DataFrame to the canonical SENTINEL schema."""
    errors = _validate_upload(df, telemetry_type)
    if errors:
        return NormalizationResult(normalized_df=pd.DataFrame(columns=CANONICAL_COLUMNS), errors=errors)

    mapping = get_source_mapping(telemetry_type)
    normalized = pd.DataFrame(index=df.index, columns=CANONICAL_COLUMNS)
    normalized[:] = pd.NA

    for canonical_col, source_col in mapping.items():
        normalized[canonical_col] = df[source_col]

    normalized["event_type"] = telemetry_type

    timestamp_series = pd.to_datetime(normalized["timestamp"], errors="coerce", utc=True)
    invalid_timestamps = int(timestamp_series.isna().sum())
    if invalid_timestamps > 0:
        errors.append(f"Invalid timestamp values found: {invalid_timestamps}.")
    normalized["timestamp"] = timestamp_series

    for field in BOOL_FIELDS:
        if field in normalized.columns:
            normalized[field] = _coerce_bool_series(normalized[field])

    for field in NUMERIC_FIELDS:
        if field in normalized.columns:
            normalized[field] = pd.to_numeric(normalized[field], errors="coerce")

    if normalized["event_id"].astype(str).str.strip().eq("").all():
        errors.append("All event_id values are empty after mapping.")

    return NormalizationResult(normalized_df=normalized, errors=errors)


def _validate_upload(df: pd.DataFrame, telemetry_type: str) -> list[str]:
    errors: list[str] = []
    if df is None:
        return ["Upload is missing."]
    if df.empty:
        return ["Uploaded CSV is empty."]

    try:
        mapping = get_source_mapping(telemetry_type)
    except ValueError as exc:
        return [str(exc)]

    mapped_source_columns = list(mapping.values())
    missing = sorted([col for col in required_source_columns(telemetry_type) if col not in df.columns])
    if missing:
        errors.append(
            "Missing required source columns for "
            f"{telemetry_type}: {', '.join(missing)}."
        )

    reversed_mapping = {}
    for canonical, source in mapping.items():
        existing = reversed_mapping.get(source)
        if existing is not None and existing != canonical:
            errors.append(
                f"Invalid mapping: source column '{source}' maps to multiple canonical fields "
                f"('{existing}', '{canonical}')."
            )
        reversed_mapping[source] = canonical

    extra_required = [col for col in REQUIRED_CANONICAL_FIELDS if col not in mapping]
    if extra_required:
        errors.append(
            "Invalid mapping config for "
            f"{telemetry_type}: missing canonical fields {', '.join(extra_required)}."
        )

    for col in mapped_source_columns:
        if col in df.columns and df[col].isna().all():
            errors.append(f"Mapped source column '{col}' is entirely empty.")

    return errors


def _coerce_bool_series(series: pd.Series) -> pd.Series:
    """Convert common bool-like values to pandas nullable booleans."""
    truthy = {"true", "1", "yes", "y"}
    falsy = {"false", "0", "no", "n"}

    def _coerce(value: Any) -> Any:
        if pd.isna(value):
            return pd.NA
        text = str(value).strip().lower()
        if text in truthy:
            return True
        if text in falsy:
            return False
        if text in {"", "na", "n/a", "none", "null", "nan"}:
            return pd.NA
        return pd.NA

    return series.map(_coerce).astype("boolean")

