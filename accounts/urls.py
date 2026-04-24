from django.contrib.auth import views as auth_views
from django.urls import path

from profiles.views import RegisterView


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    # Registration is logically owned by the profiles app, but exposed at
    # /accounts/register/ as requested.
    path("register/", RegisterView.as_view(), name="register"),
]
