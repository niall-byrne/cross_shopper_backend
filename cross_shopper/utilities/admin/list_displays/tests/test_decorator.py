"""Tests for the generate_list_display decorator."""

from typing import TYPE_CHECKING, Tuple

from django.urls import reverse
from django.utils.html import format_html
from utilities.admin.list_displays import generate_list_display

if TYPE_CHECKING:  # no cover
  from unittest import mock

  from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
  )


class TestGenerateListDisplay:

  def test_single_config__columns_evaluate_as_string_correctly(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
  ) -> None:
    assert tuple(str(element) for element in column_config_1) == \
        ("method_name",)

  def test_single_config__def_order___order__sets_the_correct_method_name(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_1)(mocked_admin)

    assert hasattr(mocked_admin, column_config_1[0].method_name) is True

  def test_single_config__def_order__sets_the_correct_description(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_1)(mocked_admin)

    assert mocked_admin.method_name.short_description == (
        column_config_1[0].description
    )

  def test_single_config__def_order__sets_the_correct_ordering(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_1)(mocked_admin)

    assert mocked_admin.method_name.admin_order_field == (
        column_config_1[0].obj_name_lookup.replace(".", "__")
    )

  def test_single_config__set_order__sets_the_correct_ordering(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    column_config_1[0].obj_order = "related.field1.ordering"

    generate_list_display(config=column_config_1)(mocked_admin)

    assert mocked_admin.method_name.admin_order_field == (
        column_config_1[0].obj_order.replace(".", "__")
    )

  def test_single_config__no_order__sets_the_correct_ordering(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    column_config_1[0].obj_order = None

    generate_list_display(config=column_config_1)(mocked_admin)

    assert not hasattr(mocked_admin.method_name, "admin_order_field")

  def test_single_config__def_order__method_called__not_none__returns_html(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
      mocked_model: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_1)(mocked_admin)

    html = mocked_admin.method_name(mocked_admin, mocked_model)

    assert html == format_html(
        '<a href="{}">{}</a>'.format(
            reverse(
                column_config_1[0].reverse_url_name,
                args=(mocked_model.related.field.pk,)
            ),
            mocked_model.related.field.name,
        )
    )

  def test_single_config__def_order__method_called__none__returns_none(
      self,
      column_config_1: Tuple["ColumnLinkConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_1)(mocked_admin)

    html = mocked_admin.method_name(mocked_admin, None)

    assert html is None

  def test_dual_config__columns_evaluate_as_string_correctly(
      self,
      column_config_2: Tuple["ColumnLinkConfig"],
  ) -> None:
    assert tuple(str(element) for element in column_config_2) == (
        "method_name_1",
        "method_name_2",
    )

  def test_dual_config__def_order__sets_the_correct_method_names(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    assert hasattr(mocked_admin, column_config_2[0].method_name) is True
    assert hasattr(mocked_admin, column_config_2[1].method_name) is True

  def test_dual_config__def_order__sets_the_correct_descriptions(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    assert mocked_admin.method_name_1.short_description == (
        column_config_2[0].description
    )
    assert mocked_admin.method_name_2.short_description == (
        column_config_2[1].description
    )

  def test_dual_config__def_order__sets_the_correct_ordering(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    assert mocked_admin.method_name_1.admin_order_field == (
        column_config_2[0].obj_name_lookup.replace(".", "__")
    )
    assert mocked_admin.method_name_2.admin_order_field == (
        column_config_2[1].obj_lookup.replace(".", "__")
    )

  def test_dual_config__set_order__sets_the_correct_ordering(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    column_config_2[0].obj_order = "related.field1.ordering"
    column_config_2[1].obj_order = "field2.ordering"

    generate_list_display(config=column_config_2)(mocked_admin)

    assert mocked_admin.method_name_1.admin_order_field == (
        column_config_2[0].obj_order.replace(".", "__")
    )
    assert mocked_admin.method_name_2.admin_order_field == (
        column_config_2[1].obj_order.replace(".", "__")
    )

  def test_dual_config__no_order__sets_the_correct_ordering(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    column_config_2[0].obj_order = None
    column_config_2[1].obj_order = None

    generate_list_display(config=column_config_2)(mocked_admin)

    assert not hasattr(mocked_admin.method_name_1, "admin_order_field")
    assert not hasattr(mocked_admin.method_name_2, "admin_order_field")

  def test_dual_config__def_order__method_1_called__not_none__returns_html(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
      mocked_model: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    html = mocked_admin.method_name_1(mocked_admin, mocked_model)

    assert html == format_html(
        '<a href="{}">{}</a>'.format(
            reverse(
                column_config_2[0].reverse_url_name,
                args=(mocked_model.related.field1.pk,)
            ),
            mocked_model.related.field1.name,
        )
    )

  def test_dual_config__def_order__method_1_called__none__returns_none(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    html = mocked_admin.method_name_1(mocked_admin, None)

    assert html is None

  def test_dual_config__def_order__method_2_called__not_none__returns_object(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
      mocked_model: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    obj = mocked_admin.method_name_2(mocked_admin, mocked_model)

    assert obj == mocked_model

  def test_dual_config__def_order__method_2_called__none__returns_none(
      self,
      column_config_2: Tuple["ColumnLinkConfig", "ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_2)(mocked_admin)

    obj = mocked_admin.method_name_2(mocked_admin, None)

    assert obj is None

  def test_boolean_config__columns_evaluate_as_string_correctly(
      self,
      column_config_3: Tuple["ColumnLinkConfig"],
  ) -> None:
    assert tuple(str(element) for element in column_config_3) == \
        ("boolean_method_name",)

  def test_boolean_config__def_order__sets_the_correct_method_name(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_3)(mocked_admin)

    assert hasattr(mocked_admin, column_config_3[0].method_name) is True

  def test_boolean_config__def_order__sets_the_correct_description(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_3)(mocked_admin)

    assert mocked_admin.boolean_method_name.short_description == (
        column_config_3[0].description
    )

  def test_boolean_config__def_order__sets_the_correct_ordering(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_3)(mocked_admin)

    assert mocked_admin.boolean_method_name.admin_order_field == (
        column_config_3[0].obj_lookup.replace(".", "__")
    )

  def test_boolean_config__no_order__sets_the_correct_ordering(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    column_config_3[0].obj_order = "related.field1.ordering"

    generate_list_display(config=column_config_3)(mocked_admin)

    assert mocked_admin.boolean_method_name.admin_order_field == (
        column_config_3[0].obj_order.replace(".", "__")
    )

  def test_boolean_config__set_order__sets_the_correct_ordering(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    column_config_3[0].obj_order = None

    generate_list_display(config=column_config_3)(mocked_admin)

    assert not hasattr(mocked_admin.boolean_method_name, "admin_order_field")

  def test_boolean_config__def_order__sets_boolean_to_true(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_3)(mocked_admin)

    assert mocked_admin.boolean_method_name.boolean is True

  def test_boolean_config__def_order__method_called__not_none__returns_object(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
      mocked_model: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_3)(mocked_admin)

    obj = mocked_admin.boolean_method_name(mocked_admin, mocked_model)

    assert obj == mocked_model.boolean.related.field

  def test_boolean_config__def_order__method_called__none__returns_none(
      self,
      column_config_3: Tuple["ColumnObjectConfig"],
      mocked_admin: "mock.Mock",
  ) -> None:
    generate_list_display(config=column_config_3)(mocked_admin)

    obj = mocked_admin.boolean_method_name(mocked_admin, None)

    assert obj is None

    assert obj is None
