"""Tests for the ReportSummaryItemPriceSerializer."""

import pytest
from items.models import Item
from ..item_price import ReportSummaryItemPriceSerializer


@pytest.mark.django_db
class TestReportSummaryItemPriceSerializer:
  """Tests for the ReportSummaryItemPriceSerializer."""

  def test_serialization__specified_item__correct_representation(
      self,
      item: Item,
  ) -> None:
    serializer = ReportSummaryItemPriceSerializer(item)

    assert serializer.data == {
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
    }
