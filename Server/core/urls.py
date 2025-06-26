from django.urls import path
from .views import register_user, login_user, check_text , message , Report

urlpatterns = [
    path("register/", register_user),
    path("login/", login_user),
    path("check/", check_text),
    path("message/" , message),
    path('api/reports/<str:uni_id>/', views.get_reports, name='get_reports'),
    # path('registerapp' , register_app )
]
