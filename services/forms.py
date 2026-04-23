from django import forms

from core.forms import StyledModelForm

from .models import Service


class ServiceForm(StyledModelForm):
    class Meta:
        model = Service
        fields = [
            "wedding",
            "name",
            "category",
            "provider",
            "price",
            "status",
            "notes",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
