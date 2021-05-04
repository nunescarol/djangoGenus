from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('inicio/',views.inicio, name='inicio'),
    path('criar/',views.criar, name='criar-curso'),
    path('cursos/',views.buscar_cursos, name='buscar-cursos'),
    path('<str:curso_slug>/resumo/',views.resumo, name='resumo'),
    path('<str:curso_slug>/',views.curso, name='curso'),
    path('<str:curso_slug>/criar-modulo/',views.criar_modulo, name='criar-modulo'),
    path('<str:curso_slug>/modulos/',views.modulos, name='modulos'), 
    path('<str:curso_slug>/<int:modulo_id>/',views.exibir_modulo, name='exibir-modulo'),
    path('<str:curso_slug>/<int:modulo_id>/criar-atividade/',views.criar_atividade, name='criar-atividade'),
    path('<str:curso_slug>/<int:modulo_id>/criar-post/',views.criar_post, name='criar-post'),  
]