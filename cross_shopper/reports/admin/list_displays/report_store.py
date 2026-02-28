"""ReportStore admin model list display."""

from utilities.admin.list_displays.columns import (
    ColumnLinkConfig,
    ColumnObjectConfig,
)

report_store_list_display = (
    ColumnObjectConfig(
        method_name="report_store",
        description="Report Store",
        obj_lookup="",
    ),
    ColumnLinkConfig(
        method_name="store__report",
        description="Report",
        reverse_url_name="admin:reports_report_change",
        obj_id_lookup="report.pk",
        obj_name_lookup="report.name",
    ),
    ColumnLinkConfig(
        method_name="store__address",
        description="Store",
        reverse_url_name="admin:stores_store_change",
        obj_id_lookup="store.pk",
        obj_name_lookup="store.address",
    ),
    ColumnLinkConfig(
        method_name="store__franchise",
        description="Franchise",
        reverse_url_name="admin:stores_franchise_change",
        obj_id_lookup="store.franchise.pk",
        obj_name_lookup="store.franchise.name",
    ),
)
