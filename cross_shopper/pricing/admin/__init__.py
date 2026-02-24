"""Admin models for the pricing app."""

from django.contrib import admin
from ..models import Price
from .price import PriceAdmin

admin.site.register(Price, PriceAdmin)
