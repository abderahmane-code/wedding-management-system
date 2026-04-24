"""Like + Match models for the matchmaking flow.

A ``Like`` is directional (``from_user`` likes ``to_user``). When the reverse
Like already exists, a ``Match`` row is created so both users can start
chatting. ``Match`` stores the pair with ``user_low.id < user_high.id`` so each
mutual pair collapses to a single row.
"""
from django.conf import settings
from django.db import models
from django.db.models import Q


class Like(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_given",
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="likes_received",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("from_user", "to_user"),
                name="unique_like_per_direction",
            ),
            models.CheckConstraint(
                check=~Q(from_user=models.F("to_user")),
                name="cannot_like_self",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.from_user} → {self.to_user}"


class MatchQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(Q(user_low=user) | Q(user_high=user))

    def between(self, user_a, user_b):
        low, high = _ordered(user_a, user_b)
        return self.filter(user_low=low, user_high=high)


def _ordered(user_a, user_b):
    """Sort a pair of users by pk so there's only one canonical Match row."""
    if user_a.pk == user_b.pk:
        raise ValueError("Match cannot contain the same user twice")
    if user_a.pk < user_b.pk:
        return user_a, user_b
    return user_b, user_a


class Match(models.Model):
    """A mutual like. Stored with ``user_low.id < user_high.id`` to deduplicate."""

    user_low = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches_as_low",
    )
    user_high = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matches_as_high",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MatchQuerySet.as_manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("user_low", "user_high"),
                name="unique_match_pair",
            ),
            models.CheckConstraint(
                check=Q(user_low__lt=models.F("user_high")),
                name="match_user_ids_ordered",
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Match<{self.user_low.username} ↔ {self.user_high.username}>"

    def other_user(self, user):
        """Return the other participant in this match."""
        return self.user_high if user == self.user_low else self.user_low

    def involves(self, user) -> bool:
        return user == self.user_low or user == self.user_high

    @classmethod
    def ensure_pair(cls, user_a, user_b):
        """Create (or fetch) the Match row for this unordered pair."""
        low, high = _ordered(user_a, user_b)
        match, _ = cls.objects.get_or_create(user_low=low, user_high=high)
        return match
