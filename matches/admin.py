from django.contrib import admin

from .models import Like, Match


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("from_user", "to_user", "created_at")
    search_fields = ("from_user__username", "to_user__username")
    autocomplete_fields = ("from_user", "to_user")
    date_hierarchy = "created_at"


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("user_low", "user_high", "created_at")
    search_fields = ("user_low__username", "user_high__username")
    autocomplete_fields = ("user_low", "user_high")
    date_hierarchy = "created_at"
