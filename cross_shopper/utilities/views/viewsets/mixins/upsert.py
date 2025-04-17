"""Upsert model instance rest_framework viewset mixin class."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast

from rest_framework import mixins, status
from rest_framework.response import Response

if TYPE_CHECKING:
  from django.db.models import Model
  from rest_framework.request import Request
  from rest_framework.viewsets import ModelViewSet

ModelType = TypeVar("ModelType", bound="Model")


class UpsertModelMixin(mixins.CreateModelMixin, Generic[ModelType]):
  """Create a model instance, or update an existing model instance."""

  def __as_mixin(self) -> ModelViewSet[ModelType]:
    return cast("ModelViewSet[ModelType]", self)

  def create(
      self,
      request: Request,
      *args: Any,
      **kwargs: dict[str, Any],
  ) -> Response:
    """Create a model instance, or update an existing model instance."""
    serializer = self.__as_mixin().get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.__as_mixin().perform_create(serializer)
    headers = self.get_success_headers(serializer.data)

    status_code: int = status.HTTP_201_CREATED

    if not serializer.context.get("created", False):
      status_code = status.HTTP_200_OK

    return Response(
        serializer.data,
        status=status_code,
        headers=headers,
    )
