"""Admin models for the errors app."""

from django.contrib import admin
from errors.admin.error import ErrorAdmin
from errors.admin.error_type import ErrorTypeAdmin
from errors.models import Error, ErrorType

admin.site.register(ErrorType, ErrorTypeAdmin)
admin.site.register(Error, ErrorAdmin)
