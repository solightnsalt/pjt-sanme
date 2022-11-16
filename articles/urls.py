from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("main/", views.main, name="main"),
    path("board/", views.board, name="board"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comment/", views.comment, name="comment"),
    path(
        "<int:pk>/comment_delete/<int:comment_pk>",
        views.comment_delete,
        name="comment_delete",
    ),
    path(
        "<int:pk>/comment_update/<int:comment_pk>",
        views.comment_update,
        name="comment_update",
    ),
    path("<int:pk>/participate/", views.participate, name="participate"),
    path("<int:pk>/recommend/", views.recommend, name="recommend"),
]
