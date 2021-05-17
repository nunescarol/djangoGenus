from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'registro'

urlpatterns = [
    path('', views.cadastro, name='cadastro'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', views.user_login, name='login'),
    path('reset-password/', views.recuperar_senha, name='recuperar-senha'),
<<<<<<< HEAD
=======
    # path('<str:curso_slug>/', views.participar, name='participar'),
>>>>>>> branch_lari
    path('check/', views.check, name="check"),
    # path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_reset/password_change_done.html'), 
    #     name='password_change_done'),

    # path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_reset/password_change.html'), 
    #     name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url = reverse_lazy('registro:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url = reverse_lazy('registro:password_reset_done')), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),
]