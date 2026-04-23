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

from .forms import ServiceForm
from .models import Service


class ServiceListView(LoginRequiredMixin, ListView):
    model = Service
    template_name = "services/service_list.html"
    context_object_name = "services"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("wedding")
        q = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        status = self.request.GET.get("status", "").strip()
        if q:
            qs = qs.filter(
                Q(name__icontains=q)
                | Q(provider__icontains=q)
                | Q(notes__icontains=q)
            )
        if category:
            qs = qs.filter(category=category)
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["category"] = self.request.GET.get("category", "")
        ctx["status"] = self.request.GET.get("status", "")
        ctx["category_choices"] = Service.Category.choices
        ctx["status_choices"] = Service.Status.choices
        return ctx


class ServiceDetailView(LoginRequiredMixin, DetailView):
    model = Service
    template_name = "services/service_detail.html"
    context_object_name = "service"


class ServiceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = "services/service_form.html"
    success_message = "Service created successfully."

    def get_initial(self):
        initial = super().get_initial()
        wedding_id = self.request.GET.get("wedding")
        if wedding_id:
            initial["wedding"] = wedding_id
        return initial


class ServiceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = "services/service_form.html"
    success_message = "Service updated successfully."


class ServiceDeleteView(LoginRequiredMixin, DeleteView):
    model = Service
    template_name = "services/service_confirm_delete.html"
    success_url = reverse_lazy("services:list")

    def form_valid(self, form):
        messages.success(self.request, "Service deleted successfully.")
        return super().form_valid(form)
