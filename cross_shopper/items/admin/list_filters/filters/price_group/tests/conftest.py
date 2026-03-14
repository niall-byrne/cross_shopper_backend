"""Test fixtures for the PriceGroup model admin list filters."""

from typing import TYPE_CHECKING
from unittest import mock

import pytest
from items.admin.list_filters.filters.price_group import in_use

if TYPE_CHECKING:  # no cover
  from typing import Callable, Dict

  AliasInUseFilterCreator = Callable[[Dict[str, str]], in_use.InUseFilter]


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model_admin() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_request() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def create_in_user_filter(
    mocked_model: mock.Mock,
    mocked_model_admin: mock.Mock,
    mocked_request: mock.Mock,
) -> "AliasInUseFilterCreator":

  def create(params: "Dict[str, str]") -> in_use.InUseFilter:
    return in_use.InUseFilter(
        mocked_request,
        params,
        mocked_model,
        mocked_model_admin,
    )

  return create
