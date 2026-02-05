"""Custom admin for the django-address Address model."""

from address.models import Address
from django.contrib import admin


class AddressAdmin(admin.ModelAdmin[Address]):
  list_filter = (
      "locality__name",
      "locality__state",
      "locality__state__country",
  )
  ordering = (
      "locality__state__country",
      "locality__state",
      "locality__name",
      "route",
      "street_number",
  )
