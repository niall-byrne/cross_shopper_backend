"""ReportStore model."""

from django.db import models
from utilities.models.bases.base_model import BaseModel


class ReportStore(
    BaseModel,
):
  """ReportStore model."""

  report = models.ForeignKey(
      'reports.Report',
      on_delete=models.PROTECT,
  )
  store = models.ForeignKey(
      'stores.Store',
      on_delete=models.PROTECT,
  )

  def __str__(self) -> str:
    return f"{str(self.store)}"
