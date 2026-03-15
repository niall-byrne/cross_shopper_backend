"""Test the ErrorsViewSet create view."""

from typing import TYPE_CHECKING

import pytest
from errors.models import Error
from errors.models.serializers.read_write.error import ErrorSerializerRW
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from rest_framework.test import APIClient
  from .conftest import AliasErrorListUrl


@pytest.mark.django_db
class TestErrorsViewSetCreateNoAuthentication:

  def test_create__forbids_access(
      self,
      unauthenticated_client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializerRW(error)
    create_data = dict(serializer.data)

    res = unauthenticated_client.post(error_list_url(), data=create_data)

    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestErrorsViewSetCreateAuthentication:

  def test_create__existing_object__returns_correct_response(
      self,
      authenticated_client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializerRW(error)
    update_data = dict(serializer.data)

    res = authenticated_client.post(
        error_list_url(),
        data=update_data,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.data == update_data

  def test_create__existing_object__increments_error_count(
      self,
      authenticated_client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializerRW(error)
    update_data = dict(serializer.data)

    authenticated_client.post(
        error_list_url(),
        data=update_data,
    )

    error.refresh_from_db()
    assert error.count == 2

  def test_create__new_object__returns_correct_response(
      self,
      authenticated_client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializerRW(error)
    update_data_without_id = dict(serializer.data)
    update_data_without_id.pop("id")
    error.delete()

    res = authenticated_client.post(
        error_list_url(),
        data=update_data_without_id,
    )
    received_data_without_id = dict(res.data)
    received_data_without_id.pop("id")

    assert res.status_code == status.HTTP_201_CREATED
    assert received_data_without_id == update_data_without_id

  def test_create__new_object__initializes_error_count(
      self,
      authenticated_client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error: "Error",
  ) -> None:
    serializer = ErrorSerializerRW(error)
    create_data_without_id = dict(serializer.data)
    create_data_without_id.pop("id")
    error.delete()

    res = authenticated_client.post(
        error_list_url(),
        data=create_data_without_id,
    )

    error = Error.objects.get(id=res.data['id'])
    assert error.count == 1
