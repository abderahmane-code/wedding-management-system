"""Match list + Like/Unlike POST endpoints."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, View

from .models import Like, Match

try:
    from blocks.models import Block
except ImportError:  # pragma: no cover
    Block = None

try:
    from notifications.models import Notification
except ImportError:  # pragma: no cover
    Notification = None


class MatchListView(LoginRequiredMixin, ListView):
    template_name = "matches/list.html"
    context_object_name = "entries"

    def get_queryset(self):
        user = self.request.user
        qs = (
            Match.objects.for_user(user)
            .select_related("user_low__profile", "user_high__profile")
            .order_by("-created_at")
        )
        entries = []
        for match in qs:
            other = match.other_user(user)
            last_msg = match.messages.order_by("-created_at").first()
            entries.append({"match": match, "other": other, "last_message": last_msg})
        return entries


class LikeUserView(LoginRequiredMixin, View):
    """POST /matches/like/<user_id>/ — create a Like and maybe a Match."""

    def post(self, request, user_id: int):
        if request.user.id == user_id:
            messages.error(request, "You can't like yourself.")
            return redirect("profiles:browse")

        target = get_object_or_404(User, pk=user_id)

        # Refuse to like across a block in either direction.
        if Block is not None and Block.objects.are_blocked(request.user, target):
            messages.error(request, "You can't like this person.")
            return redirect("profiles:browse")

        with transaction.atomic():
            try:
                Like.objects.create(from_user=request.user, to_user=target)
            except IntegrityError:
                # Already liked — just follow through to the reverse-like check
                pass

            reverse_like = Like.objects.filter(
                from_user=target, to_user=request.user
            ).exists()
            if reverse_like:
                match = Match.ensure_pair(request.user, target)
                _notify_match(request.user, target, match)
                messages.success(
                    request,
                    f"It's a match with {target.get_full_name() or target.username}!",
                )
                return redirect("matches:list")

        messages.success(request, "Like sent.")
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("profiles:browse")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])


def _notify_match(user_a, user_b, match) -> None:
    """Create a Notification row for each participant in a newly-created match."""
    if Notification is None:
        return
    chat_url = reverse("chat:thread", args=[match.id])
    for owner, other in ((user_a, user_b), (user_b, user_a)):
        other_name = other.get_full_name() or other.username
        Notification.objects.create(
            user=owner,
            kind=Notification.KIND_MATCH,
            title=f"It's a match with {other_name}!",
            body="You can now chat with each other.",
            url=chat_url,
        )


class UnlikeUserView(LoginRequiredMixin, View):
    """POST /matches/unlike/<user_id>/ — remove a like you sent (only if no match yet)."""

    def post(self, request, user_id: int):
        target = get_object_or_404(User, pk=user_id)
        matched = Match.objects.between(request.user, target).exists()
        if matched:
            messages.error(request, "You already matched — can't unlike from here.")
            return redirect("matches:list")
        deleted, _ = Like.objects.filter(
            from_user=request.user, to_user=target
        ).delete()
        if deleted:
            messages.info(request, "Like withdrawn.")
        return redirect("profiles:browse")

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
