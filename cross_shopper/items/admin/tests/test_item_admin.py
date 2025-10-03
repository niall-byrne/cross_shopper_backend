"""Test the admin for the Item model."""

from unittest import mock

import pytest
from django.test import override_settings
from items.admin.item import ItemAdmin, ItemScraperConfigInline


class TestItemAdmin:
  """Test the ItemAdmin class."""

  def test_instantiate__has_correct_fieldsets(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.fieldsets == (
        (
            "IDENTIFICATION",
            {
                "fields": ('name', 'brand')
            },
        ), (
            "PACKAGING",
            {
                "fields": ('packaging',),
            },
        ), (
            "CHARACTERISTICS",
            {
                "fields": (
                    'is_non_gmo',
                    'is_organic',
                ),
            },
        )
    )

  def test_instantiate__has_correct_inlines(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.inlines == [ItemScraperConfigInline]

  def test_instantiate__has_correct_search_fields(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.search_fields == ("name", "brand__name")

  def test_get_ordering__returns_correct_field_order(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.ordering == (
        'name',
        'brand__name',
        'is_organic',
        'packaging__container',
        'packaging__quantity',
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
    mocked_model_manager.order_by.assert_called_once_with('name')

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
        'container__name',
        'quantity',
    )

  @pytest.mark.parametrize(
      "model_change", (True, False), ids=lambda b: f"change-{b}"
  )
  @override_settings(ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS=True)
  def test_save_model__model_object__setting_on___item_attached_to_reports(
      self,
      item_admin: ItemAdmin,
      mocked_form: mock.Mock,
      mocked_report_manger: mock.Mock,
      mocked_request: mock.Mock,
      model_change: bool,
  ) -> None:
    mocked_object = mock.Mock()

    item_admin.save_model(
        mocked_request, mocked_object, mocked_form, model_change
    )

    mocked_report_manger.filter.assert_called_once_with(is_testing_only=False)
    for mocked_report in mocked_report_manger.filter.return_value:
      mocked_report.item.add.assert_called_once_with(mocked_object)

  @pytest.mark.parametrize(
      "model_change", (True, False), ids=lambda b: f"change-{b}"
  )
  @override_settings(ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS=False)
  def test_save_model__model_object__setting_off__item_not_attached_to_reports(
      self,
      item_admin: ItemAdmin,
      mocked_form: mock.Mock,
      mocked_report_manger: mock.Mock,
      mocked_request: mock.Mock,
      model_change: bool,
  ) -> None:
    mocked_object = mock.Mock()

    item_admin.save_model(
        mocked_request, mocked_object, mocked_form, model_change
    )

    mocked_report_manger.filter.assert_not_called()
    for mocked_report in mocked_report_manger.filter.return_value:
      mocked_report.item.add.assert_not_called()

  @pytest.mark.parametrize(
      "model_change", (True, False), ids=lambda b: f"change-{b}"
  )
  @pytest.mark.usefixtures('mocked_request')
  def test_save_model__model_object__saves_model_object(
      self,
      item_admin: ItemAdmin,
      mocked_form: mock.Mock,
      mocked_request: mock.Mock,
      model_change: bool,
  ) -> None:
    mocked_object = mock.Mock()

    item_admin.save_model(
        mocked_request, mocked_object, mocked_form, model_change
    )

    mocked_object.save.assert_called_once_with()
