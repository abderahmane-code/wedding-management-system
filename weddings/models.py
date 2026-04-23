from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils import timezone


class Wedding(models.Model):
    class Status(models.TextChoices):
        PLANNING = "planning", "Planning"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    bride_name = models.CharField(max_length=150)
    groom_name = models.CharField(max_length=150)
    wedding_date = models.DateField()
    location = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PLANNING
    )
    total_budget = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-wedding_date"]
        verbose_name = "Wedding"
        verbose_name_plural = "Weddings"

    def __str__(self) -> str:
        return f"{self.bride_name} & {self.groom_name} — {self.wedding_date:%Y-%m-%d}"

    def get_absolute_url(self) -> str:
        return reverse("weddings:detail", args=[self.pk])

    @property
    def couple(self) -> str:
        return f"{self.bride_name} & {self.groom_name}"

    @property
    def is_upcoming(self) -> bool:
        return self.wedding_date >= timezone.localdate()

    @property
    def total_paid(self) -> Decimal:
        total = self.payments.aggregate(total=Sum("amount"))["total"]
        return total or Decimal("0.00")

    @property
    def remaining_amount(self) -> Decimal:
        return Decimal(self.total_budget) - self.total_paid

    @property
    def total_services_cost(self) -> Decimal:
        total = self.services.aggregate(total=Sum("price"))["total"]
        return total or Decimal("0.00")

    @property
    def guests_confirmed_count(self) -> int:
        return self.guests.filter(rsvp_status="confirmed").count()
