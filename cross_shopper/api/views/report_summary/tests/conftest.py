"""Test fixtures for the report_summary API views."""
from __future__ import annotations

from typing import Callable, Protocol

import pytest
from django.urls import reverse
from django.utils.http import urlencode

AliasReportSummaryDetailUrl = Callable[[int], str]

REPORT_JSON_URL_BASENAME = "report_summary"


class AliasReportSummaryListUrl(Protocol):

  def __call__(  # noqa: D102
      self,
      query: dict[str, int | str] | None = None,
  ) -> str:
    ...


@pytest.fixture
def report_summary_detail_url() -> AliasReportSummaryDetailUrl:

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_JSON_URL_BASENAME}-detail",
        kwargs={"pk": report_pk},
    )

  return create


@pytest.fixture
def report_summary_list_url() -> AliasReportSummaryListUrl:

  def create(query: dict[str, int | str] | None = None) -> str:
    url = reverse(f"{REPORT_JSON_URL_BASENAME}-list")
    if query:
      url += ("?" + urlencode(query))
    return url

  return create
