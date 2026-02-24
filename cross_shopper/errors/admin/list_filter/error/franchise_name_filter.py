"""Franchise name model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class FranchiseNameFilter(AdminListFilterBase):
  title = "franchise"
  parameter_name = "store__franchise__name"
