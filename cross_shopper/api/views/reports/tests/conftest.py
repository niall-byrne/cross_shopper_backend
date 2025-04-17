"""Test fixtures for the reports API views."""

from typing import Callable, Dict, Optional, Protocol, Union

import pytest
from django.urls import reverse
from django.utils.http import urlencode

REPORT_URL_BASENAME = "report"

AliasReportDetailUrl = Callable[[int], str]


class AliasReportListUrl(Protocol):

  def __call__(  # noqa: D102
      self,
      query: Optional[Dict[str, Union[int, str]]] = None,
  ) -> str:
    ...


@pytest.fixture
def report_detail_url() -> "AliasReportDetailUrl":

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_URL_BASENAME}-detail",
        kwargs={"pk": report_pk},
    )

  return create


@pytest.fixture
def report_list_url() -> "AliasReportListUrl":

  def create(query: Optional[Dict[str, Union[int, str]]] = None) -> str:
    url = reverse(f"{REPORT_URL_BASENAME}-list")
    if query:
      url += ('?' + urlencode(query))
    return url

  return create
