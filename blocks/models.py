"""Block model — unilateral block from one user to another.

A ``Block`` hides the target user from Browse, prevents them from viewing
the blocker's profile page, and makes any chat thread between the pair
inaccessible.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Q


class BlockQuerySet(models.QuerySet):
    def users_blocked_either_way(self, user) -> set[int]:
        """Return the set of user IDs involved in any block with ``user``."""
        rows = self.filter(Q(from_user=user) | Q(to_user=user)).values_list(
            "from_user_id", "to_user_id"
        )
        ids: set[int] = set()
        for from_id, to_id in rows:
            ids.add(from_id if from_id != user.pk else to_id)
        return ids

    def are_blocked(self, user_a, user_b) -> bool:
        """True if *either* user has blocked the other."""
        return self.filter(
            Q(from_user=user_a, to_user=user_b) | Q(from_user=user_b, to_user=user_a)
        ).exists()


class Block(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks_given",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blocks_received",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = BlockQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("from_user", "to_user"),
                name="unique_block_per_direction",
            ),
            models.CheckConstraint(
                check=~Q(from_user=models.F("to_user")),
                name="cannot_block_self",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.from_user} ⛔ {self.to_user}"
