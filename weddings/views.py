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

from .forms import WeddingForm
from .models import Wedding


class WeddingListView(LoginRequiredMixin, ListView):
    model = Wedding
    template_name = "weddings/wedding_list.html"
    context_object_name = "weddings"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        status = self.request.GET.get("status", "").strip()
        if q:
            qs = qs.filter(
                Q(bride_name__icontains=q)
                | Q(groom_name__icontains=q)
                | Q(location__icontains=q)
            )
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["status"] = self.request.GET.get("status", "")
        ctx["status_choices"] = Wedding.Status.choices
        return ctx


class WeddingDetailView(LoginRequiredMixin, DetailView):
    model = Wedding
    template_name = "weddings/wedding_detail.html"
    context_object_name = "wedding"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        wedding = self.object
        ctx["clients"] = wedding.clients.all()
        ctx["guests"] = wedding.guests.all()
        ctx["services"] = wedding.services.all()
        ctx["payments"] = wedding.payments.select_related("service").all()
        ctx["events"] = wedding.events.all()
        return ctx


class WeddingCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Wedding
    form_class = WeddingForm
    template_name = "weddings/wedding_form.html"
    success_message = "Wedding created successfully."


class WeddingUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Wedding
    form_class = WeddingForm
    template_name = "weddings/wedding_form.html"
    success_message = "Wedding updated successfully."


class WeddingDeleteView(LoginRequiredMixin, DeleteView):
    model = Wedding
    template_name = "weddings/wedding_confirm_delete.html"
    success_url = reverse_lazy("weddings:list")

    def form_valid(self, form):
        messages.success(self.request, "Wedding deleted successfully.")
        return super().form_valid(form)
