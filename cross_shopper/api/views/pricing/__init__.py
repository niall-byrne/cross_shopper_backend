"""Pricing API endpoints."""

from typing import Any, Dict

from pricing.models import Price
from pricing.models.serializers.pricing import PricingSerializer
from rest_framework import status, viewsets
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
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)

    status_code: int = status.HTTP_201_CREATED

    if not serializer.context.get("created", False):
      status_code = status.HTTP_200_OK

    return Response(
        serializer.data,
        status=status_code,
        headers=headers,
    )
