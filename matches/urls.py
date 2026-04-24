from django.urls import path

from . import views


urlpatterns = [
    path("", views.MatchListView.as_view(), name="list"),
    path("like/<int:user_id>/", views.LikeUserView.as_view(), name="like"),
    path("unlike/<int:user_id>/", views.UnlikeUserView.as_view(), name="unlike"),
]
