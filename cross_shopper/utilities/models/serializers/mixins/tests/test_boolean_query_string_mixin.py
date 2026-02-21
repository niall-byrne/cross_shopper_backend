"""Test the BooleanQueryParamMixin class."""

from unittest import mock

from utilities.models.serializers.mixins.boolean_query_string_mixin import (
    BooleanQueryParamMixin,
)
from .conftest import AliasCreateMockedRequest


class TestBooleanQueryParamMixin:

  def test_with_a_request_context__returns_none(
      self,
      mocked_model: mock.Mock,
      serializer_with_boolean_query_string: BooleanQueryParamMixin,
  ) -> None:
    serializer = BooleanQueryParamMixin(mocked_model)

    assert serializer.get_boolean_query_param("boolean") is None

  def test_with_a_missing_query_param__returns_none(
      self,
      create_mocked_request: AliasCreateMockedRequest,
      mocked_model: mock.Mock,
      serializer_with_boolean_query_string: BooleanQueryParamMixin,
  ) -> None:
    mocked_request = create_mocked_request({})
    serializer = BooleanQueryParamMixin(
        mocked_model, context={'request': mocked_request}
    )

    assert serializer.get_boolean_query_param("boolean") is None

  def test_with_a_non_boolean_query_param__returns_none(
      self,
      create_mocked_request: AliasCreateMockedRequest,
      mocked_model: mock.Mock,
      serializer_with_boolean_query_string: BooleanQueryParamMixin,
  ) -> None:
    mocked_request = create_mocked_request({"boolean": "invalid value"})
    serializer = BooleanQueryParamMixin(
        mocked_model, context={'request': mocked_request}
    )

    assert serializer.get_boolean_query_param("boolean") is None

  def test_with_a_true_query_param__returns_true(
      self,
      create_mocked_request: AliasCreateMockedRequest,
      mocked_model: mock.Mock,
      serializer_with_boolean_query_string: BooleanQueryParamMixin,
  ) -> None:
    mocked_request = create_mocked_request({"boolean": "true"})
    serializer = BooleanQueryParamMixin(
        mocked_model, context={'request': mocked_request}
    )

    assert serializer.get_boolean_query_param("boolean") is True

  def test_with_a_false_query_param__returns_false(
      self,
      create_mocked_request: AliasCreateMockedRequest,
      mocked_model: mock.Mock,
      serializer_with_boolean_query_string: BooleanQueryParamMixin,
  ) -> None:
    mocked_request = create_mocked_request({"boolean": "false"})
    serializer = BooleanQueryParamMixin(
        mocked_model, context={'request': mocked_request}
    )

    assert serializer.get_boolean_query_param("boolean") is False
