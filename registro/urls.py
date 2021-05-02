from django.urls import path
from . import views

app_name = 'registro'

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('check/', views.check, name="check")
    
]