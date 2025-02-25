"""
models.py
Ian Kollipara <ian.kollipara@cune.edu>
2025-02-25

Todo Model
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class TodoQuerySet(models.QuerySet["Todo"]):
    def incomplete(self):
        return self.filter(completed_at__isnull=True)


class Todo(models.Model):
    """Todo model."""

    title = models.CharField(_("title"), max_length=255)
    completed_at = models.DateTimeField(_("completed At"), null=True, blank=True)
    description = models.TextField(_("description"))

    objects: TodoQuerySet = TodoQuerySet.as_manager()

    @property
    def is_complete(self) -> bool:
        """Check if the given todo is complete."""
        return self.completed_at is not None

    def __str__(self):
        return f"{self.title} [{'X' if self.is_complete else ' '}]"

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("todo_detail", kwargs={"pk": self.pk})
