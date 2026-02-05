"""Test the admin for the Locality model."""

from django.contrib import admin
from utilities.admin.django_address.state import StateAdmin


class TestStateAdmin:
  """Test the StateAdmin class."""

  def test_instantiate__inheritance(
      self,
      state_admin: StateAdmin,
  ) -> None:
    assert isinstance(state_admin, admin.ModelAdmin)

  def test_instantiate__has_correct_list_filter(
      self,
      state_admin: StateAdmin,
  ) -> None:
    assert state_admin.list_filter == ("country",)

  def test_instantiate__has_correct_ordering(
      self,
      state_admin: StateAdmin,
  ) -> None:
    assert state_admin.ordering == (
        "country",
        "name",
    )
