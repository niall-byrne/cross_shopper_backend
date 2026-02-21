"""Test the ReportSerializer class."""

import pytest
from django.conf import settings
from django.db.models import Prefetch
from items.models.serializers.item import ItemSerializer
from reports.models import Report
from scrapers.models import ScraperConfig
from stores.models.serializers.store import StoreSerializer
from ..report import ReportSerializer
from .conftest import AliasCreateMockedRequest


@pytest.mark.django_db
class TestReportSerializer:
  query_param = settings.QUERY_PARAMETER_REPORT_ITEM_SCRAPER_CONFIG_IS_ACTIVE

  def test_serialization__no_filter__correct_representation(
      self,
      report: Report,
      create_mocked_request: AliasCreateMockedRequest,
  ) -> None:
    serialized = ReportSerializer(
        report, context={'request': create_mocked_request({})}
    )

    assert serialized.data == {
        "id":
            report.id,
        "name":
            report.name,
        "item":
            ItemSerializer(
                report.item.all().order_by(
                    *ReportSerializer.ITEM_FIELD_ORDERING
                ),
                many=True,
            ).data,
        "store":
            StoreSerializer(
                report.store,
                many=True,
            ).data,
        "is_testing_only":
            report.is_testing_only,
    }

  def test_serialization__active_scrapers__correct_representation(
      self,
      report: Report,
      create_mocked_request: AliasCreateMockedRequest,
  ) -> None:
    mocked_request = create_mocked_request({self.query_param: "true"})
    serialized = ReportSerializer(report, context={'request': mocked_request})

    qs = report.item.all().order_by(*ReportSerializer.ITEM_FIELD_ORDERING)
    qs = qs.prefetch_related(
        Prefetch(
            'scraper_config',
            queryset=ScraperConfig.objects.filter(is_active=True),
        )
    )

    assert serialized.data == {
        "id": report.id,
        "name": report.name,
        "item": ItemSerializer(qs, many=True).data,
        "store": StoreSerializer(
            report.store,
            many=True,
        ).data,
        "is_testing_only": report.is_testing_only,
    }

  def test_serialization__disabled_scrapers__correct_representation(
      self,
      report: Report,
      create_mocked_request: AliasCreateMockedRequest,
  ) -> None:
    mocked_request = create_mocked_request({self.query_param: "false"})
    serialized = ReportSerializer(report, context={'request': mocked_request})

    qs = report.item.all().order_by(*ReportSerializer.ITEM_FIELD_ORDERING)
    qs = qs.prefetch_related(
        Prefetch(
            'scraper_config',
            queryset=ScraperConfig.objects.filter(is_active=False),
        )
    )

    assert serialized.data == {
        "id": report.id,
        "name": report.name,
        "item": ItemSerializer(qs, many=True).data,
        "store": StoreSerializer(
            report.store,
            many=True,
        ).data,
        "is_testing_only": report.is_testing_only,
    }
