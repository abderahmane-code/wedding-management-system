from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "role", "phone", "email", "wedding")
    list_filter = ("role", "wedding")
    search_fields = ("full_name", "phone", "email", "address")
    autocomplete_fields = ("wedding",)
