"""Test fixtures for the utilities app model admins."""

from typing import Tuple
from unittest import mock

import pytest
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)


@pytest.fixture
def column_config_1() -> Tuple[ColumnLinkConfig]:
  return (
      ColumnLinkConfig(
          method_name="method_name",
          description="simple description",
          reverse_url_name="admin:stores_store_change",
          obj_id_lookup="related.field.pk",
          obj_name_lookup="related.field.name",
      ),
  )


@pytest.fixture
def column_config_2() -> Tuple[ColumnLinkConfig, ColumnObjectConfig]:
  return (
      ColumnLinkConfig(
          method_name="method_name_1",
          description="simple description 1",
          reverse_url_name="admin:stores_store_change",
          obj_id_lookup="related.field1.pk",
          obj_name_lookup="related.field1.name",
      ),
      ColumnObjectConfig(
          method_name="method_name_2",
          description="simple description 2",
          obj_lookup=""
      ),
  )


@pytest.fixture
def column_config_3() -> Tuple[ColumnObjectConfig]:
  return (
      ColumnObjectConfig(
          method_name="boolean_method_name",
          description="boolean simple description",
          obj_lookup="boolean.related.field",
          is_boolean=True,
      ),
  )


@pytest.fixture
def mocked_admin() -> mock.Mock:
  return mock.Mock()


@pytest.fixture
def mocked_model() -> mock.Mock:
  return mock.Mock()
