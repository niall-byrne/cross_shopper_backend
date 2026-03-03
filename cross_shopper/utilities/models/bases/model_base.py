"""Model base class for Cross Shopper."""

from typing import Any

from django.db import models


class ModelBase(models.Model):
  """Inherit from me."""

  class Meta:
    abstract = True

  def __repr__(self) -> str:
    return str(self.pk) + ":" + super().__repr__()

  def save(self, *args: Any, **kwargs: Any) -> None:
    """Clean and save model."""
    self.full_clean()
    super().save(*args, **kwargs)
