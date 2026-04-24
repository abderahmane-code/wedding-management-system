"""Forms for registration + profile edit."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from core.forms import StyledModelForm, _apply_form_control

from .models import Profile


class RegisterForm(UserCreationForm):
    """Standard Django signup form, but with our styled widgets + email."""

    email = forms.EmailField(required=False, help_text="Optional.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            _apply_form_control(field.widget)


class ProfileForm(StyledModelForm):
    class Meta:
        model = Profile
        fields = (
            "age",
            "city",
            "bio",
            "profile_picture",
            "show_age",
            "show_city",
            "show_bio",
            "show_photo",
            "is_discoverable",
        )
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell others a bit about yourself."}),
        }
