"""Test the ErrorsViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from errors.models.serializers.error import ErrorSerializer
from rest_framework import status

if TYPE_CHECKING:  # nocover
  from errors.models import Error
  from rest_framework.test import APIClient
  from .conftest import AliasErrorDetailUrl


@pytest.mark.django_db
class TestErrorsViewSetUpdateNoAuthentication:
  """Test the ErrorsViewSet update view without authentication."""

  def test_update__forbids_access(
      self,
      unauthenticated_client: "APIClient",
      error_detail_url: "AliasErrorDetailUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializer(error)
    data = dict(serializer.data)

    res = unauthenticated_client.put(error_detail_url(error.id), data=data)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestErrorsViewSetAuthentication:
  """Test the ErrorsViewSet update view with authentication."""

  def test_update__existing_object__returns_correct_response(
      self,
      authenticated_client: "APIClient",
      error_detail_url: "AliasErrorDetailUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializer(error)
    update_data = dict(serializer.data)

    res = authenticated_client.put(
        error_detail_url(error.id),
        data=update_data,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == update_data

  def test_update__existing_object__does_not_increment_error_count(
      self,
      authenticated_client: "APIClient",
      error_detail_url: "AliasErrorDetailUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializer(error)
    update_data = dict(serializer.data)

    authenticated_client.put(
        error_detail_url(error.id),
        data=update_data,
    )

    error.refresh_from_db()
    assert error.count == 1
