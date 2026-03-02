"""Errors API endpoints."""

from typing import Any, Dict, Optional

from errors.models import Error
from errors.models.serializers.read_write.error import ErrorSerializerRW
from rest_framework import viewsets
from rest_framework.request import Request
from .filters import ErrorFilter


class ErrorViewSet(
    viewsets.ModelViewSet,
):
  """Error API endpoint."""

  queryset = Error.objects.all()
  serializer_class = ErrorSerializerRW
  filterset_class = ErrorFilter

  def create(self, request: Request, *args: Any, **kwargs: Dict[str, Any]):
    """Create a model instance, or update an existing model instance."""
    existing_object = self.get_existing_object(request)

    if existing_object:
      self.kwargs["pk"] = existing_object.pk
      return self.update(request, *args, **kwargs)
    return super().create(request, *args, **kwargs)

  def get_existing_object(self, request: Request) -> Optional[Error]:
    """Retrieve any existing object that matches the request data."""
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    filter_params = dict(serializer.data)
    filter_params["type__name"] = filter_params.pop("type")

    return self.queryset.filter(**filter_params).first()
