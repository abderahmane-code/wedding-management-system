from django.db import models
from django.urls import reverse


class Client(models.Model):
    class Role(models.TextChoices):
        BRIDE = "bride", "Bride"
        GROOM = "groom", "Groom"
        PARENT = "parent", "Parent"
        PLANNER = "planner", "Planner"
        OTHER = "other", "Other"

    wedding = models.ForeignKey(
        "weddings.Wedding",
        on_delete=models.CASCADE,
        related_name="clients",
    )
    full_name = models.CharField(max_length=150)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.OTHER)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self) -> str:
        return self.full_name

    def get_absolute_url(self) -> str:
        return reverse("clients:detail", args=[self.pk])
