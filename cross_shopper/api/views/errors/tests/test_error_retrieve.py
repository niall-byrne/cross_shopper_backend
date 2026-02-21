"""Test for the ErrorsViewSet retrieve view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from errors.models.serializers.error import ErrorSerializer
from rest_framework import status

if TYPE_CHECKING:
  from errors.models import Error
  from rest_framework.test import APIClient
  from .conftest import AliasErrorDetailUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestErrorsViewSetRetrieve:

  def test_retrieve__returns_correct_response(
      self,
      client: APIClient,
      error: Error,
      error_detail_url: AliasErrorDetailUrl,
  ) -> None:
    res = client.get(error_detail_url(error.pk))
    serializer = ErrorSerializer(error)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
