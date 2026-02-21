"""Tests for the ErrorsViewSet list view."""

from typing import TYPE_CHECKING, cast

import pytest
from errors.models import Error
from errors.models.serializers.error import ErrorSerializer
from rest_framework import status

if TYPE_CHECKING:  # no cover
  from django.db.models import QuerySet
  from rest_framework.test import APIClient
  from .conftest import AliasErrorListUrl


@pytest.mark.django_db
@pytest.mark.parametrize(
    "client",
    ["authenticated_client", "unauthenticated_client"],
    indirect=True,
)
class TestErrorsViewSetListTest:
  """Tests for the ErrorsViewSet list view."""

  def test_list__no_filter__returns_correct_response(
      self,
      client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error_batch: "QuerySet[Error]",
  ) -> None:
    serializer = ErrorSerializer(error_batch, many=True)

    res = client.get(error_list_url())

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_item_id__returns_correct_response(
      self,
      client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error_batch: "QuerySet[Error]",
  ) -> None:
    first_item = cast("Error", error_batch.first()).item
    query = Error.objects.filter(item=first_item.id,)

    res = client.get(error_list_url({"itemId": first_item.id}))
    serializer = ErrorSerializer(query, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_reoccurring__returns_correct_response(
      self,
      client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error_batch: "QuerySet[Error]",
  ) -> None:
    query = Error.objects.filter(is_reoccurring=True)

    res = client.get(error_list_url({"is_reoccurring": True}))
    serializer = ErrorSerializer(query, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_store_id__returns_correct_response(
      self,
      client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error_batch: "QuerySet[Error]",
  ) -> None:
    last_store = cast("Error", error_batch.last()).store
    query = Error.objects.filter(store=last_store.id,)

    res = client.get(error_list_url({"storeId": last_store.id}))
    serializer = ErrorSerializer(query, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data

  def test_list__filter_by_type__returns_correct_response(
      self,
      client: "APIClient",
      error_list_url: "AliasErrorListUrl",
      error_batch: "QuerySet[Error]",
  ) -> None:
    first_type = cast("Error", error_batch.last()).type
    query = Error.objects.filter(type=first_type.id,)

    res = client.get(error_list_url({"type": first_type.name}))
    serializer = ErrorSerializer(query, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
