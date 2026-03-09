"""Scraper data migration for TitleField refactor."""

from typing import TYPE_CHECKING, cast

from django.db import migrations, transaction

if TYPE_CHECKING:  # no cover
  from django.apps.registry import Apps
  from django.db.backends.base.schema import BaseDatabaseSchemaEditor
  from scrapers.models import Scraper


def save_all_func(
    apps: "Apps",
    schema_editor: "BaseDatabaseSchemaEditor",
) -> None:
  ScraperModel = cast(
      "Scraper",
      apps.get_model("scrapers", "Scraper"),
  )

  with transaction.atomic():
    for scraper in ScraperModel.objects.all():
      scraper.save()


class Migration(migrations.Migration):

  dependencies = [
      ("scrapers", "0004_alter_scraperconfig_url_constraints"),
  ]

  operations = [
      migrations.RunPython(save_all_func, save_all_func),
  ]
