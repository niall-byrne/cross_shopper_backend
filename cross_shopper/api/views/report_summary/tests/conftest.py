"""Test fixtures for the report_summary API views."""

from typing import Callable, Dict, Optional, Protocol, Union

import pytest
from django.urls import reverse
from django.utils.http import urlencode

REPORT_JSON_URL_BASENAME = "report_summary"

AliasReportJsonDetailUrl = Callable[[int], str]


class AliasReportJsonListUrl(Protocol):

  def __call__(  # noqa: D102
      self,
      query: Optional[Dict[str, Union[int, str]]] = None,
  ) -> str:
    ...


@pytest.fixture
def report_summary_detail_url() -> "AliasReportJsonDetailUrl":

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_JSON_URL_BASENAME}-detail",
        kwargs={"pk": report_pk},
    )

  return create


@pytest.fixture
def report_with_item(report: "Report", item: "Item") -> "Report":
  report.item.add(item)
  return report


@pytest.fixture
def report_summary_list_url() -> "AliasReportJsonListUrl":

  def create(query: Optional[Dict[str, Union[int, str]]] = None) -> str:
    url = reverse(f"{REPORT_JSON_URL_BASENAME}-list")
    if query:
      url += ('?' + urlencode(query))
    return url

  return create
