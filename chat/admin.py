from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("match", "sender", "preview", "created_at", "read_at")
    list_filter = ("created_at",)
    search_fields = ("sender__username", "content")
    autocomplete_fields = ("match", "sender")
    date_hierarchy = "created_at"

    @admin.display(description="Content")
    def preview(self, obj):
        return (obj.content or "")[:60]
