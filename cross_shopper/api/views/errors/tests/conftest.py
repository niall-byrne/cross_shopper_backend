"""Test fixtures for the errors API views."""

from typing import Callable, Dict, Optional, Protocol, Union

import pytest
from django.urls import reverse
from django.utils.http import urlencode

URL_BASENAME = "error"

AliasErrorDetailUrl = Callable[[int], str]


class AliasErrorListUrl(Protocol):

  def __call__(
      self,
      query: Optional[Dict[str, Union[str, int]]] = None,
  ) -> str:
    ...


@pytest.fixture
def error_detail_url() -> "AliasErrorDetailUrl":

  def create(pk: int) -> str:
    return reverse(f"{URL_BASENAME}-detail", kwargs={"pk": pk})

  return create


@pytest.fixture
def error_list_url() -> "AliasErrorListUrl":

  def create(query: Optional[Dict[str, Union[str, int]]] = None) -> str:
    url = reverse(f"{URL_BASENAME}-list")
    if query:
      url += "?" + urlencode(query)
    return url

  return create
