"""Context processors shared across all templates."""
from django.urls import reverse


def sidebar_nav(request):
    """Build the sidebar navigation config so templates can render it consistently.

    Each item is ``{"label": str, "url": str, "icon": str, "match": str}``
    where ``match`` is the URL path prefix used to highlight the active link.
    """
    items = [
        {"label": "Dashboard", "url": reverse("core:dashboard"), "icon": "home", "match": "/dashboard"},
        {"label": "Weddings", "url": reverse("weddings:list"), "icon": "heart", "match": "/weddings"},
        {"label": "Clients", "url": reverse("clients:list"), "icon": "users", "match": "/clients"},
        {"label": "Guests", "url": reverse("guests:list"), "icon": "user-check", "match": "/guests"},
        {"label": "Services", "url": reverse("services:list"), "icon": "gift", "match": "/services"},
        {"label": "Payments", "url": reverse("payments:list"), "icon": "credit-card", "match": "/payments"},
        {"label": "Planning", "url": reverse("planning:list"), "icon": "calendar", "match": "/planning"},
    ]
    matchmaking_items = [
        {"label": "Browse", "url": reverse("profiles:browse"), "icon": "search", "match": "/profiles/browse"},
        {"label": "Matches", "url": reverse("matches:list"), "icon": "spark", "match": "/matches"},
        {"label": "Chat", "url": reverse("chat:list"), "icon": "message", "match": "/chat"},
        {"label": "My profile", "url": reverse("profiles:self"), "icon": "user", "match": "/profiles/me"},
    ]
    return {"sidebar_items": items, "sidebar_matchmaking_items": matchmaking_items}
