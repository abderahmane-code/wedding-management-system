from django.contrib import admin

from .models import PlanningEvent


@admin.register(PlanningEvent)
class PlanningEventAdmin(admin.ModelAdmin):
    list_display = ("title", "wedding", "date", "time", "location")
    list_filter = ("date", "wedding")
    search_fields = ("title", "location", "notes")
    autocomplete_fields = ("wedding",)
    date_hierarchy = "date"
