from django.contrib import admin

from .models import Block


@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("from_user__username", "to_user__username")
    autocomplete_fields = ("from_user", "to_user")
    date_hierarchy = "created_at"
