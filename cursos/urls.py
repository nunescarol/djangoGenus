from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('',views.perfil, name='perfil'),
    path('criar/',views.criar, name='criar-curso'),
    path('cursos/',views.buscar_cursos, name='buscar-cursos'),
]