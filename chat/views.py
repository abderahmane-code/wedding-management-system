"""Chat: list threads (one per match) + thread detail with send form."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView

from matches.models import Match

from .forms import MessageForm
from .models import Message

try:
    from blocks.models import Block
except ImportError:  # pragma: no cover
    Block = None


class ChatListView(LoginRequiredMixin, ListView):
    template_name = "chat/list.html"
    context_object_name = "threads"

    def get_queryset(self):
        user = self.request.user
        qs = (
            Match.objects.for_user(user)
            .select_related("user_low__profile", "user_high__profile")
            .prefetch_related("messages")
            .order_by("-created_at")
        )
        threads = []
        for match in qs:
            other = match.other_user(user)
            last = match.messages.order_by("-created_at").first()
            unread = match.messages.filter(read_at__isnull=True).exclude(sender=user).count()
            threads.append(
                {"match": match, "other": other, "last": last, "unread": unread}
            )
        return threads


class ChatThreadView(LoginRequiredMixin, DetailView):
    model = Match
    pk_url_kwarg = "match_id"
    template_name = "chat/thread.html"
    context_object_name = "match"

    def get_queryset(self):
        return Match.objects.for_user(self.request.user).select_related(
            "user_low__profile", "user_high__profile"
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self._blocked(self.object):
            raise Http404("Chat unavailable.")
        return super().get(request, *args, **kwargs)

    def _blocked(self, match: Match) -> bool:
        if Block is None:
            return False
        return Block.objects.are_blocked(
            self.request.user, match.other_user(self.request.user)
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        match: Match = ctx["match"]
        user = self.request.user

        # Mark incoming unread messages as read
        match.messages.filter(read_at__isnull=True).exclude(sender=user).update(
            read_at=timezone.now()
        )

        ctx["other"] = match.other_user(user)
        ctx["messages_list"] = list(match.messages.select_related("sender").all())
        ctx["form"] = MessageForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        match: Match = self.object
        if not match.involves(request.user):
            raise Http404("Not your match.")
        if self._blocked(match):
            raise Http404("Chat unavailable.")
        form = MessageForm(request.POST)
        if form.is_valid():
            Message.objects.create(
                match=match,
                sender=request.user,
                content=form.cleaned_data["content"],
            )
            return redirect("chat:thread", match_id=match.id)

        ctx = self.get_context_data()
        ctx["form"] = form
        return self.render_to_response(ctx)
