"""Tests for the DefaultFilterSet."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # no cover
  from typing import Type

  from utilities.views.filtersets.default import DefaultFilterSet


class TestDefaultFilterSet:

  def test_initialize__no_data__populates_default_values(
      self,
      mocked_filterset: "Type[DefaultFilterSet]",
  ) -> None:
    filter_set = mocked_filterset(data=None)

    assert filter_set.data is not None
    assert filter_set.data["name"] == "default_name"

  def test_initialize__empty_data__populates_default_values(
      self,
      mocked_filterset: "Type[DefaultFilterSet]",
  ) -> None:
    filter_set = mocked_filterset(data={})

    assert filter_set.data is not None
    assert filter_set.data["name"] == "default_name"

  def test_initialize__provided_data__does_not_overwrite(
      self,
      mocked_filterset: "Type[DefaultFilterSet]",
  ) -> None:
    filter_set = mocked_filterset(data={"name": "provided_name"})

    assert filter_set.data is not None
    assert filter_set.data["name"] == "provided_name"
