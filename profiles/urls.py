from django.urls import path

from . import views


urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("me/", views.ProfileSelfView.as_view(), name="self"),
    path("me/edit/", views.ProfileEditView.as_view(), name="edit"),
    path("browse/", views.BrowseView.as_view(), name="browse"),
    path("<int:pk>/", views.ProfileDetailView.as_view(), name="detail"),
]
