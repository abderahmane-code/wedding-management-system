from django.urls import path

from . import views


urlpatterns = [
    path("", views.PaymentListView.as_view(), name="list"),
    path("new/", views.PaymentCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PaymentDetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.PaymentUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PaymentDeleteView.as_view(), name="delete"),
]
