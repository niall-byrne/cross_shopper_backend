"""Test the ReportStore admin model list display."""

from reports.admin.list_displays.report_store import (
    report_store_list_display,
)
from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)
from utilities.testing.comparisons.instance import InstanceOfClass


class TestReportStoreAdminListDisplay:

  def test_list_display(self) -> None:
    assert report_store_list_display == (
        InstanceOfClass(
            base=ColumnObjectConfig,
            attributes={
                "method_name": "report_store",
                "description": "Report Store",
                "obj_lookup": "",
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "store__report",
                "description": "Report",
                "reverse_url_name": "admin:reports_report_change",
                "obj_id_lookup": "report.pk",
                "obj_name_lookup": "report.name",
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "store__address",
                "description": "Store",
                "reverse_url_name": "admin:stores_store_change",
                "obj_id_lookup": "store.pk",
                "obj_name_lookup": "store.address",
            }
        ),
        InstanceOfClass(
            base=ColumnLinkConfig,
            attributes={
                "method_name": "store__franchise",
                "description": "Franchise",
                "reverse_url_name": "admin:stores_franchise_change",
                "obj_id_lookup": "store.franchise.pk",
                "obj_name_lookup": "store.franchise.name",
            }
        ),
    )
