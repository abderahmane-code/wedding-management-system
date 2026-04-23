from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import RedirectView, TemplateView

from clients.models import Client
from guests.models import Guest
from payments.models import Payment
from planning.models import PlanningEvent
from services.models import Service
from weddings.models import Wedding


class HomeRedirectView(RedirectView):
    """Send unauthenticated users to login, authenticated ones to dashboard."""

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return reverse("core:dashboard")
        return reverse("accounts:login")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "core/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        today = timezone.localdate()

        ctx["total_weddings"] = Wedding.objects.count()
        ctx["total_clients"] = Client.objects.count()
        ctx["total_guests"] = Guest.objects.count()
        ctx["total_services"] = Service.objects.count()
        ctx["total_payments"] = Payment.objects.count()

        payments_total = Payment.objects.aggregate(total=Sum("amount"))["total"]
        ctx["payments_total_amount"] = payments_total or Decimal("0.00")

        budgets_total = Wedding.objects.aggregate(total=Sum("total_budget"))["total"]
        ctx["budgets_total_amount"] = budgets_total or Decimal("0.00")
        ctx["remaining_amount"] = (
            ctx["budgets_total_amount"] - ctx["payments_total_amount"]
        )

        ctx["upcoming_weddings"] = (
            Wedding.objects.filter(wedding_date__gte=today)
            .order_by("wedding_date")[:5]
        )
        ctx["upcoming_events"] = (
            PlanningEvent.objects.filter(date__gte=today)
            .select_related("wedding")
            .order_by("date", "time")[:5]
        )
        ctx["recent_payments"] = (
            Payment.objects.select_related("wedding", "service")
            .order_by("-payment_date", "-created_at")[:5]
        )
        ctx["guests_confirmed"] = Guest.objects.filter(
            rsvp_status=Guest.RSVPStatus.CONFIRMED
        ).count()
        ctx["guests_pending"] = Guest.objects.filter(
            rsvp_status=Guest.RSVPStatus.PENDING
        ).count()
        return ctx
