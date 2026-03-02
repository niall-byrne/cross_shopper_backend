"""Test the ErrorsViewSet modify view."""
from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from errors.models.serializers.read_write.error import ErrorSerializerRW
from rest_framework import status

if TYPE_CHECKING:
  from errors.models import Error
  from rest_framework.test import APIClient
  from .conftest import AliasErrorDetailUrl


@pytest.mark.django_db
class TestErrorsViewSetModifyNoAuthentication:

  def test_put__forbids_access(
      self,
      unauthenticated_client: APIClient,
      error_detail_url: AliasErrorDetailUrl,
      error: Error,
  ) -> None:
    serializer = ErrorSerializerRW(error)

    res = unauthenticated_client.put(
        error_detail_url(error.pk),
        data=serializer.data,
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestErrorsViewSetModifyAuthentication:

  def test_put__returns_correct_response(
      self,
      authenticated_client: APIClient,
      error_detail_url: AliasErrorDetailUrl,
      error: Error,
  ) -> None:
    serializer = ErrorSerializerRW(error)

    res = authenticated_client.put(
        error_detail_url(error.pk),
        data=serializer.data,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
