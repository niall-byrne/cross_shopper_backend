"""Tests for the ReportSummaryItemPriceSerializerRO."""

from typing import TYPE_CHECKING

import pytest
from items.models.serializers.read_write.packaging import PackagingSerializerRW
from reports.models.serializers.read_only.report_summary.item import (
    ReportSummaryItemSerializerRO,
)
from reports.models.serializers.read_only.report_summary.item_price import (
    ReportSummaryItemPriceSerializerRO,
)

if TYPE_CHECKING:
  from reports.models.report import Report


@pytest.mark.django_db
class TestReportSummaryItemSerializerRO:

  @pytest.mark.usefixtures(
      "report_summary_mocked_pricing_aggregate_last_52_weeks_manager"
  )
  def test_serialization__specified_item__returns_correct_representation(
      self,
      report_prefetched: "Report",
  ) -> None:
    item = report_prefetched.item.all()[0]

    serializer = ReportSummaryItemSerializerRO(
        item,
        context={"report": report_prefetched},
    )

    assert serializer.data == {
        "id":
            item.pk,
        "name":
            item.name,
        "brand":
            item.brand.name,
        "is_bulk":
            item.is_bulk,
        "is_organic":
            item.is_organic,
        "is_non_gmo":
            item.is_non_gmo,
        "packaging":
            PackagingSerializerRW(item.packaging).data,
        "price":
            ReportSummaryItemPriceSerializerRO(
                item,
                context=serializer.context,
            ).data,
    }
