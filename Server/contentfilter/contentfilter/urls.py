from django.contrib import admin
from django.urls import path
from filter import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.register, name='register'),  
    path('api/login/', views.login, name='login'),           
    path('api/analyze/', views.analyze_text, name='analyze'),
]