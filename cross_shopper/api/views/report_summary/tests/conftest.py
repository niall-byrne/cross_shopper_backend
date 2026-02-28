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
      report_pk: int,
      query: Optional[Dict[str, Union[int, str]]] = None,
  ) -> str:
    ...


@pytest.fixture
def report_summary_detail_url() -> "AliasReportJsonDetailUrl":

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_JSON_URL_BASENAME}-detail",
        kwargs={
            "report_pk": report_pk,
            "pk": report_pk,
        },
    )

  return create


@pytest.fixture
def report_summary_list_url() -> "AliasReportJsonListUrl":

  def create(
      report_pk: int,
      query: Optional[Dict[str, Union[int, str]]] = None,
  ) -> str:
    url = reverse(
        f"{REPORT_JSON_URL_BASENAME}-list",
        kwargs={"report_pk": report_pk},
    )
    if query:
      url += ('?' + urlencode(query))
    return url

  return create
