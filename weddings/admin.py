from django.contrib import admin

from .models import Wedding


@admin.register(Wedding)
class WeddingAdmin(admin.ModelAdmin):
    list_display = (
        "couple",
        "wedding_date",
        "location",
        "status",
        "total_budget",
        "total_paid",
    )
    list_filter = ("status", "wedding_date")
    search_fields = ("bride_name", "groom_name", "location")
    date_hierarchy = "wedding_date"
    ordering = ("-wedding_date",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Couple", {"fields": ("bride_name", "groom_name")}),
        (
            "Event",
            {"fields": ("wedding_date", "location", "status", "total_budget")},
        ),
        ("Notes", {"fields": ("notes",)}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
