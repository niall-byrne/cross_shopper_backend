"""Tests for the ReportSummaryFilter."""

from typing import Any

import pytest
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year
from ..filters import ReportSummaryFilter


@pytest.mark.django_db
class TestReportSummaryFilter:
  """Tests for the ReportSummaryFilter."""

  def test_init__missing_week_year__populates_default_values(
      self,
  ) -> None:
    filter_set = ReportSummaryFilter(data={})

    assert filter_set.data['week'] == default_pricing_week()
    assert filter_set.data['year'] == default_pricing_year()

  def test_init__provided_week_year__respects_values(
      self,
  ) -> None:
    filter_set = ReportSummaryFilter(data={'week': 10, 'year': 2025})

    assert filter_set.data['week'] == 10
    assert filter_set.data['year'] == 2025
