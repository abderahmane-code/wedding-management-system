"""Forms for registration + profile edit."""
from __future__ import annotations

import io

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from core.forms import StyledModelForm, _apply_form_control

from .models import Profile


# Images uploaded beyond this edge length are downscaled (preserving aspect
# ratio). Keeps the `media/` directory small and the Browse grid snappy.
MAX_PHOTO_EDGE = 800
MAX_PHOTO_BYTES = 5 * 1024 * 1024  # 5 MB hard limit on the upload itself
ALLOWED_PHOTO_FORMATS = {"JPEG", "PNG", "WEBP"}


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
            "bio": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Tell others a bit about yourself."}
            ),
        }

    def clean_profile_picture(self):
        photo = self.cleaned_data.get("profile_picture")
        if not photo or not hasattr(photo, "size"):
            return photo
        if photo.size > MAX_PHOTO_BYTES:
            raise forms.ValidationError(
                f"File is too large ({photo.size // 1024} KB). Max is "
                f"{MAX_PHOTO_BYTES // 1024 // 1024} MB."
            )
        return photo

    def save(self, commit: bool = True) -> Profile:
        """Resize profile_picture (if newly uploaded) before saving.

        Pillow is imported lazily so test-only flows that never touch photos
        don't pay the import cost, and so `pip install` failures for Pillow
        don't break unrelated profile edits.
        """
        profile: Profile = super().save(commit=False)
        photo = self.cleaned_data.get("profile_picture")

        # hasattr(photo, "file") is True only for newly-uploaded files;
        # existing FieldFiles loaded from the DB lack a fresh `.file` attr we
        # want to reprocess.
        if photo and hasattr(photo, "content_type"):
            try:
                resized = _resize_image(photo)
            except _InvalidImage as exc:
                self.add_error("profile_picture", str(exc))
                raise forms.ValidationError(str(exc))
            if resized is not None:
                profile.profile_picture = resized

        if commit:
            profile.save()
            self.save_m2m()
        return profile


class _InvalidImage(Exception):
    """Raised when an uploaded profile picture is unreadable."""


def _resize_image(upload):
    """Return a ContentFile with the resized JPEG, or ``None`` to keep original.

    Returning ``None`` signals "the upload is already small enough, leave it
    alone so Django's default storage handling takes over".
    """
    try:
        from PIL import Image, UnidentifiedImageError
    except ImportError:
        # Pillow missing — skip resize gracefully so profile edit still works.
        return None

    try:
        upload.seek(0)
        img = Image.open(upload)
        img.load()
    except (UnidentifiedImageError, OSError, ValueError):
        raise _InvalidImage("Couldn't read this file as an image. Try JPEG or PNG.")

    fmt = (img.format or "").upper()
    if fmt not in ALLOWED_PHOTO_FORMATS:
        raise _InvalidImage(
            f"Unsupported image format '{fmt or 'unknown'}'. Use JPEG, PNG, or WEBP."
        )

    # Normalize to RGB so the output is always a safe JPEG.
    if img.mode not in ("RGB", "L"):
        img = img.convert("RGB")

    w, h = img.size
    if max(w, h) <= MAX_PHOTO_EDGE:
        # Don't rewrite the file; keep the original upload.
        upload.seek(0)
        return None

    img.thumbnail((MAX_PHOTO_EDGE, MAX_PHOTO_EDGE), Image.LANCZOS)
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG", quality=88, optimize=True)
    buffer.seek(0)
    # Keep the original filename but force .jpg extension for the resized copy.
    original_name = getattr(upload, "name", "profile.jpg")
    stem = original_name.rsplit(".", 1)[0] or "profile"
    return ContentFile(buffer.read(), name=f"{stem}.jpg")
