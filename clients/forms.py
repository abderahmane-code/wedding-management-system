from django import forms

from core.forms import StyledModelForm

from .models import Client


class ClientForm(StyledModelForm):
    class Meta:
        model = Client
        fields = ["wedding", "full_name", "role", "phone", "email", "address", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
