from django.contrib import admin

from .models import Service


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "provider", "price", "status", "wedding")
    list_filter = ("category", "status", "wedding")
    search_fields = ("name", "provider", "notes")
    autocomplete_fields = ("wedding",)
