"""Report model."""

from django.db import models
from django.db.models.functions import Lower
from utilities.models.bases.model_base import ModelBase
from utilities.models.fields.title import TitleField

CONSTRAINT_NAMES = {'name': 'Report name must be unique'}


class Report(
    ModelBase,
):
  """Report model."""

  class Meta:
    constraints = [
        models.UniqueConstraint(
            Lower('name'),
            name=CONSTRAINT_NAMES['name'],
        ),
    ]

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

  is_testing = models.BooleanField(default=False)

  def __str__(self) -> str:
    return self.name
