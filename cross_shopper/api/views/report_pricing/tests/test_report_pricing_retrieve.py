"""Test the ReportPricingReadOnlyViewSet retrieve view."""

from typing import TYPE_CHECKING, cast

import pytest
from reports.models.serializers.report_pricing import ReportPricingSerializer
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasReportPricingDetailUrl

if TYPE_CHECKING:  # no cover
  from items.models import Item
  from reports.models import Report


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportPricingViewSetRetrieve:
  """Test the ReportPricingReadOnlyViewSet retrieve view."""

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      report_pricing_detail_url: AliasReportPricingDetailUrl,
      report_with_pricing: "Report",
  ) -> None:
    serializer = ReportPricingSerializer(
        report_with_pricing.item.first(),
        context={"report": report_with_pricing},
    )

    res = client.get(
        report_pricing_detail_url(
            report_with_pricing.id,
            cast("Item", report_with_pricing.item.first()).id,
        )
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
