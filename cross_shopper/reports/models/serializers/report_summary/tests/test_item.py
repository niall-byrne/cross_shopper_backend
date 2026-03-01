"""Tests for the ReportSummaryItemSerializer."""

import pytest
from items.models import Item
from items.models.serializers.packaging import PackagingSerializer
from ..item import ReportSummaryItemSerializer


@pytest.mark.django_db
class TestReportSummaryItemSerializer:
  """Tests for the ReportSummaryItemSerializer."""

  def test_serialization(self, item: Item) -> None:
    """Test that the serializer correctly represents an item."""
    serializer = ReportSummaryItemSerializer(item)
    assert serializer.data == {
        "id": item.id,
        "name": item.name,
        "brand": item.brand.name,
        "is_bulk": item.is_bulk,
        "is_organic": item.is_organic,
        "is_non_gmo": item.is_non_gmo,
        "packaging": PackagingSerializer(item.packaging).data,
        "price": {
            "last_52_weeks": {
                "average": None,
                "high": None,
                "low": None,
            },
            "selected_week": {
                "average": None,
                "best": None,
                "per_store": {},
            },
        },
    }

  def test_serialization__with_context(self, item: Item) -> None:
    """Test that context is passed down through the serializer."""
    serializer = ReportSummaryItemSerializer(item, context={'some': 'context'})
    assert serializer.context['some'] == 'context'
