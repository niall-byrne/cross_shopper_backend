"""Tests for the DefaultFilterSet."""

from typing import Type

from ...filtersets.default import DefaultFilterSet


class TestDefaultFilterSet:
  """Tests for the DefaultFilterSet."""

  def test_init__populates_default_values(
      self,
      mock_filterset: Type[DefaultFilterSet],
  ) -> None:
    """Test that default values are correctly populated in self.data."""
    filter_set = mock_filterset(data={})
    assert filter_set.data['name'] == 'default_name'

  def test_init__does_not_overwrite_provided_values(
      self,
      mock_filterset: Type[DefaultFilterSet],
  ) -> None:
    """Test that provided values are not overwritten by defaults."""
    filter_set = mock_filterset(data={'name': 'provided_name'})
    assert filter_set.data['name'] == 'provided_name'
