from django.urls import path

from . import views


urlpatterns = [
    path("", views.BlockListView.as_view(), name="list"),
    path("<int:user_id>/block/", views.BlockUserView.as_view(), name="block"),
    path("<int:user_id>/unblock/", views.UnblockUserView.as_view(), name="unblock"),
]
