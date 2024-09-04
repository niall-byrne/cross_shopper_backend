"""Test fixtures for the utilities app serializer fields."""

from typing import Any

import pytest
from rest_framework import serializers
from utilities.models.serializers.fields import blonde, lowercase, title


@pytest.fixture
def blonde_field_serializer() -> type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = blonde.BlondeCharField(allow_null=True)

  return TestSerializer


@pytest.fixture
def lowercase_field_serializer() -> type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = lowercase.LowerCaseField()

  return TestSerializer


@pytest.fixture
def title_field_serializer() -> type[serializers.Serializer[Any]]:

  class TestSerializer(serializers.Serializer[Any]):
    field = title.TitleField()

  return TestSerializer
