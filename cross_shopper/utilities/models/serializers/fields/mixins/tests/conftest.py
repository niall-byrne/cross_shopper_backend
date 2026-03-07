"""Test fixtures for the utilities app serializer field mixins."""

import pytest
from utilities.models.serializers.fields.mixins import peroxide


@pytest.fixture
def peroxide_field_mixin() -> peroxide.PeroxideFieldMixin:
  return peroxide.PeroxideFieldMixin()
