"""Phase 3 feature engineering (per-user behavioral aggregates)."""

from sentinel.features.user_behavior import (
    FEATURE_COLUMN_NAMES,
    REQUIRED_COLUMNS_FOR_FEATURES,
    build_user_features,
    feature_distribution_counts,
    feature_numeric_summary,
    validate_normalized_for_features,
)

__all__ = [
    "FEATURE_COLUMN_NAMES",
    "REQUIRED_COLUMNS_FOR_FEATURES",
    "build_user_features",
    "feature_distribution_counts",
    "feature_numeric_summary",
    "validate_normalized_for_features",
]
