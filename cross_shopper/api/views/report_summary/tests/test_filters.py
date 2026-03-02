"""Tests for the ReportSummaryFilter."""

import pytest
from api.views.report_summary.filters import ReportSummaryFilter
from pricing.models.defaults.default_pricing_week import default_pricing_week
from pricing.models.defaults.default_pricing_year import default_pricing_year


@pytest.mark.django_db
class TestReportSummaryFilter:

  def test_instantiate__unspecified_week_and_year__populates_default_values(
      self,
  ) -> None:
    filter_set = ReportSummaryFilter(data={})

    assert filter_set.data['week'] == default_pricing_week()
    assert filter_set.data['year'] == default_pricing_year()

  def test_instantiate__specified_week_and_year__respects_values(self,) -> None:
    filter_set = ReportSummaryFilter(data={'week': 10, 'year': 2025})

    assert filter_set.data['week'] == 10
    assert filter_set.data['year'] == 2025
