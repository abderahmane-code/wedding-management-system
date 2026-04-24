"""Chat messages between matched users.

Messages are attached to a :class:`matches.Match` (not directly to
``sender``/``receiver``). Binding to a Match makes the "only chat if matched"
rule expressible at the query level — if there's no Match there can't be a
Message.
"""
from django.conf import settings
from django.db import models


class Message(models.Model):
    match = models.ForeignKey(
        "matches.Match",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_sent",
    )
    content = models.TextField(max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=("match", "created_at")),
        ]

    def __str__(self) -> str:
        preview = (self.content or "")[:40]
        return f"{self.sender.username}: {preview}"

    @property
    def receiver(self):
        """Convenience: the other participant in the match."""
        return self.match.other_user(self.sender)
