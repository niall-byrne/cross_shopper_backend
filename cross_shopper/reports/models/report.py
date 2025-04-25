"""Report model."""

from django.db import models
from utilities.models.bases.base_model import BaseModel
from utilities.models.fields.title import TitleField


class Report(
    BaseModel,
):
  """Report model."""

  name = TitleField(
      max_length=80,
      blank=False,
  )
  item = models.ManyToManyField('items.Item')
  store = models.ManyToManyField(
      'stores.Store',
      through='reports.ReportStore',
  )
  user = models.ForeignKey(
      'auth.User',
      on_delete=models.PROTECT,
  )

  is_testing_only = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.name
