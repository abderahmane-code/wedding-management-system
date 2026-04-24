"""Block / unblock endpoints + block list."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from .models import Block


class BlockListView(LoginRequiredMixin, ListView):
    """The current user's list of blocked people, with unblock buttons."""

    model = Block
    template_name = "blocks/list.html"
    context_object_name = "blocks"

    def get_queryset(self):
        return (
            Block.objects.filter(from_user=self.request.user)
            .select_related("to_user__profile")
            .order_by("-created_at")
        )


class BlockUserView(LoginRequiredMixin, View):
    """POST /blocks/<user_id>/block/ — block another user."""

    def post(self, request, user_id: int):
        if request.user.pk == user_id:
            raise Http404("Cannot block yourself.")
        target = get_object_or_404(User, pk=user_id)
        Block.objects.get_or_create(from_user=request.user, to_user=target)
        messages.success(request, f"Blocked {target.username}. They're hidden from Browse now.")
        next_url = request.POST.get("next") or reverse("blocks:list")
        return redirect(next_url)


class UnblockUserView(LoginRequiredMixin, View):
    """POST /blocks/<user_id>/unblock/ — remove an existing block."""

    def post(self, request, user_id: int):
        target = get_object_or_404(User, pk=user_id)
        Block.objects.filter(from_user=request.user, to_user=target).delete()
        messages.success(request, f"Unblocked {target.username}.")
        next_url = request.POST.get("next") or reverse("blocks:list")
        return redirect(next_url)
