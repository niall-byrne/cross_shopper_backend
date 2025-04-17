"""Test scenarios for the Pricing model aggregate last 52 weeks manager."""

import pytest

eoy_boundary_scenarios = pytest.mark.parametrize(
    "test_datetime",
    [
        "2035-1-1",
        "2035-12-25",
    ],
)
