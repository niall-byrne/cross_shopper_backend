"""Admin for the brand model."""

from django.contrib import admin
from items.models import Brand


class BrandAdmin(admin.ModelAdmin[Brand]):
  ordering = ("name",)
