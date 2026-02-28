"""Tests for the ReportSummaryHistoricalItemPriceSerializer."""

import decimal
import pytest
from freezegun import freeze_time
from pricing.models.factories.pricing import PriceFactory
from reports.models.serializers.report_summary.item_price_history import (
    ReportSummaryItemPriceHistorySerializer,
)


@pytest.mark.django_db
class TestReportSummaryHistoricalItemPriceSerializer:
  """Tests for the ReportSummaryHistoricalItemPriceSerializer."""

  def test_serialize__no_context__returns_none(self, item):
    serializer = ReportSummaryItemPriceHistorySerializer(item)
    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }

  @freeze_time("2024-06-01")
  def test_serialize__with_context_and_history__returns_correct_data(
      self, item, report
  ):
    # Ensure current week/year used by manager is what we expect
    from pricing.models.defaults.default_pricing_week import default_pricing_week
    from pricing.models.defaults.default_pricing_year import default_pricing_year

    current_week = default_pricing_week()
    current_year = default_pricing_year()

    store = report.store.all()[0]

    PriceFactory(
        item=item,
        store=store,
        amount=decimal.Decimal('10.00'),
        year=current_year,
        week=current_week,
    )
    # 2024-06-01 is middle of year, so current_week > 1
    prev_week = current_week - 1
    prev_year = current_year

    PriceFactory(
        item=item,
        store=store,
        amount=decimal.Decimal('20.00'),
        year=prev_year,
        week=prev_week,
    )

    serializer = ReportSummaryItemPriceHistorySerializer(
        item,
        context={'report': report},
    )

    data = serializer.data
    # Manager quantizes average to .01, high/low to .00
    assert data['average'] == '15.00'
    assert data['high'] == '20.00'
    assert data['low'] == '10.00'

  def test_serialize__no_report_in_context__returns_none(self, item):
    serializer = ReportSummaryItemPriceHistorySerializer(
        item,
        context={},
    )
    assert serializer.data == {
        'average': None,
        'high': None,
        'low': None,
    }
