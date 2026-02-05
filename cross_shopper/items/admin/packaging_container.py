"""Admin for the packaging container model."""

from django.contrib import admin
from items.models import PackagingContainer


class PackagingContainerAdmin(admin.ModelAdmin[PackagingContainer]):
  ordering = ('name',)
