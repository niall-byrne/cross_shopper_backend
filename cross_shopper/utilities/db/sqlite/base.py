"""A custom SQLite database wrapper."""

from django.db.backends.sqlite3 import base


class DatabaseWrapper(base.DatabaseWrapper):
  """Custom SQLite database wrapper for improved transaction concurrency."""

  def _start_transaction_under_autocommit(self) -> None:
    self.cursor().execute("BEGIN IMMEDIATE")
