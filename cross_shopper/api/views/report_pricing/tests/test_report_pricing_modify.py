"""Test the ReportPricingReadOnlyViewSet modify view."""
from __future__ import annotations

from typing import TYPE_CHECKING, cast

import pytest
from rest_framework import status

if TYPE_CHECKING:
  from items.models import Item
  from reports.models import Report
  from rest_framework.test import APIClient
  from .conftest import AliasReportPricingDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestReportPricingReadOnlyViewSetModify:

  def test_modify__forbids_access(
      self,
      client: APIClient,
      report_pricing_detail_url: AliasReportPricingDetailUrl,
      report_with_pricing: Report,
  ) -> None:
    res = client.put(
        report_pricing_detail_url(
            report_with_pricing.pk,
            cast("Item", report_with_pricing.item.first()).pk,
        ),
        data={},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN
