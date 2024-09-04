"""Test fixtures for the utilities app serializer fields."""

from typing import Type

import pytest
from rest_framework import serializers
from utilities.models.serializers.fields import blonde, lowercase, title


@pytest.fixture
def blonde_field_serializer() -> Type[serializers.Serializer]:

  class TestSerializer(serializers.Serializer):
    field = blonde.BlondeCharField(allow_null=True)

  return TestSerializer


@pytest.fixture
def lowercase_field_serializer() -> Type[serializers.Serializer]:

  class TestSerializer(serializers.Serializer):
    field = lowercase.LowerCaseField()

  return TestSerializer


@pytest.fixture
def title_field_serializer() -> Type[serializers.Serializer]:

  class TestSerializer(serializers.Serializer):
    field = title.TitleField()

  return TestSerializer
