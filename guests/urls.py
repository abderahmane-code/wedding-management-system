from django.urls import path

from . import views


urlpatterns = [
    path("", views.GuestListView.as_view(), name="list"),
    path("new/", views.GuestCreateView.as_view(), name="create"),
    path("<int:pk>/", views.GuestDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.GuestUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.GuestDeleteView.as_view(), name="delete"),
]
