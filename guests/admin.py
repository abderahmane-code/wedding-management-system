from django.contrib import admin

from .models import Guest


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("full_name", "rsvp_status", "plus_ones", "phone", "wedding")
    list_filter = ("rsvp_status", "wedding")
    search_fields = ("full_name", "phone", "email")
    autocomplete_fields = ("wedding",)
