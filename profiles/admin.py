from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "age", "is_discoverable", "updated_at")
    list_filter = ("is_discoverable", "show_age", "show_city", "show_bio", "show_photo")
    search_fields = ("user__username", "user__first_name", "user__last_name", "city")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at", "updated_at")
