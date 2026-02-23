"""Tests for the list_display_column_generator function."""

from typing import Tuple
from unittest import mock

from django.urls import reverse
from django.utils.html import format_html
from utilities.admin.list_display.column_generator import (
    ColumnLinkConfig,
    ColumnObjectConfig,
    list_display_column_generator,
)


class TestListDisplayColumnGenerator:
  """Tests for the list_display_column_generator function."""

  def test_single_configuration__sets_the_correct_method_name(
      self,
      column_config_1: Tuple[ColumnLinkConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_1)

    assert hasattr(mocked_admin, column_config_1[0].method_name) is True

  def test_single_configuration__sets_the_correct_description(
      self,
      column_config_1: Tuple[ColumnLinkConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_1)

    assert mocked_admin.method_name.short_description == (
        column_config_1[0].description
    )

  def test_single_configuration__method_called__not_none__returns_html(
      self,
      column_config_1: Tuple[ColumnLinkConfig],
      mocked_admin: mock.Mock,
      mocked_model: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_1)

    html = mocked_admin.method_name(mocked_admin, mocked_model)

    assert html == format_html(
        '<a href="{}">{}</a>'.format(
            reverse(
                column_config_1[0].reverse_url_name,
                args=(mocked_model.related.field.id,)
            ),
            mocked_model.related.field.name,
        )
    )

  def test_single_configuration__method_called__none__returns_none(
      self,
      column_config_1: Tuple[ColumnLinkConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_1)

    html = mocked_admin.method_name(mocked_admin, None)

    assert html is None

  def test_dual_configuration__sets_the_correct_method_names(
      self,
      column_config_2: Tuple[ColumnLinkConfig, ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_2)

    assert hasattr(mocked_admin, column_config_2[0].method_name) is True
    assert hasattr(mocked_admin, column_config_2[1].method_name) is True

  def test_dual_configuration__sets_the_correct_descriptions(
      self,
      column_config_2: Tuple[ColumnLinkConfig, ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_2)

    assert mocked_admin.method_name_1.short_description == (
        column_config_2[0].description
    )
    assert mocked_admin.method_name_2.short_description == (
        column_config_2[1].description
    )

  def test_dual_configuration__method_1_called__not_none__returns_html(
      self,
      column_config_2: Tuple[ColumnLinkConfig, ColumnObjectConfig],
      mocked_admin: mock.Mock,
      mocked_model: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_2)

    html = mocked_admin.method_name_1(mocked_admin, mocked_model)

    assert html == format_html(
        '<a href="{}">{}</a>'.format(
            reverse(
                column_config_2[0].reverse_url_name,
                args=(mocked_model.related.field1.id,)
            ),
            mocked_model.related.field1.name,
        )
    )

  def test_dual_configuration__method_1_called__none__returns_none(
      self,
      column_config_2: Tuple[ColumnLinkConfig, ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_2)

    html = mocked_admin.method_name_1(mocked_admin, None)

    assert html is None

  def test_dual_configuration__method_2_called__not_none__returns_object(
      self,
      column_config_2: Tuple[ColumnLinkConfig, ColumnObjectConfig],
      mocked_admin: mock.Mock,
      mocked_model: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_2)

    obj = mocked_admin.method_name_2(mocked_admin, mocked_model)

    assert obj == mocked_model

  def test_dual_configuration__method_2_called__none__returns_none(
      self,
      column_config_2: Tuple[ColumnLinkConfig, ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_2)

    obj = mocked_admin.method_name_2(mocked_admin, None)

    assert obj is None

  def test_boolean_configuration__sets_the_correct_method_name(
      self,
      column_config_3: Tuple[ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_3)

    assert hasattr(mocked_admin, column_config_3[0].method_name) is True

  def test_boolean_configuration__sets_the_correct_description(
      self,
      column_config_3: Tuple[ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_3)

    assert mocked_admin.boolean_method_name.short_description == (
        column_config_3[0].description
    )

  def test_boolean_configuration__sets_boolean_to_true(
      self,
      column_config_3: Tuple[ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_3)

    assert mocked_admin.boolean_method_name.boolean is True

  def test_boolean_configuration__method_called__not_none__returns_object(
      self,
      column_config_3: Tuple[ColumnObjectConfig],
      mocked_admin: mock.Mock,
      mocked_model: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_3)

    obj = mocked_admin.boolean_method_name(mocked_admin, mocked_model)

    assert obj == mocked_model.boolean.related.field

  def test_boolean_configuration__method_called__none__returns_none(
      self,
      column_config_3: Tuple[ColumnObjectConfig],
      mocked_admin: mock.Mock,
  ) -> None:
    list_display_column_generator(mocked_admin)(config=column_config_3)

    obj = mocked_admin.boolean_method_name(mocked_admin, None)

    assert obj is None
