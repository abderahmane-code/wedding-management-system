"""URL configuration for wedding_project."""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include(("accounts.urls", "accounts"), namespace="accounts")),
    path("weddings/", include(("weddings.urls", "weddings"), namespace="weddings")),
    path("clients/", include(("clients.urls", "clients"), namespace="clients")),
    path("guests/", include(("guests.urls", "guests"), namespace="guests")),
    path("services/", include(("services.urls", "services"), namespace="services")),
    path("payments/", include(("payments.urls", "payments"), namespace="payments")),
    path("planning/", include(("planning.urls", "planning"), namespace="planning")),
    path("", include(("core.urls", "core"), namespace="core")),
]


# Branding for the Django admin
admin.site.site_header = "Wedding Management System — Admin"
admin.site.site_title = "Wedding Management Admin"
admin.site.index_title = "Administration"
