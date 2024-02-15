from django.urls import path
from . import views

app_name = "comments"
urlpatterns = [
    path("create_comment/<slug:slug>/", views.CommentView.as_view(), name="create_comment")
]
