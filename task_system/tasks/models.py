import enum
from django.conf import settings
from django.db import models
from django.utils.functional import cached_property

from task_system.users.models import Creator, Performer


class TaskStatus(enum.IntEnum):
    OPEN = 0
    IN_PROGRESS = 10
    COMPLETED = 20
    WONT_BE_COMPLETED = 30
    CLOSED = 40
    DELETED = 50


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.PositiveIntegerField(
        default=None,
        choices=[(x.value, x.name) for x in TaskStatus],
        null=True,
        blank=True,
    )  # статус задачи
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, db_index=True
    )
    closed_at = models.DateTimeField(default=None, null=True, blank=True)
    enable = models.BooleanField(default=False, db_index=True)
    created_by = models.ForeignKey(
        Creator,
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )
    performer = models.ForeignKey(
        Performer,
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return str(f"{self.name} ")

    @cached_property
    def comments(self):
        return self.task_comments.all().order_by("id")


class TaskComment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="task_comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    text = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )