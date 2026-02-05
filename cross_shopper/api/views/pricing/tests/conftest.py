"""Test fixtures for the pricing API views."""
from __future__ import annotations

from typing import Callable, Protocol

import pytest
from django.urls import reverse
from django.utils.http import urlencode

URL_BASENAME = "price"

AliasPricingDetailUrl = Callable[[int], str]


class AliasPricingListUrl(Protocol):

  def __call__(
      self,
      query: dict[str, int] | None = None,
  ) -> str:
    ...


@pytest.fixture
def pricing_detail_url() -> AliasPricingDetailUrl:

  def create(pk: int) -> str:
    return reverse(f"{URL_BASENAME}-detail", kwargs={"pk": pk})

  return create


@pytest.fixture
def pricing_list_url() -> AliasPricingListUrl:

  def create(query: dict[str, int] | None = None) -> str:
    url = reverse(f"{URL_BASENAME}-list")
    if query:
      url += ("?" + urlencode(query))
    return url

  return create
