from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("detail/<int:pk>/", views.detail, name="detail"),
    path("update/<int:pk>/", views.update, name="update"),
    path("logout/", views.logout, name="logout"),
]
