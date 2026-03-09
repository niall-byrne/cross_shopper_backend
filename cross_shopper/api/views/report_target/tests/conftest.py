"""Test fixtures for the report targets API views."""
from __future__ import annotations

from typing import Callable, Protocol

import pytest
from django.urls import reverse
from django.utils.http import urlencode

REPORT_URL_BASENAME = "report_target"

AliasTargetReportDetailUrl = Callable[[int], str]


class AliasReportTargetListUrl(Protocol):

  def __call__(  # noqa: D102
      self,
      query: dict[str, int | str] | None = None,
  ) -> str:
    ...


@pytest.fixture
def report_target_detail_url() -> AliasTargetReportDetailUrl:

  def create(report_pk: int) -> str:
    return reverse(
        f"{REPORT_URL_BASENAME}-detail",
        kwargs={"pk": report_pk},
    )

  return create


@pytest.fixture
def report_target_list_url() -> AliasReportTargetListUrl:

  def create(query: dict[str, int | str] | None = None) -> str:
    url = reverse(f"{REPORT_URL_BASENAME}-list")
    if query:
      url += ("?" + urlencode(query))
    return url

  return create
