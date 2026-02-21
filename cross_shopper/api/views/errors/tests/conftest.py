"""Test fixtures for the errors API views."""
from __future__ import annotations

from typing import Callable, Protocol

import pytest
from django.urls import reverse
from django.utils.http import urlencode

URL_BASENAME = "error"

AliasErrorDetailUrl = Callable[[int], str]


class AliasErrorListUrl(Protocol):

  def __call__(
      self,
      query: dict[str, str | int] | None = None,
  ) -> str:
    ...


@pytest.fixture
def error_detail_url() -> AliasErrorDetailUrl:

  def create(pk: int) -> str:
    return reverse(f"{URL_BASENAME}-detail", kwargs={"pk": pk})

  return create


@pytest.fixture
def error_list_url() -> AliasErrorListUrl:

  def create(query: dict[str, str | int] | None = None) -> str:
    url = reverse(f"{URL_BASENAME}-list")
    if query:
      url += "?" + urlencode(query)
    return url

  return create
