"""Test the admin for the Item model."""
from __future__ import annotations

from typing import TYPE_CHECKING

from items.admin.inlines.item import item_inlines

if TYPE_CHECKING:
  from unittest import mock

  from items.admin.item import ItemAdmin


class TestItemAdmin:

  def test_instantiate__has_correct_fieldsets(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.fieldsets == (
        (
            "IDENTIFICATION",
            {
                "fields": ("name", "brand")
            },
        ), (
            "PACKAGING",
            {
                "fields": ("packaging",),
            },
        ), (
            "CHARACTERISTICS",
            {
                "fields": (
                    "is_non_gmo",
                    "is_organic",
                ),
            },
        )
    )

  def test_instantiate__has_correct_inlines(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.inlines == item_inlines

  def test_instantiate__has_correct_ordering(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.ordering == (
        "name",
        "brand__name",
        "is_organic",
        "packaging__container",
        "packaging__quantity",
    )

  def test_formfield_for_foreignkey__default__correct_sort_order(
      self,
      item_admin: ItemAdmin,
      mocked_db_field: mock.Mock,
      mocked_formfield_for_foreignkey: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    mocked_db_field.name = "default"

    item_admin.formfield_for_foreignkey(mocked_db_field, mocked_request)

    mocked_formfield_for_foreignkey.assert_called_once_with(
        mocked_db_field,
        mocked_request,
    )

  def test_formfield_for_foreignkey__brand_model__correct_sort_order(
      self,
      item_admin: ItemAdmin,
      mocked_db_field: mock.Mock,
      mocked_formfield_for_foreignkey: mock.Mock,
      mocked_model_manager: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    mocked_db_field.name = "brand"

    item_admin.formfield_for_foreignkey(mocked_db_field, mocked_request)

    mocked_formfield_for_foreignkey.assert_called_once_with(
        mocked_db_field,
        mocked_request,
        queryset=mocked_model_manager.order_by.return_value,
    )
    mocked_model_manager.order_by.assert_called_once_with("name")

  def test_formfield_for_foreignkey__packaging_model__correct_sort_order(
      self,
      item_admin: ItemAdmin,
      mocked_db_field: mock.Mock,
      mocked_formfield_for_foreignkey: mock.Mock,
      mocked_model_manager: mock.Mock,
      mocked_request: mock.Mock,
  ) -> None:
    mocked_db_field.name = "packaging"

    item_admin.formfield_for_foreignkey(mocked_db_field, mocked_request)

    mocked_formfield_for_foreignkey.assert_called_once_with(
        mocked_db_field,
        mocked_request,
        queryset=mocked_model_manager.order_by.return_value,
    )
    mocked_model_manager.order_by.assert_called_once_with(
        "container__name",
        "quantity",
    )
