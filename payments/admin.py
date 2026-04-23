from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("wedding", "service", "amount", "method", "payment_date")
    list_filter = ("method", "payment_date", "wedding")
    search_fields = ("notes",)
    autocomplete_fields = ("wedding", "service")
    date_hierarchy = "payment_date"
