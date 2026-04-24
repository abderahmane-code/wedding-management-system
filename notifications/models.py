"""In-app notifications for matchmaking events.

Kept intentionally simple: no realtime transport, no email — a notification
is just a row the user sees on ``/notifications/`` with a link to the
related object (match, message, etc.).
"""
from __future__ import annotations

from django.conf import settings
from django.db import models


class Notification(models.Model):
    KIND_MATCH = "match"
    KIND_LIKE = "like"
    KIND_MESSAGE = "message"
    KIND_CHOICES = [
        (KIND_MATCH, "New match"),
        (KIND_LIKE, "Received a like"),
        (KIND_MESSAGE, "New message"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    kind = models.CharField(max_length=16, choices=KIND_CHOICES)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=400, blank=True)
    # URL the item links to (a match detail, a chat thread, etc.).
    url = models.CharField(max_length=255, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=("user", "is_read", "-created_at")),
        ]

    def __str__(self) -> str:
        return f"{self.user.username}: {self.title}"
