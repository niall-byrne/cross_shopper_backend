"""Pricing API endpoints."""
from __future__ import annotations

from pricing.models import Price
from pricing.models.serializers.pricing import PricingSerializer
from rest_framework import viewsets
from utilities.views.viewsets.mixins import upsert
from .filters import PricingFilter


class PricingViewSet(
    upsert.UpsertModelMixin[Price],
    viewsets.ModelViewSet[Price],
):
  """Pricing API endpoint."""

  queryset = Price.objects.all()
  serializer_class = PricingSerializer
  filterset_class = PricingFilter
