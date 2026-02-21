"""Admin for the error type model."""

from django.contrib import admin
from errors.models import ErrorType


class ErrorTypeAdmin(admin.ModelAdmin[ErrorType]):
  ordering = ("name",)
