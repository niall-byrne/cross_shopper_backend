"""Test fixtures for the items app model admins."""

from unittest import mock

import pytest
from items.admin.inlines.price_group import price_group_attribute


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def price_group_attribute_inline(
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> price_group_attribute.PriceGroupAttributeInline:
  return price_group_attribute.PriceGroupAttributeInline(
      parent_model=mocked_model,
      admin_site=mocked_admin_site,
  )
