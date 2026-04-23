from django import forms

from core.forms import StyledModelForm

from .models import Payment


class PaymentForm(StyledModelForm):
    class Meta:
        model = Payment
        fields = ["wedding", "service", "amount", "payment_date", "method", "notes"]
        widgets = {
            "payment_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
