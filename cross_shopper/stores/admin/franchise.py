"""Admin for the franchise model."""

from django.contrib import admin
from stores.models import Franchise


class FranchiseAdmin(admin.ModelAdmin[Franchise]):
  ordering = ('name',)
