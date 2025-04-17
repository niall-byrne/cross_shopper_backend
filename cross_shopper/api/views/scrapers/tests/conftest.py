"""Test fixtures for the scrapers API views."""

from typing import Callable, Dict, Optional, Protocol, Union

import pytest
from django.urls import reverse
from django.utils.http import urlencode

REPORT_URL_BASENAME = "scraper"

AliasScraperDetailUrl = Callable[[int], str]


class AliasScraperListUrl(Protocol):
  def __call__(  # noqa: D102
    self,
    query: Optional[Dict[str, Union[int, str]]] = None,
  ) -> str:
    ...


@pytest.fixture
def scraper_detail_url() -> "AliasScraperDetailUrl":

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_URL_BASENAME}-detail",
        kwargs={"pk": report_pk},
    )

  return create


@pytest.fixture
def scraper_list_url() -> "AliasScraperListUrl":

  def create(query: Optional[Dict[str, Union[int, str]]] = None) -> str:
    url = reverse(f"{REPORT_URL_BASENAME}-list")
    if query:
      url += "?" + urlencode(query)
    return url

  return create
