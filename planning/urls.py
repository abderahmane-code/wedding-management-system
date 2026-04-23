from django.urls import path

from . import views


urlpatterns = [
    path("", views.PlanningEventListView.as_view(), name="list"),
    path("new/", views.PlanningEventCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PlanningEventDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PlanningEventUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PlanningEventDeleteView.as_view(), name="delete"),
]
