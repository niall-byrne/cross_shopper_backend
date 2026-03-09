"""Report data migration for TitleField refactor."""
from __future__ import annotations

from typing import TYPE_CHECKING, cast

from django.db import migrations, transaction

if TYPE_CHECKING:
  from django.apps.registry import Apps
  from django.db.backends.base.schema import BaseDatabaseSchemaEditor
  from reports.models import Report


def save_all_func(
    apps: Apps,
    schema_editor: BaseDatabaseSchemaEditor,
) -> None:
  ReportModel = cast(
      "Report",
      apps.get_model("reports", "Report"),
  )

  with transaction.atomic():
    for scraper in ReportModel.objects.all():
      scraper.save()


class Migration(migrations.Migration):

  dependencies = [
      ("reports", "0005_alter_report_name_constraints"),
  ]

  operations = [
      migrations.RunPython(save_all_func, save_all_func),
  ]
