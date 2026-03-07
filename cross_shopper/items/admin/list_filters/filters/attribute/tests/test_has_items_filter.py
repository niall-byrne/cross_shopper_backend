"""Test the HasItemsFilter admin model list filter."""

from unittest import mock

from items.admin.list_filters.filters.attribute.has_items import (
    HasItemsFilter,
)
from utilities.admin.list_filters import GenericListFilter


class TestHasItemsFilter:

  def test_inheritance(self) -> None:
    assert issubclass(HasItemsFilter, GenericListFilter)

  def test_attributes(self) -> None:
    assert HasItemsFilter.title == "has items"
    assert HasItemsFilter.parameter_name == "has_item"
    assert HasItemsFilter.is_boolean is True

  def test_queryset__true(
      self,
      mocked_model: mock.Mock,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = HasItemsFilter(
        mocked_request,
        {HasItemsFilter.parameter_name: "True"},
        mocked_model,
        mocked_model_admin,
    )
    mocked_queryset = mock.Mock()

    with mock.patch.object(HasItemsFilter, "value", return_value="True"):
      with mock.patch(
          "items.models.ItemAttribute.associations.with_items"
      ) as mocked_with_items:
        result = filter_instance.queryset(mocked_request, mocked_queryset)

    mocked_with_items.assert_called_once_with(mocked_queryset)
    assert result == mocked_with_items.return_value

  def test_queryset__false(
      self,
      mocked_model: mock.Mock,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = HasItemsFilter(
        mocked_request,
        {HasItemsFilter.parameter_name: "False"},
        mocked_model,
        mocked_model_admin,
    )
    mocked_queryset = mock.Mock()

    with mock.patch.object(HasItemsFilter, "value", return_value="False"):
      with mock.patch(
          "items.models.ItemAttribute.associations.with_no_items"
      ) as mocked_with_no_items:
        result = filter_instance.queryset(mocked_request, mocked_queryset)

    mocked_with_no_items.assert_called_once_with(mocked_queryset)
    assert result == mocked_with_no_items.return_value

  def test_queryset__none(
      self,
      mocked_model: mock.Mock,
      mocked_model_admin: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    filter_instance = HasItemsFilter(
        mocked_request,
        {},
        mocked_model,
        mocked_model_admin,
    )
    mocked_queryset = mock.Mock()

    with mock.patch.object(HasItemsFilter, "value", return_value=None):
      result = filter_instance.queryset(mocked_request, mocked_queryset)

    assert result == mocked_queryset
