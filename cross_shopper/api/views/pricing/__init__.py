"""Pricing API endpoints."""

from typing import Any, Dict, Optional

from pricing.models import Price
from pricing.models.serializers.pricing import PricingSerializer
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from .filters import PricingFilter


class PricingViewSet(
    viewsets.ModelViewSet[Price],
):
  """Pricing API endpoint."""

  queryset = Price.objects.all()
  serializer_class = PricingSerializer
  filterset_class = PricingFilter

  def create(
      self,
      request: Request,
      *args: Any,
      **kwargs: Dict[str, Any],
  ) -> Response:
    """Create a model instance, or update an existing model instance."""
    existing_object = self.get_existing_object(request)

    if existing_object:
      self.kwargs['pk'] = existing_object.pk
      return self.update(request, *args, **kwargs)
    return super().create(request, *args, **kwargs)

  def get_existing_object(self, request: Request) -> Optional[Price]:
    """Retrieve any existing object that matches the request data."""
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    return self.queryset.filter(
        item=serializer.data["item"],
        store=serializer.data["store"],
        week=serializer.data["week"],
        year=serializer.data["year"],
    ).first()
