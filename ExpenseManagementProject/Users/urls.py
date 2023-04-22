from django.urls import path
from ..User.views import *

app_name = "users"

urlpatterns = [
    path("register",registerView.as_view(),name="register"),
    path("login",loginView.as_view(),name="login"),
    path("user",userView.as_view(),name="user"),
    path("logout",logoutView.as_view(),name="logout")
]