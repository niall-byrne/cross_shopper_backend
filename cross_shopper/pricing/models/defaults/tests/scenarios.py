"""Test scenarios for the pricing app model defaults generators."""

from datetime import datetime, timezone

import pytest

eoy_boundary_scenarios = pytest.mark.parametrize(
    "edge_case_datetime,iso_week_wrapping",
    [
        (datetime(2015, 12, 31, tzinfo=timezone.utc), True),
        (datetime(2017, 12, 27, tzinfo=timezone.utc), False),
        (datetime(2017, 12, 29, tzinfo=timezone.utc), True),
        (datetime(2017, 12, 31, tzinfo=timezone.utc), True),
    ],
)

non_boundary_scenarios = pytest.mark.parametrize(
    "test_datetime",
    [
        datetime(2015, 12, 18, tzinfo=timezone.utc),
    ],
)
