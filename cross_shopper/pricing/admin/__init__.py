"""Admin models for the pricing app."""

from django.contrib import admin
from ..models import Price
from .filters import price_filter
from .price import PriceAdmin

admin.site.register(Price, PriceAdmin, list_filter=price_filter)
