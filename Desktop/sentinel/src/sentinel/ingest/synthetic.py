"""Synthetic security telemetry for demos and tests (not real events)."""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd

# Subset of canonical fields (full schema comes in Phase 2).
_DEMO_COLUMNS = [
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
    "raw_source",
]


def generate_demo_events(n: int = 50, seed: int | None = None) -> pd.DataFrame:
    """Build a reproducible demo DataFrame of synthetic security-like events.

    Args:
        n: Number of rows to generate (must be >= 1).
        seed: Optional RNG seed for repeatable output.

    Returns:
        DataFrame with canonical-like columns suitable for later normalization.
    """
    if n < 1:
        raise ValueError("n must be at least 1")

    rng = np.random.default_rng(seed)
    base = datetime(2025, 1, 1, 8, 0, 0, tzinfo=timezone.utc)

    users = [("u001", "alice", "analyst"), ("u002", "bob", "engineer"), ("u003", "carol", "admin")]
    actions = ["login", "read", "write", "approve", "download"]
    resources = ["/reports/q1", "/config/app", "/data/customers", "/admin/users"]
    countries = ["US", "US", "US", "GB", "DE"]
    hostnames = ["laptop-01", "laptop-02", "srv-app-1"]

    rows: list[dict] = []
    for _ in range(n):
        uid, uname, role = users[int(rng.integers(0, len(users)))]
        success = bool(rng.random() > 0.12)
        approval_required = bool(rng.random() > 0.75)
        approval_present = approval_required and bool(rng.random() > 0.35)
        if not success:
            approval_present = False

        ts = base + timedelta(
            minutes=int(rng.integers(0, 60 * 24 * 3)),
            seconds=int(rng.integers(0, 59)),
        )

        event_id = str(uuid.UUID(bytes=bytes(rng.integers(0, 256, size=16, dtype=np.uint8))))
        bip = int(rng.integers(100, 5000))
        bop = int(rng.integers(0, 2_000_000))
        fail_reasons = np.array(["bad_password", "mfa_failed", "locked"])

        rows.append(
            {
                "event_id": event_id,
                "event_type": "auth" if rng.random() > 0.5 else "access",
                "timestamp": ts.isoformat(),
                "user_id": uid,
                "username": uname,
                "role": role,
                "source_ip": f"203.0.113.{int(rng.integers(1, 200))}",
                "device_id": f"dev-{int(rng.integers(100, 999))}",
                "hostname": hostnames[int(rng.integers(0, len(hostnames)))],
                "geo_country": countries[int(rng.integers(0, len(countries)))],
                "action": actions[int(rng.integers(0, len(actions)))],
                "resource": resources[int(rng.integers(0, len(resources)))],
                "resource_sensitivity": ["low", "medium", "high"][int(rng.integers(0, 3))],
                "approval_required": approval_required,
                "approval_present": approval_present,
                "success": success,
                "failure_reason": "" if success else str(rng.choice(fail_reasons)),
                "bytes_in": bip,
                "bytes_out": bop,
                "raw_source": "synthetic_demo",
            }
        )

    return pd.DataFrame(rows, columns=_DEMO_COLUMNS)


def demo_columns() -> list[str]:
    """Column names produced by :func:`generate_demo_events`."""
    return list(_DEMO_COLUMNS)
