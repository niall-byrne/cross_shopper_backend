"""Tests for the JSON serializers."""

import decimal

import pytest
from freezegun import freeze_time
from pricing.models.factories.pricing import PriceFactory
from reports.models.serializers.report_summary.item import (
    ReportSummaryItemSerializer,
)
from reports.models.serializers.report_summary.report import (
    ReportSummarySerializer,
)
from reports.models.serializers.report_summary.store import (
    ReportSummaryStoreSerializer,
)


@pytest.mark.django_db
class TestStoreJsonSerializer:
  """Tests for the StoreJsonSerializer."""

  def test_serialize(self, store):
    serializer = ReportSummaryStoreSerializer(store)
    assert serializer.data == {
        'id': store.id,
        'franchise_name': store.franchise.name,
    }


@pytest.mark.django_db
class TestItemJsonSerializer:
  """Tests for the ItemJsonSerializer."""

  def test_serialize_no_report_in_context(self, item):
    serializer = ReportSummaryItemSerializer(item)
    data = serializer.data
    assert data['best_price'] is None
    assert data['average_price'] is None
    assert data['prices'] == {}

  def test_serialize_no_prices(self, item, report):
    serializer = ReportSummaryItemSerializer(
        item, context={
            'report': report,
            'week': 1,
            'year': 2024
        }
    )
    data = serializer.data
    assert data['id'] == item.id
    assert data['name'] == item.name
    assert data['best_price'] is None
    assert data['average_price'] is None
    assert data['prices'] == {str(s.id): None for s in report.store.all()}

  @freeze_time("2024-01-15")
  def test_serialize_with_prices_and_context(self, item, report):
    store1 = report.store.all()[0]
    PriceFactory(
        item=item,
        store=store1,
        amount=decimal.Decimal('10.00'),
        year=2024,
        week=1,
    )
    PriceFactory(
        item=item,
        store=store1,
        amount=decimal.Decimal('12.00'),
        year=2024,
        week=2,
    )

    # Context for week 2
    serializer = ReportSummaryItemSerializer(
        item, context={
            'report': report,
            'week': 2,
            'year': 2024
        }
    )
    data = serializer.data
    assert data['prices'][str(store1.id)] == '12.00'
    assert data['best_price'] == '12.00'

    # Context for week 1
    # Clear cache because @cache is used and context changed (but Item didn't)
    # Actually @cache on method caches based on (self, instance).
    # New serializer instance means new cache.
    serializer2 = ReportSummaryItemSerializer(
        item, context={
            'report': report,
            'week': 1,
            'year': 2024
        }
    )
    data2 = serializer2.data
    assert data2['prices'][str(store1.id)] == '10.00'


@pytest.mark.django_db
class TestReportJsonSerializer:
  """Tests for the ReportJsonSerializer."""

  @freeze_time("2026-02-24 02:04:28")
  def test_serialize_no_time_context(self, report):
    serializer = ReportSummarySerializer(report)
    data = serializer.data
    assert data['id'] == report.id
    assert data['generated_at'] == "Tue, 24 Feb 2026 02:04:28 GMT"

  @freeze_time("2026-02-24 02:04:28")
  def test_serialize(self, report):
    serializer = ReportSummarySerializer(
        report, context={
            'week': 1,
            'year': 2024
        }
    )
    data = serializer.data
    assert data['id'] == report.id
    assert data['name'] == report.name
    assert data['generated_at'] == "Tue, 24 Feb 2026 02:04:28 GMT"
    assert 'stores' in data
    assert 'items' in data
    assert len(data['stores']) == report.store.count()
    assert len(data['items']) == report.item.count()

  def test_serialize_with_prefetching(self, item, report):
    report.item.add(item)
    store1 = report.store.all()[0]
    PriceFactory(
        item=item,
        store=store1,
        amount=decimal.Decimal('15.00'),
        year=2024,
        week=5,
    )

    serializer = ReportSummarySerializer(
        report, context={
            'week': 5,
            'year': 2024
        }
    )
    data = serializer.data

    # Find our item in the data
    item_data = next(i for i in data['items'] if i['id'] == item.id)
    assert item_data['prices'][str(store1.id)] == '15.00'
