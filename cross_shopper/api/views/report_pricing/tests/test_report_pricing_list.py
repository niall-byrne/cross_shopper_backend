"""Test the ReportPricingReadOnlyViewSet list view."""

from typing import TYPE_CHECKING

import pytest
from reports.models.serializers.report_pricing import ReportPricingSerializer
from rest_framework import status
from rest_framework.test import APIClient
from .conftest import AliasReportPricingListUrl

if TYPE_CHECKING:  # no cover
  from reports.models import Report


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportPricingViewSetList:
  """Test the ReportPricingReadOnlyViewSet list view."""

  def test_list__returns_correct_response(
      self,
      client: APIClient,
      report_pricing_list_url: AliasReportPricingListUrl,
      report_with_pricing: "Report",
  ) -> None:
    serializer = ReportPricingSerializer(
        report_with_pricing.item,
        context={"report": report_with_pricing},
        many=True,
    )

    res = client.get(report_pricing_list_url(report_with_pricing.id))

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
