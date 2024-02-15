from django.urls import path
from . import views

app_name = "scoring_favorite"
urlpatterns = [
    path("add_score/", views.add_score, name="add_score"),
    path("add_to_favorite/", views.add_to_favorite, name="add_to_favorite"),
    path("favorit_user/", views.UserfavoritView.as_view(), name="favorit_user"),
]
