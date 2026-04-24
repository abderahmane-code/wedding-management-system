from django.urls import path

from . import views


urlpatterns = [
    path("", views.ChatListView.as_view(), name="list"),
    path("<int:match_id>/", views.ChatThreadView.as_view(), name="thread"),
]
