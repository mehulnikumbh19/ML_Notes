"""Pydantic schemas for normalized SENTINEL telemetry."""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

CANONICAL_COLUMNS = [
    "event_id",
    "event_type",
    "timestamp",
    "user_id",
    "username",
    "role",
    "source_ip",
    "device_id",
    "hostname",
    "geo_country",
    "action",
    "resource",
    "resource_sensitivity",
    "approval_required",
    "approval_present",
    "success",
    "failure_reason",
    "bytes_in",
    "bytes_out",
    "endpoint_process",
    "network_destination",
    "raw_source",
]


class CanonicalEventSchema(BaseModel):
    """Canonical schema used after source-specific normalization."""

    event_id: str
    event_type: str
    timestamp: datetime
    user_id: str
    username: str
    role: Optional[str] = None
    source_ip: Optional[str] = None
    device_id: Optional[str] = None
    hostname: Optional[str] = None
    geo_country: Optional[str] = None
    action: Optional[str] = None
    resource: Optional[str] = None
    resource_sensitivity: Optional[str] = None
    approval_required: Optional[bool] = None
    approval_present: Optional[bool] = None
    success: Optional[bool] = None
    failure_reason: Optional[str] = None
    bytes_in: Optional[float] = None
    bytes_out: Optional[float] = None
    endpoint_process: Optional[str] = None
    network_destination: Optional[str] = None
    raw_source: str
