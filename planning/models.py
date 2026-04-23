from django.db import models
from django.urls import reverse


class PlanningEvent(models.Model):
    wedding = models.ForeignKey(
        "weddings.Wedding",
        on_delete=models.CASCADE,
        related_name="events",
    )
    title = models.CharField(max_length=150)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date", "time"]
        verbose_name = "Planning event"
        verbose_name_plural = "Planning events"

    def __str__(self) -> str:
        return f"{self.title} — {self.date:%Y-%m-%d}"

    def get_absolute_url(self) -> str:
        return reverse("planning:detail", args=[self.pk])
