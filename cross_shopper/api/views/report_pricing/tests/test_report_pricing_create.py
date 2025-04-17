"""Test the ReportPricingReadOnlyViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from reports.models import Report
  from rest_framework.test import APIClient
  from .conftest import AliasReportPricingListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportPricingReadOnlyViewSetCreate:
  """Test the ReportPricingReadOnlyViewSet create view."""

  def test_list__forbids_access(
      self,
      client: "APIClient",
      report_pricing_list_url: "AliasReportPricingListUrl",
      report_with_pricing: "Report",
  ) -> None:
    res = client.post(
        report_pricing_list_url(report_with_pricing.pk),
        data={},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN
