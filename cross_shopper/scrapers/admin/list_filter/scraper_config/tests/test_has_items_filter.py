"""Test the HasItemsFilter class."""

from unittest import mock

import pytest
from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)
from scrapers.admin.list_filter.scraper_config.has_items_filter import (
    HasItemsFilter,
)


class TestHasItemsFilter:
  """Test the HasItemsFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(HasItemsFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert HasItemsFilter.title == 'has items'
    assert HasItemsFilter.parameter_name == 'has_item'
    assert HasItemsFilter.is_boolean is True

  def test_queryset__true(
      self,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = HasItemsFilter(
        mocked_request, {HasItemsFilter.parameter_name: 'True'}, HasItemsFilter,
        mock.Mock()
    )
    mocked_queryset = mock.Mock()

    with mock.patch.object(HasItemsFilter, 'value', return_value='True'):
      with mock.patch(
          'items.models.ItemScraperConfig.associations.with_items'
      ) as mocked_with_items:
        result = filter_instance.queryset(mocked_request, mocked_queryset)

    mocked_with_items.assert_called_once_with(mocked_queryset)
    assert result == mocked_with_items.return_value

  def test_queryset__false(
      self,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = HasItemsFilter(
        mocked_request, {HasItemsFilter.parameter_name: 'False'},
        HasItemsFilter, mock.Mock()
    )
    mocked_queryset = mock.Mock()

    with mock.patch.object(HasItemsFilter, 'value', return_value='False'):
      with mock.patch(
          'items.models.ItemScraperConfig.associations.with_no_items'
      ) as mocked_with_no_items:
        result = filter_instance.queryset(mocked_request, mocked_queryset)

    mocked_with_no_items.assert_called_once_with(mocked_queryset)
    assert result == mocked_with_no_items.return_value

  def test_queryset__none(
      self,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = HasItemsFilter(
        mocked_request, {}, HasItemsFilter, mock.Mock()
    )
    mocked_queryset = mock.Mock()

    with mock.patch.object(HasItemsFilter, 'value', return_value=None):
      result = filter_instance.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset
