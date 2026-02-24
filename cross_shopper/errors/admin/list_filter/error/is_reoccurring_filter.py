"""Is reoccurring model list filter."""

from utilities.admin.list_filter.bases.admin_list_filter_base import (
    AdminListFilterBase,
)


class IsReoccurringFilter(AdminListFilterBase):
  title = "is_reoccurring"
  parameter_name = "is_reoccurring"
  is_boolean = True
