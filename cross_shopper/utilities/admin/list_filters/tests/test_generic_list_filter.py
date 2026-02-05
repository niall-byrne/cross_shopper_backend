"""Test the GenericListFilter list filter class."""

from typing import Any, Dict, List, Tuple
from unittest import mock

import pytest
from django.contrib import admin
from utilities.admin.list_filters.generic_list_filter import GenericListFilter


class TestGenericListFilter:

  def test_instantiate__inheritance(
      self,
      generic_list_filter: GenericListFilter,
  ) -> None:
    assert isinstance(generic_list_filter, admin.SimpleListFilter)

  @pytest.mark.parametrize(
      "params", [
          {
              "title": "test_title",
              "parameter_name": "test.parameter",
          },
          {
              "title": "test_title",
              "parameter_name": "test.parameter",
              "is_boolean": True,
              "is_reversed": True,
          },
          {
              "title": "test_title",
              "parameter_name": "test.parameter",
              "is_boolean": False,
              "is_reversed": True,
          },
          {
              "title": "test_title",
              "parameter_name": "test.parameter",
              "is_boolean": False,
              "is_reversed": False,
          },
          {
              "title": "test_title",
              "parameter_name": "test.parameter",
              "is_boolean": True,
              "is_reversed": False,
          },
      ]
  )
  def test_create__with_params__returns_subclass_with_correct_attributes(
      self,
      params: Dict[str, Any],
  ) -> None:
    created = GenericListFilter.create(**params)

    assert issubclass(created, GenericListFilter)
    assert created.title == params['title']
    assert created.parameter_name == params['parameter_name']
    assert created.is_boolean == params.get('is_boolean', False)
    assert created.is_reversed == params.get('is_reversed', False)

  def test_queryset__no_value__returns_original_queryset(
      self,
      generic_list_filter: GenericListFilter,
      mocked_request: mock.Mock,
      mocked_queryset: mock.Mock,
  ) -> None:
    with mock.patch.object(generic_list_filter, 'value', return_value=None):
      result = generic_list_filter.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset

  def test_queryset__has_value__returns_filtered_queryset(
      self,
      generic_list_filter: GenericListFilter,
      mocked_request: mock.Mock,
      mocked_queryset: mock.Mock,
  ) -> None:
    with mock.patch.object(generic_list_filter, 'value', return_value='foo'):
      result = generic_list_filter.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset.filter.return_value
    mocked_queryset.filter.assert_called_once_with(test_param='foo')

  @pytest.mark.parametrize("is_reversed", (True, False))
  def test_lookups__not_boolean__vary_reverse__returns_correct_lookups(
      self,
      generic_list_filter: GenericListFilter,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
      is_reversed: bool,
  ) -> None:
    generic_list_filter.is_boolean = False
    generic_list_filter.is_reversed = is_reversed
    mocked_qs = mocked_model_admin.get_queryset.return_value

    # Reset mock because __init__ already called lookups once
    mocked_qs.values_list.reset_mock()

    mocked_qs.values_list.return_value.distinct.return_value \
      .order_by.return_value = ['a', 'b']

    result = generic_list_filter.lookups(mocked_request, mocked_model_admin)

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
      generic_list_filter: GenericListFilter,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
      is_reversed: bool,
      expected_lookups: List[Tuple[bool, str]],
  ) -> None:
    generic_list_filter.is_boolean = True
    generic_list_filter.is_reversed = is_reversed

    result = generic_list_filter.lookups(mocked_request, mocked_model_admin)

    assert result == expected_lookups
