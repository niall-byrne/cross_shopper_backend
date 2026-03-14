"""Tests fixtures for the items models admin mixins."""

from typing import Type
from unittest import mock

import pytest
from django.contrib import admin
from items.admin.mixins import price_group_members


@pytest.fixture
def mocked_admin_site() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def concrete_price_group_members_admin(
) -> Type[price_group_members.PriceGroupMembersAdminMixin]:

  class ConcretePriceGroupMemberAdmin(
      price_group_members.PriceGroupMembersAdminMixin,
      admin.ModelAdmin[mock.Mock],
  ):
    pass

  return ConcretePriceGroupMemberAdmin


@pytest.fixture
def price_group_members_admin(
    concrete_price_group_members_admin: Type[admin.ModelAdmin[mock.Mock]],
    mocked_admin_site: mock.Mock,
    mocked_model: mock.Mock,
) -> admin.ModelAdmin[mock.Mock]:
  return concrete_price_group_members_admin(
      model=mocked_model,
      admin_site=mocked_admin_site,
  )
