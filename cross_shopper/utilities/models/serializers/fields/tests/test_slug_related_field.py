"""Tests for the CreatableSlugRelatedField."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.relations import SlugRelatedField
from utilities.models.serializers.fields.mixins.peroxide import (
    PeroxideFieldMixin,
)
from utilities.models.serializers.fields.slug_related_field import (
    CreatableSlugRelatedField,
)

if TYPE_CHECKING:
  from unittest import mock

  from rest_framework import serializers


class TestSerializerContextField:

  scenarios = pytest.mark.parametrize(
      "data_scenario",
      (
          {
              "field": "case_sensitive",
              "lookup": "exact",
              "model": "mocked_model",
              "slug_field": "mocked_slug_field",
              "related_model": "mocked_related_model",
              "related_field": "mocked_slug_field",
          },
          {
              "field": "case_insensitive",
              "lookup": "iexact",
              "model": "mocked_model_alternate",
              "slug_field": "mocked_slug_field_alternate",
              "related_model": "mocked_related_model_alternate",
              "related_field": "mocked_slug_field_alternate",
          },
          {
              "field": "case_sensitive",
              "lookup": "exact",
              "model": "mocked_model",
              "slug_field": "mocked_slug_field",
              "related_model": "mocked_related_model",
              "related_field": "mocked_slug_field",
          },
      ),
  )

  def test_instantiate__inheritance(self) -> None:
    assert issubclass(CreatableSlugRelatedField, PeroxideFieldMixin)
    assert issubclass(CreatableSlugRelatedField, SlugRelatedField)

  @scenarios
  def test_deserialize__vary_field__returns_correct_model_instances(
      self,
      creatable_slug_related_field_serializer: type[serializers.Serializer[Any]
                                                   ],
      data_scenario: dict[str, str],
      request: pytest.FixtureRequest,
  ) -> None:
    model_mock = request.getfixturevalue(data_scenario["model"])
    slug_field_mock = request.getfixturevalue(data_scenario["slug_field"])

    serializer = creatable_slug_related_field_serializer(
        data={
            data_scenario["field"]: "any value",
        }
    )
    serializer.is_valid(raise_exception=True)

    assert serializer.data[data_scenario["field"]] == getattr(
        model_mock,
        slug_field_mock,
    )

  @scenarios
  def test_deserialize__sanitizes_input_data(
      self,
      creatable_slug_related_field_serializer: type[serializers.Serializer[Any]
                                                   ],
      mocked_input_value: str,
      mocked_sanitize: mock.Mock,
      data_scenario: dict[str, str],
  ) -> None:
    serializer = creatable_slug_related_field_serializer(
        data={
            data_scenario["field"]: mocked_input_value,
        }
    )
    serializer.is_valid(raise_exception=True)

    mocked_sanitize.assert_called_once_with(mocked_input_value)

  @scenarios
  def test_deserialize__existing__gets_model_with_sanitized_data_and_lookup(
      self,
      creatable_slug_related_field_serializer: type[serializers.Serializer[Any]
                                                   ],
      mocked_input_value: str,
      mocked_sanitize: mock.Mock,
      data_scenario: dict[str, str],
      request: pytest.FixtureRequest,
  ) -> None:
    rel_model_mock = request.getfixturevalue(data_scenario["related_model"])
    rel_model_field = request.getfixturevalue(data_scenario["related_field"])
    rel_model_lookup = data_scenario["lookup"]

    serializer = creatable_slug_related_field_serializer(
        data={
            data_scenario["field"]: mocked_input_value,
        }
    )
    serializer.is_valid(raise_exception=True)

    rel_model_mock.get.assert_called_once_with(
        **{
            f"{rel_model_field}__{rel_model_lookup}":
                mocked_sanitize.return_value,
        }
    )

  @scenarios
  def test_deserialize__non_existing__creates_model_with_sanitized_data(
      self,
      creatable_slug_related_field_serializer: type[serializers.Serializer[Any]
                                                   ],
      mocked_input_value: str,
      mocked_sanitize: mock.Mock,
      data_scenario: dict[str, str],
      request: pytest.FixtureRequest,
  ) -> None:
    rel_model_mock = request.getfixturevalue(data_scenario["related_model"])
    rel_model_field = request.getfixturevalue(data_scenario["related_field"])
    rel_model_mock.get.side_effect = ObjectDoesNotExist

    serializer = creatable_slug_related_field_serializer(
        data={
            data_scenario["field"]: mocked_input_value,
        }
    )
    serializer.is_valid(raise_exception=True)

    rel_model_mock.create.assert_called_once_with(
        **{
            f"{rel_model_field}": mocked_sanitize.return_value,
        }
    )
