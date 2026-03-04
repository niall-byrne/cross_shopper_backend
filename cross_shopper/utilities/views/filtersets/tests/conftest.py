"""Test fixtures for the utilities app filtersets."""

from typing import Type

import pytest
from django.db import models
from django_filters import rest_framework as filters
from utilities.views.filtersets.default import DefaultFilterSet


class MockModel(models.Model):  # noqa: DJ008
  """A mock model for testing."""

  name = models.CharField(max_length=100)

  class Meta:
    app_label = 'utilities'
    managed = False


@pytest.fixture
def mocked_filterset() -> Type[DefaultFilterSet]:

  class MockFilterSet(DefaultFilterSet):
    """A mock filterset for testing."""

    name = filters.CharFilter(field_name='name')

    class Meta:
      model = MockModel
      fields = ['name']

    def default_name(self) -> str:
      """Return the default name."""
      return 'default_name'

  return MockFilterSet
