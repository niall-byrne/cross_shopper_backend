"""Test the admin for the ErrorType model."""

from django.contrib import admin
from errors.admin.error_type import ErrorTypeAdmin


class TestErrorTypeAdmin:

  def test_instantiate__inheritance(
      self,
      error_type_admin: ErrorTypeAdmin,
  ) -> None:
    assert isinstance(error_type_admin, admin.ModelAdmin)

  def test_instantiate__ordering(
      self,
      error_type_admin: ErrorTypeAdmin,
  ) -> None:
    assert error_type_admin.ordering == ("name",)
