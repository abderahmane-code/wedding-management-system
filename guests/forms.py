from django import forms

from core.forms import StyledModelForm

from .models import Guest


class GuestForm(StyledModelForm):
    class Meta:
        model = Guest
        fields = [
            "wedding",
            "full_name",
            "phone",
            "email",
            "rsvp_status",
            "plus_ones",
            "notes",
        ]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
