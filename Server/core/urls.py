from django.urls import path
from .views import register_user, login_user, check_text

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("check/", check_text),
]
