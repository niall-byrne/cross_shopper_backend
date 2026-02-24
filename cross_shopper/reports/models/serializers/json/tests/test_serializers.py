"""Tests for the JSON serializers."""

import decimal
import pytest
from freezegun import freeze_time
from reports.models.serializers.json.store import StoreJsonSerializer
from reports.models.serializers.json.item import ItemJsonSerializer
from reports.models.serializers.json.report import ReportJsonSerializer
from pricing.models.factories.pricing import PriceFactory

@pytest.mark.django_db
class TestStoreJsonSerializer:
  """Tests for the StoreJsonSerializer."""

  def test_serialize(self, store):
    serializer = StoreJsonSerializer(store)
    assert serializer.data == {
        'id': store.id,
        'franchise_name': store.franchise.name,
    }

@pytest.mark.django_db
class TestItemJsonSerializer:
  """Tests for the ItemJsonSerializer."""

  def test_serialize_no_report_in_context(self, item):
    serializer = ItemJsonSerializer(item)
    data = serializer.data
    assert data['best_price'] is None
    assert data['average_price'] is None
    assert data['prices'] == {}

  def test_serialize_no_prices(self, item, report):
    serializer = ItemJsonSerializer(item, context={'report': report})
    data = serializer.data
    assert data['id'] == item.id
    assert data['name'] == item.name
    assert data['best_price'] is None
    assert data['average_price'] is None
    assert data['prices'] == {str(s.id): None for s in report.store.all()}

  @freeze_time("2024-01-15")
  def test_serialize_with_prices(self, item, report):
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

    serializer = ItemJsonSerializer(item, context={'report': report})
    data = serializer.data
    assert data['prices'][str(store1.id)] == '12.00'
    assert data['best_price'] == '12.00'
    assert data['average_price'] == '11.00'

@pytest.mark.django_db
class TestReportJsonSerializer:
  """Tests for the ReportJsonSerializer."""

  @freeze_time("2026-02-24 02:04:28")
  def test_serialize(self, report):
    serializer = ReportJsonSerializer(report)
    data = serializer.data
    assert data['id'] == report.id
    assert data['name'] == report.name
    assert data['generated_at'] == "Tue, 24 Feb 2026 02:04:28 GMT"
    assert 'stores' in data
    assert 'items' in data
    assert len(data['stores']) == report.store.count()
    assert len(data['items']) == report.item.count()
