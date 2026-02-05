"""Custom admin for the django-address Locality model."""

from address.models import Locality
from django.contrib import admin


class LocalityAdmin(admin.ModelAdmin[Locality]):
  list_filter = (
      "state__name",
      "state__country",
  )
  ordering = (
      "state__country",
      "state__name",
  )
