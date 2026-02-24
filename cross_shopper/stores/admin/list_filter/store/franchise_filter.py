"""Franchise model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class FranchiseFilter(AdminListFilterBase):
  title = 'franchise'
  parameter_name = 'franchise__name'
