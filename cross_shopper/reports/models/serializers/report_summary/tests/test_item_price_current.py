"""Tests for the ReportSummaryCurrentItemPriceSerializer."""

import decimal
import pytest
from pricing.models.factories.pricing import PriceFactory
from reports.models.serializers.report_summary.item_price_current import (
    ReportSummaryCurrentItemPriceSerializer,
)


@pytest.mark.django_db
class TestReportSummaryCurrentItemPriceSerializer:
  """Tests for the ReportSummaryCurrentItemPriceSerializer."""

  def test_serialize__no_context__returns_empty_or_none(self, item):
    serializer = ReportSummaryCurrentItemPriceSerializer(item)
    assert serializer.data == {
        'average': None,
        'best': None,
        'per_store': {},
    }

  def test_serialize__with_context_and_prices__returns_correct_data(
      self, item, report
  ):
    store1 = report.store.all()[0]
    store2 = report.store.all()[1]
    PriceFactory(
        item=item,
        store=store1,
        amount=decimal.Decimal('10.00'),
        year=2024,
        week=1,
    )
    PriceFactory(
        item=item,
        store=store2,
        amount=decimal.Decimal('20.00'),
        year=2024,
        week=1,
    )

    serializer = ReportSummaryCurrentItemPriceSerializer(
        item,
        context={
            'report': report,
            'week': 1,
            'year': 2024,
        },
    )

    data = serializer.data
    assert data['per_store'][str(store1.id)] == '10.00'
    assert data['per_store'][str(store2.id)] == '20.00'
    assert data['average'] == '15.00'
    assert data['best'] == '10.00'

  def test_serialize__with_partial_prices__handles_missing_stores(
      self, item, report
  ):
    store1 = report.store.all()[0]
    # No price for store2
    PriceFactory(
        item=item,
        store=store1,
        amount=decimal.Decimal('10.00'),
        year=2024,
        week=1,
    )

    serializer = ReportSummaryCurrentItemPriceSerializer(
        item,
        context={
            'report': report,
            'week': 1,
            'year': 2024,
        },
    )

    data = serializer.data
    assert data['per_store'][str(store1.id)] == '10.00'
    assert data['per_store'][str(report.store.all()[1].id)] is None
    assert data['average'] == '10.00'
    assert data['best'] == '10.00'
