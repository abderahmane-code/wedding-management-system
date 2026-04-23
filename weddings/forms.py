from django import forms

from core.forms import StyledModelForm

from .models import Wedding


class WeddingForm(StyledModelForm):
    class Meta:
        model = Wedding
        fields = [
            "bride_name",
            "groom_name",
            "wedding_date",
            "location",
            "status",
            "total_budget",
            "notes",
        ]
        widgets = {
            "wedding_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
