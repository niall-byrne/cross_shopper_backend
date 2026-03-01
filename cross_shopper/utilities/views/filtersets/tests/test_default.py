"""Tests for the DefaultFilterSet."""

from django.db import models
from django_filters import rest_framework as filters
from ..default import DefaultFilterSet


class MockModel(models.Model):
  """A mock model for testing."""
  name = models.CharField(max_length=100)

  class Meta:
    app_label = 'utilities'
    managed = False


class MockFilterSet(DefaultFilterSet):
  """A mock filterset for testing."""
  name = filters.CharFilter(field_name='name')

  class Meta:
    model = MockModel
    fields = ['name']

  def default_name(self) -> str:
    """Return the default name."""
    return 'default_name'


class TestDefaultFilterSet:
  """Tests for the DefaultFilterSet."""

  def test_init__populates_default_values(self) -> None:
    """Test that default values are correctly populated in self.data."""
    filter_set = MockFilterSet(data={})
    assert filter_set.data['name'] == 'default_name'

  def test_init__does_not_overwrite_provided_values(self) -> None:
    """Test that provided values are not overwritten by defaults."""
    filter_set = MockFilterSet(data={'name': 'provided_name'})
    assert filter_set.data['name'] == 'provided_name'
