"""Serializer to retrieve or list Report model targets."""

from reports.models import Report
from rest_framework import serializers


class ReportTargetSerializerRO(serializers.ModelSerializer[Report]):
  """Serializer to retrieve or list Report model targets."""

  class Meta:
    model = Report
    fields = (
        "id",
        "name",
    )
