"""Admin models for the errors app."""

from django.contrib import admin
from ..models import Error, ErrorType
from . import filters
from .error import ErrorAdmin
from .error_type import ErrorTypeAdmin

admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(
    Error,
    ErrorAdmin,
    list_filter=filters.error_filter,
)
