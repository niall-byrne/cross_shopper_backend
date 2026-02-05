"""Test the base admin list filter."""

from typing import List, Tuple
from unittest import mock

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class TestAdminListFilterBase:
  """Test the AdminListFilterBase class."""

  def test_queryset__no_value__returns_original_queryset(
      self,
      admin_list_filter_base: AdminListFilterBase,
      mocked_request: mock.Mock,
      mocked_queryset: mock.Mock,
  ) -> None:
    with mock.patch.object(admin_list_filter_base, 'value', return_value=None):
      result = admin_list_filter_base.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset

  def test_queryset__has_value__returns_filtered_queryset(
      self,
      admin_list_filter_base: AdminListFilterBase,
      mocked_request: mock.Mock,
      mocked_queryset: mock.Mock,
  ) -> None:
    with mock.patch.object(admin_list_filter_base, 'value', return_value='foo'):
      result = admin_list_filter_base.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset.filter.return_value
    mocked_queryset.filter.assert_called_once_with(test_param='foo')

  @pytest.mark.parametrize("is_reversed", (True, False))
  def test_lookups__not_boolean__vary_reverse__returns_correct_lookups(
      self,
      admin_list_filter_base: AdminListFilterBase,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
      is_reversed: bool,
  ) -> None:
    admin_list_filter_base.is_boolean = False
    admin_list_filter_base.is_reversed = is_reversed
    mocked_qs = mocked_model_admin.get_queryset.return_value

    # Reset mock because __init__ already called lookups once
    mocked_qs.values_list.reset_mock()

    mocked_qs.values_list.return_value.distinct.return_value \
      .order_by.return_value = ['a', 'b']

    result = admin_list_filter_base.lookups(mocked_request, mocked_model_admin)

    assert result == [('a', 'a'), ('b', 'b')]
    mocked_qs.values_list.assert_called_once_with('test_param', flat=True)
    operator = "-" if is_reversed else ""
    mocked_qs.values_list.return_value.distinct.return_value \
      .order_by.assert_called_once_with(f"{operator}test_param")

  @pytest.mark.parametrize(
      "is_reversed,expected_lookups", [
          (True, [(False, "No"), (True, "Yes")]),
          (False, [(True, "Yes"), (False, "No")]),
      ]
  )
  def test_lookups__is_boolean__vary_reverse__returns_correct_lookups(
      self,
      admin_list_filter_base: AdminListFilterBase,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
      is_reversed: bool,
      expected_lookups: List[Tuple[bool, str]],
  ) -> None:
    admin_list_filter_base.is_boolean = True
    admin_list_filter_base.is_reversed = is_reversed

    result = admin_list_filter_base.lookups(mocked_request, mocked_model_admin)

    assert result == expected_lookups
