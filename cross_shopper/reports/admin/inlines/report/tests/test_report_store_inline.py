"""Test the ReportStore admin model inline."""
from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib import admin
from reports.models.report_store import ReportStore

if TYPE_CHECKING:
  from reports.admin.inlines.report.report_store import ReportStoreInline


class TestReportStoreInline:

  def test_instantiate__inheritance(
      self,
      item_scraper_config_inline: ReportStoreInline,
  ) -> None:
    assert isinstance(item_scraper_config_inline, admin.StackedInline)

  def test_instantiate__has_correct_extra(
      self,
      item_scraper_config_inline: ReportStoreInline,
  ) -> None:
    assert item_scraper_config_inline.extra == 0

  def test_instantiate__has_correct_ordering(
      self,
      item_scraper_config_inline: ReportStoreInline,
  ) -> None:
    assert item_scraper_config_inline.ordering == (
        "store__franchise__name",
        "store__address",
    )

  def test_instantiate__has_correct_model(
      self,
      item_scraper_config_inline: ReportStoreInline,
  ) -> None:
    assert item_scraper_config_inline.model == ReportStore

  def test_instantiate__has_correct_verbose_name(
      self,
      item_scraper_config_inline: ReportStoreInline,
  ) -> None:
    assert item_scraper_config_inline.verbose_name == "Report Store"

  def test_instantiate__has_correct_verbose_name_plural(
      self,
      item_scraper_config_inline: ReportStoreInline,
  ) -> None:
    assert item_scraper_config_inline.verbose_name_plural == "Report Stores"
