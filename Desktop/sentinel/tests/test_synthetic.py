"""Tests for synthetic demo telemetry."""

import pandas as pd
import pytest

from sentinel.ingest.synthetic import demo_columns, generate_demo_events


def test_generate_demo_events_shape_and_columns():
    df = generate_demo_events(n=25, seed=7)
    assert len(df) == 25
    assert list(df.columns) == demo_columns()
    assert not df.empty


def test_generate_demo_events_deterministic_with_seed():
    a = generate_demo_events(n=10, seed=123)
    b = generate_demo_events(n=10, seed=123)
    pd.testing.assert_frame_equal(a, b)


def test_generate_demo_events_rejects_zero_rows():
    with pytest.raises(ValueError, match="at least 1"):
        generate_demo_events(n=0, seed=1)
