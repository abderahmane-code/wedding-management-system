from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import GuestForm
from .models import Guest


class GuestListView(LoginRequiredMixin, ListView):
    model = Guest
    template_name = "guests/guest_list.html"
    context_object_name = "guests"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("wedding")
        q = self.request.GET.get("q", "").strip()
        rsvp = self.request.GET.get("rsvp", "").strip()
        if q:
            qs = qs.filter(
                Q(full_name__icontains=q)
                | Q(phone__icontains=q)
                | Q(email__icontains=q)
            )
        if rsvp:
            qs = qs.filter(rsvp_status=rsvp)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["rsvp"] = self.request.GET.get("rsvp", "")
        ctx["rsvp_choices"] = Guest.RSVPStatus.choices
        return ctx


class GuestDetailView(LoginRequiredMixin, DetailView):
    model = Guest
    template_name = "guests/guest_detail.html"
    context_object_name = "guest"


class GuestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Guest
    form_class = GuestForm
    template_name = "guests/guest_form.html"
    success_message = "Guest created successfully."

    def get_initial(self):
        initial = super().get_initial()
        wedding_id = self.request.GET.get("wedding")
        if wedding_id:
            initial["wedding"] = wedding_id
        return initial


class GuestUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Guest
    form_class = GuestForm
    template_name = "guests/guest_form.html"
    success_message = "Guest updated successfully."


class GuestDeleteView(LoginRequiredMixin, DeleteView):
    model = Guest
    template_name = "guests/guest_confirm_delete.html"
    success_url = reverse_lazy("guests:list")

    def form_valid(self, form):
        messages.success(self.request, "Guest deleted successfully.")
        return super().form_valid(form)
