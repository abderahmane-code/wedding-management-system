"""Profile for matchmaking users."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """A matchmaking profile attached to a Django auth User.

    Privacy flags control what other users see on the Browse page *before*
    a mutual like creates a Match. After a Match, every field is revealed.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    age = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(120)],
    )
    city = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )

    # Privacy: control which fields other users see before a match.
    show_age = models.BooleanField(default=True)
    show_city = models.BooleanField(default=True)
    show_bio = models.BooleanField(default=True)
    show_photo = models.BooleanField(default=True)
    is_discoverable = models.BooleanField(
        default=True,
        help_text="Uncheck to hide your profile from Browse entirely.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Profile<{self.user.username}>"

    @property
    def display_name(self) -> str:
        return self.user.get_full_name() or self.user.username

    def public_view(self, matched: bool) -> dict:
        """Return the viewer-facing dict for this profile given match state.

        Every key is always present so templates can distinguish between
        "field empty" and "field hidden by a privacy flag" via the ``*_hidden``
        booleans — which is what powers the "Bio hidden until you match."
        muted indicator.
        """
        age_visible = matched or self.show_age
        city_visible = matched or self.show_city
        bio_visible = matched or self.show_bio
        photo_visible = matched or self.show_photo
        photo_url = (
            self.profile_picture.url
            if photo_visible and self.profile_picture
            else ""
        )
        return {
            "display_name": self.display_name,
            "age": self.age if age_visible else None,
            "age_hidden": not age_visible,
            "city": self.city if city_visible else "",
            "city_hidden": not city_visible,
            "bio": self.bio if bio_visible else "",
            "bio_hidden": not bio_visible,
            "photo": photo_url,
            "photo_hidden": not photo_visible,
        }


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """Auto-create an empty profile whenever a new User is created."""
    if created:
        Profile.objects.get_or_create(user=instance)
