"""Custom admin for the django-address State model."""

from address.models import State
from django.contrib import admin


class StateAdmin(admin.ModelAdmin[State]):
  list_filter = ("country",)
  ordering = (
      "country",
      "name",
  )
