"""Test the ReportPricingSerializer class."""
import decimal
from unittest import mock

import pytest
from reports.models import Report
from reports.models.serializers.report_pricing import ReportPricingSerializer


@pytest.mark.django_db
class TestReportPricingSerializerSerializer:

  def test_serialization__without_pricing__correct_representation(
      self,
      report: Report,
      mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    mocked_aggregate_last_52_weeks_manager.average.return_value = None
    mocked_aggregate_last_52_weeks_manager.high.return_value = None
    mocked_aggregate_last_52_weeks_manager.low.return_value = None

    serialized = ReportPricingSerializer(
        report.item.first(),
        context={"report": report},
    )

    assert serialized.data == {
        "id": report.item.all()[0].pk,
        "name": str(report.item.all()[0]),
        'last_52_weeks_average': None,
        'last_52_weeks_high': None,
        'last_52_weeks_low': None,
    }

  def test_serialization__with_pricing__correct_representation(
      self,
      report: Report,
      mocked_aggregate_last_52_weeks_manager: mock.Mock,
  ) -> None:
    mocked_aggregate_last_52_weeks_manager.average.return_value = (
        decimal.Decimal('10.50')
    )
    mocked_aggregate_last_52_weeks_manager.high.return_value = (
        decimal.Decimal('20.50')
    )
    mocked_aggregate_last_52_weeks_manager.low.return_value = (
        decimal.Decimal('1.50')
    )

    serialized = ReportPricingSerializer(
        report.item.first(),
        context={"report": report},
    )

    assert serialized.data == {
        "id":
            report.item.all()[0].pk,
        "name":
            str(report.item.all()[0]),
        'last_52_weeks_average':
            str(mocked_aggregate_last_52_weeks_manager.average.return_value),
        'last_52_weeks_high':
            str(mocked_aggregate_last_52_weeks_manager.high.return_value),
        'last_52_weeks_low':
            str(mocked_aggregate_last_52_weeks_manager.low.return_value),
    }
