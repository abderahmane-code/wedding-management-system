from django import forms

from core.forms import StyledModelForm

from .models import PlanningEvent


class PlanningEventForm(StyledModelForm):
    class Meta:
        model = PlanningEvent
        fields = ["wedding", "title", "date", "time", "location", "notes"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time": forms.TimeInput(attrs={"type": "time"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
