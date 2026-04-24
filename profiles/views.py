"""Views: registration, self profile, edit, browse, detail."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView

from matches.models import Like, Match

from .forms import ProfileForm, RegisterForm
from .models import Profile


class RegisterView(CreateView):
    """Public user registration — creates a User (Profile auto-created via signal)."""

    form_class = RegisterForm
    template_name = "profiles/register.html"
    success_url = reverse_lazy("profiles:edit")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Welcome! Finish your profile to start browsing.")
        return response


class ProfileSelfView(LoginRequiredMixin, TemplateView):
    template_name = "profiles/self.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        ctx["profile"] = profile
        return ctx


class ProfileEditView(LoginRequiredMixin, UpdateView):
    form_class = ProfileForm
    template_name = "profiles/edit.html"
    success_url = reverse_lazy("profiles:self")

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Profile updated.")
        return super().form_valid(form)


class BrowseView(LoginRequiredMixin, ListView):
    template_name = "profiles/browse.html"
    context_object_name = "cards"
    paginate_by = 12

    def get_queryset(self):
        user = self.request.user
        qs = (
            Profile.objects.select_related("user")
            .filter(is_discoverable=True)
            .exclude(user=user)
        )
        city = self.request.GET.get("city", "").strip()
        if city:
            qs = qs.filter(city__icontains=city)

        liked_ids = set(Like.objects.filter(from_user=user).values_list("to_user_id", flat=True))
        matched_ids = set(
            Match.objects.for_user(user).values_list("user_low_id", flat=True)
        ) | set(
            Match.objects.for_user(user).values_list("user_high_id", flat=True)
        )

        # Remove users this user has already liked or already matched with
        qs = qs.exclude(user_id__in=liked_ids | matched_ids)

        cards = []
        for profile in qs.order_by("-updated_at")[:200]:
            cards.append({"profile": profile, "view": profile.public_view(matched=False)})
        return cards

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["city_filter"] = self.request.GET.get("city", "").strip()
        return ctx


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = "other"
    template_name = "profiles/detail.html"

    def get_queryset(self):
        return User.objects.select_related("profile")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        other: User = ctx["other"]
        if other == self.request.user:
            raise Http404("Use your own profile page instead.")

        # Check match state
        matched = Match.objects.between(self.request.user, other).exists()
        try:
            other_profile = other.profile
        except Profile.DoesNotExist:
            other_profile = Profile.objects.create(user=other)
        if not other_profile.is_discoverable and not matched:
            raise Http404("Profile not available.")

        ctx["matched"] = matched
        ctx["view"] = other_profile.public_view(matched=matched)
        ctx["already_liked"] = Like.objects.filter(
            from_user=self.request.user, to_user=other
        ).exists()
        ctx["other_profile"] = other_profile
        return ctx
