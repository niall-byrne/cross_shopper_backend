"""Pricing API endpoints."""

from pricing.models import Price
from pricing.models.serializers.read_write.pricing import PricingSerializerRW
from rest_framework import viewsets
from .filters import PricingFilter


class PricingViewSet(
    viewsets.ModelViewSet[Price],
):
  """Pricing API endpoint."""

  queryset = Price.objects.all()
  serializer_class = PricingSerializerRW
  filterset_class = PricingFilter
