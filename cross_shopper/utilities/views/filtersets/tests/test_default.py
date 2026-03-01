"""Tests for the DefaultFilterSet."""

from typing import Type

from utilities.views.filtersets.default import DefaultFilterSet


class TestDefaultFilterSet:
  """Tests for the DefaultFilterSet."""

  def test_init__empty_data__populates_default_values(
      self,
      mock_filterset: Type[DefaultFilterSet],
  ) -> None:
    filter_set = mock_filterset(data={})

    assert filter_set.data['name'] == 'default_name'

  def test_init__provided_data__does_not_overwrite(
      self,
      mock_filterset: Type[DefaultFilterSet],
  ) -> None:
    filter_set = mock_filterset(data={'name': 'provided_name'})

    assert filter_set.data['name'] == 'provided_name'
