from django.urls import path
from .views import register_user, login_user, check_text , message , get_report

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("check/", check_text),
    path("message/" , message),
 
    # path('registerapp' , register_app )
]
