from django.urls import path

from . import views


urlpatterns = [
    path("", views.NotificationListView.as_view(), name="list"),
    path("mark-all-read/", views.MarkAllReadView.as_view(), name="mark_all_read"),
]
