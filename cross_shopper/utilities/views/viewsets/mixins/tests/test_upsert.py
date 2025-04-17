"""Test the UpsertModelMixin class."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from rest_framework import status

if TYPE_CHECKING:
  from unittest import mock

  from rest_framework.test import APIRequestFactory
  from rest_framework.viewsets import ModelViewSet


class TestUpsertModelMixin:

  @pytest.mark.parametrize(
      "scenario", (
          {
              "is_created": False,
              "expected_status_code": status.HTTP_200_OK,
          },
          {
              "is_created": True,
              "expected_status_code": status.HTTP_201_CREATED,
          },
      )
  )
  def test_create__vary_model_created__returns_expected_status_code(
      self,
      api_factory: APIRequestFactory,
      concrete_upsert_view_set: type[ModelViewSet[mock.Mock]],
      mocked_serializer: mock.Mock,
      scenario: dict[str, bool | int],
  ) -> None:
    mocked_serializer.return_value.context.get.return_value = (
        scenario["is_created"]
    )
    request = api_factory.post("/api/url", {"mocked_data": "mocked_data"})
    view = concrete_upsert_view_set.as_view({"post": "create"})

    response = view(request)

    assert response.status_code == scenario["expected_status_code"]
