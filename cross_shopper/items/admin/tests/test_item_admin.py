"""Test the admin for the Item model."""

from unittest import mock

import pytest
from constance.test import override_config
from django.contrib import admin
from items.admin.inlines.item import item_inlines
from items.admin.item import ItemAdmin
from items.admin.list_displays.item import item_list_display
from items.admin.list_filters.item import item_list_filter
from items.admin.mixins.price_group_members import PriceGroupMembersAdminMixin


@pytest.mark.django_db
class TestItemAdmin:

  def test_instantiate__inheritance(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert isinstance(item_admin, admin.ModelAdmin)
    assert isinstance(item_admin, PriceGroupMembersAdminMixin)

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
            "PRICE COMPARISONS",
            {
                "fields": ('price_group', 'price_group_members'),
            },
        ), (
            "CERTIFICATIONS",
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
    assert item_admin.inlines == item_inlines

  def test_instantiate__has_correct_list_display(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.list_display == tuple(map(str, item_list_display))

  def test_instantiate__has_correct_list_filter(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.list_filter == item_list_filter

  def test_instantiate__has_correct_ordering(
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

  def test_instantiate__has_correct_readonly_fields(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.readonly_fields == ('price_group_members',)

  def test_instantiate__has_correct_search_fields(
      self,
      item_admin: ItemAdmin,
  ) -> None:
    assert item_admin.search_fields == (
        "name",
        "attribute__name",
        "brand__name",
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

  def test_price_group_members__passes_price_group_to_mixin(
      self,
      item_admin: ItemAdmin,
      mocked_price_group_members_mixin: mock.Mock,
  ) -> None:
    mocked_object = mock.Mock()

    html = item_admin.price_group_members(mocked_object)

    mocked_price_group_members_mixin.assert_called_once_with(
        mocked_object.price_group
    )
    assert html == mocked_price_group_members_mixin.return_value

  @pytest.mark.parametrize(
      "model_change", (True, False), ids=lambda b: f"change-{b}"
  )
  @override_config(ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS=True)
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

    mocked_report_manger.filter.assert_called_once_with(is_testing=False)
    for mocked_report in mocked_report_manger.filter.return_value:
      mocked_report.item.add.assert_called_once_with(mocked_object)

  @pytest.mark.parametrize(
      "model_change", (True, False), ids=lambda b: f"change-{b}"
  )
  @override_config(ADMIN_AUTO_ATTACH_ITEMS_TO_REPORTS=False)
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
