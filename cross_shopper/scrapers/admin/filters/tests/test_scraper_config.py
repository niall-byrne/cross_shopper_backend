"""Test the scraper config model list filters."""

from unittest import mock

import pytest
from scrapers.admin.filters.scraper_config import (
    HasItemsFilter,
    ScraperFilter,
)
from utilities.admin.filters.bases.base_admin_list_filter import (
    AdminListFilterBase,
)


class TestScraperFilter:
  """Test the ScraperFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(ScraperFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert ScraperFilter.title == 'scraper name'
    assert ScraperFilter.parameter_name == 'scraper__name'


class TestHasItemsFilter:
  """Test the HasItemsFilter class."""

  def test_inheritance(self) -> None:
    assert issubclass(HasItemsFilter, AdminListFilterBase)

  def test_attributes(self) -> None:
    assert HasItemsFilter.title == 'has items'
    assert HasItemsFilter.parameter_name == 'has_item'
    assert HasItemsFilter.is_boolean is True

  def test_queryset__no_value__returns_queryset(self) -> None:
    mocked_queryset = mock.Mock()
    mocked_request = mock.Mock()
    instance = HasItemsFilter(
        request=mocked_request,
        params={},
        model=mock.Mock(),
        model_admin=mock.Mock(),
    )

    result = instance.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset

  @mock.patch("scrapers.admin.filters.scraper_config.ItemScraperConfig")
  def test_queryset__true__calls_with_items(
      self, mocked_model: mock.Mock
  ) -> None:
    mocked_queryset = mock.Mock()
    mocked_request = mock.Mock()
    instance = HasItemsFilter(
        request=mocked_request,
        params={'has_item': 'True'},
        model=mock.Mock(),
        model_admin=mock.Mock(),
    )

    result = instance.queryset(mocked_request, mocked_queryset)

    mocked_model.associations.with_items.assert_called_once_with(
        mocked_queryset
    )
    assert result == mocked_model.associations.with_items.return_value

  @mock.patch("scrapers.admin.filters.scraper_config.ItemScraperConfig")
  def test_queryset__false__calls_with_no_items(
      self, mocked_model: mock.Mock
  ) -> None:
    mocked_queryset = mock.Mock()
    mocked_request = mock.Mock()
    instance = HasItemsFilter(
        request=mocked_request,
        params={'has_item': 'False'},
        model=mock.Mock(),
        model_admin=mock.Mock(),
    )

    result = instance.queryset(mocked_request, mocked_queryset)

    mocked_model.associations.with_no_items.assert_called_once_with(
        mocked_queryset
    )
    assert result == mocked_model.associations.with_no_items.return_value
