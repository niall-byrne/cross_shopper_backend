"""Test fixtures for the report_pricing API views."""
from __future__ import annotations

from typing import Callable

import pytest
from django.urls import reverse

REPORT_URL_BASENAME = "report"
REPORT_PRICING_URL_BASENAME = "report_pricing"

AliasReportPricingDetailUrl = Callable[[int, int], str]
AliasReportPricingListUrl = Callable[[int], str]


@pytest.fixture
def report_pricing_detail_url() -> AliasReportPricingDetailUrl:

  def create(report_pk: int, item_pk: int) -> str:
    return reverse(
        f"{REPORT_PRICING_URL_BASENAME}-detail",
        kwargs={
            "report_pk": report_pk,
            "pk": item_pk
        },
    )

  return create


@pytest.fixture
def report_pricing_list_url() -> AliasReportPricingListUrl:

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_PRICING_URL_BASENAME}-list",
        kwargs={"report_pk": report_pk},
    )

  return create
