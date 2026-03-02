"""Errors API endpoints."""

from errors.models import Error
from errors.models.serializers.read_write.error import ErrorSerializerRW
from rest_framework import viewsets
from utilities.views.viewsets.mixins import upsert
from .filters import ErrorFilter


class ErrorViewSet(
    upsert.UpsertModelMixin[Error],
    viewsets.ModelViewSet[Error],
):
  """Error API endpoint."""

  queryset = Error.objects.all()
  serializer_class = ErrorSerializerRW
  filterset_class = ErrorFilter
