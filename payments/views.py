from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import PaymentForm
from .models import Payment


class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = "payments/payment_list.html"
    context_object_name = "payments"
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset().select_related("wedding", "service")
        wedding_id = self.request.GET.get("wedding", "").strip()
        method = self.request.GET.get("method", "").strip()
        if wedding_id:
            qs = qs.filter(wedding_id=wedding_id)
        if method:
            qs = qs.filter(method=method)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        total = self.get_queryset().aggregate(total=Sum("amount"))["total"]
        ctx["total_amount"] = total or Decimal("0.00")
        ctx["wedding"] = self.request.GET.get("wedding", "")
        ctx["method"] = self.request.GET.get("method", "")
        ctx["method_choices"] = Payment.Method.choices
        return ctx


class PaymentDetailView(LoginRequiredMixin, DetailView):
    model = Payment
    template_name = "payments/payment_detail.html"
    context_object_name = "payment"


class PaymentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    success_message = "Payment recorded successfully."

    def get_initial(self):
        initial = super().get_initial()
        wedding_id = self.request.GET.get("wedding")
        if wedding_id:
            initial["wedding"] = wedding_id
        return initial


class PaymentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Payment
    form_class = PaymentForm
    template_name = "payments/payment_form.html"
    success_message = "Payment updated successfully."


class PaymentDeleteView(LoginRequiredMixin, DeleteView):
    model = Payment
    template_name = "payments/payment_confirm_delete.html"
    success_url = reverse_lazy("payments:list")

    def form_valid(self, form):
        messages.success(self.request, "Payment deleted successfully.")
        return super().form_valid(form)
