"""Serializer for Store instances in Report model summaries."""

from rest_framework import serializers
from stores.models import Store


class ReportSummaryStoreSerializer(serializers.ModelSerializer):
  """Serializer for Store instances in Report model summaries."""

  franchise_name = serializers.CharField(source='franchise.name')

  class Meta:
    model = Store
    fields = ('id', 'franchise_name')
