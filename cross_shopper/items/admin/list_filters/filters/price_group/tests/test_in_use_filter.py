"""Test the InUseFilter admin model list filter."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from items.admin.list_filters.filters.price_group.in_use import (
    InUseFilter,
)
from items.models import PriceGroup
from utilities.admin.list_filters import GenericListFilter

if TYPE_CHECKING:
  from unittest import mock

  from items.models import Item
  from .conftest import AliasInUseFilterCreator


@pytest.mark.django_db
class TestInUseFilter:

  def test_inheritance(self) -> None:
    assert issubclass(InUseFilter, GenericListFilter)

  def test_attributes(self) -> None:
    assert InUseFilter.title == "in use"
    assert InUseFilter.parameter_name == "has_item"
    assert InUseFilter.is_boolean is True

  def test_queryset__true__returns_assigned_groups_only(
      self,
      create_in_user_filter: AliasInUseFilterCreator,
      item: Item,
      price_group: PriceGroup,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = create_in_user_filter(
        {InUseFilter.parameter_name: "True"},
    )

    result = filter_instance.queryset(mocked_request, PriceGroup.objects.all())

    assert list(result) == [item.price_group]
    assert price_group not in list(result)

  def test_queryset__false__returns_unassigned_groups_only(
      self,
      create_in_user_filter: AliasInUseFilterCreator,
      item: Item,
      price_group: PriceGroup,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = create_in_user_filter(
        {InUseFilter.parameter_name: "False"},
    )

    result = filter_instance.queryset(mocked_request, PriceGroup.objects.all())

    assert list(result) == [price_group]
    assert item.price_group not in list(result)

  def test_queryset__none__returns_full_query_set(
      self,
      create_in_user_filter: AliasInUseFilterCreator,
      item: Item,
      price_group: PriceGroup,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = create_in_user_filter(
        {InUseFilter.parameter_name: "None"},
    )

    result = filter_instance.queryset(mocked_request, PriceGroup.objects.all())

    assert list(result) == list(PriceGroup.objects.all())
