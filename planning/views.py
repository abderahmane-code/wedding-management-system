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

from .forms import PlanningEventForm
from .models import PlanningEvent


class PlanningEventListView(LoginRequiredMixin, ListView):
    model = PlanningEvent
    template_name = "planning/planningevent_list.html"
    context_object_name = "events"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("wedding")
        q = self.request.GET.get("q", "").strip()
        wedding_id = self.request.GET.get("wedding", "").strip()
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(location__icontains=q)
                | Q(notes__icontains=q)
            )
        if wedding_id:
            qs = qs.filter(wedding_id=wedding_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["wedding"] = self.request.GET.get("wedding", "")
        return ctx


class PlanningEventDetailView(LoginRequiredMixin, DetailView):
    model = PlanningEvent
    template_name = "planning/planningevent_detail.html"
    context_object_name = "event"


class PlanningEventCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = PlanningEvent
    form_class = PlanningEventForm
    template_name = "planning/planningevent_form.html"
    success_message = "Planning event created successfully."

    def get_initial(self):
        initial = super().get_initial()
        wedding_id = self.request.GET.get("wedding")
        if wedding_id:
            initial["wedding"] = wedding_id
        return initial


class PlanningEventUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = PlanningEvent
    form_class = PlanningEventForm
    template_name = "planning/planningevent_form.html"
    success_message = "Planning event updated successfully."


class PlanningEventDeleteView(LoginRequiredMixin, DeleteView):
    model = PlanningEvent
    template_name = "planning/planningevent_confirm_delete.html"
    success_url = reverse_lazy("planning:list")

    def form_valid(self, form):
        messages.success(self.request, "Planning event deleted successfully.")
        return super().form_valid(form)
