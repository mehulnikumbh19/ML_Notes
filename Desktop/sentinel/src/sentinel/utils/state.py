"""Helpers for clearing Streamlit session state for demos."""

from __future__ import annotations

from typing import Iterable

DEFAULT_EXACT_KEYS = (
    "demo_df",
    "pipeline_norm_result",
    "pipeline_norm_sig",
    "pipeline_feat_df",
    "pipeline_feat_errs",
    "pipeline_feat_sig",
    "pipeline_score_df",
    "pipeline_score_errs",
    "pipeline_score_sig",
    "pipeline_risk_df",
    "pipeline_risk_errs",
    "pipeline_risk_sig",
)

DEFAULT_PREFIXES = ("pipeline_", "demo_")


def clear_demo_session_state(
    session_state: dict,
    *,
    exact_keys: Iterable[str] = DEFAULT_EXACT_KEYS,
    prefixes: Iterable[str] = DEFAULT_PREFIXES,
) -> int:
    """Clear SENTINEL demo keys from Streamlit session state.

    Returns the number of keys removed.
    """
    keys_to_remove = set(exact_keys)
    for key in list(session_state.keys()):
        if any(key.startswith(prefix) for prefix in prefixes):
            keys_to_remove.add(key)

    removed = 0
    for key in keys_to_remove:
        if key in session_state:
            session_state.pop(key, None)
            removed += 1
    return removed
