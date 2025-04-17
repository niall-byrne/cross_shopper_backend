"""Admin models for the pricing app."""

from django.contrib import admin
from pricing.admin.price import PriceAdmin
from pricing.models import Price

admin.site.register(Price, PriceAdmin)
