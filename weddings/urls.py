from django.urls import path

from . import views


urlpatterns = [
    path("", views.WeddingListView.as_view(), name="list"),
    path("new/", views.WeddingCreateView.as_view(), name="create"),
    path("<int:pk>/", views.WeddingDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.WeddingUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.WeddingDeleteView.as_view(), name="delete"),
]
