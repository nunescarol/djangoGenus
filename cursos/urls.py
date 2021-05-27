from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('inicio/',views.inicio, name='inicio'),
    path('criar/',views.criar, name='criar-curso'),
    path('cursos/',views.buscar_cursos, name='buscar-cursos'),
    path('buscar/',views.buscar_cursos, name='buscar'),
    path('<str:curso_slug>/resumo/',views.resumo, name='resumo'),
    path('<str:curso_slug>/',views.curso, name='curso'),
    path('<str:curso_slug>/criar-modulo/',views.criar_modulo, name='criar-modulo'),
    path('<str:curso_slug>/modulos/',views.modulos, name='modulos'), 
    path('<str:curso_slug>/alunos/',views.exibir_alunos, name='exibir-alunos'), 
    path('<str:curso_slug>/<int:modulo_id>/',views.exibir_modulo, name='exibir-modulo'),
    path('<str:curso_slug>/<int:modulo_id>/criar-post/',views.criar_post, name='criar-post'),
    path('<str:curso_slug>/<int:modulo_id>/criar-atividade/',views.criar_atividade, name='criar-atividade'),    
    path('<str:curso_slug>/<int:modulo_id>/<int:post_id>/',views.exibir_post, name='exibir-post'),
    path('<str:curso_slug>/<int:modulo_id>/<int:post_id>/adicionar-arquivo/',views.adicionar_arquivo, name='adicionar-arquivo'),
    
    path('<str:curso_slug>/<int:modulo_id>/<int:post_id>/adicionar-comentario/',views.adicionar_comentario, name='adicionar-comentario'), 
    path('<str:curso_slug>/<int:modulo_id>/<int:post_id>/respostas/',views.exibir_respostas, name='exibir-respostas'),
    path('<str:curso_slug>/<int:modulo_id>/<int:post_id>/respostas/<str:aluno>',views.exibir_resposta_de_aluno, name='exibir-resp-aluno'),

    
    
    path('inicio/aaa/', views.teste_formnota, name='teste'),
    # path('<str:curso_slug>/<int:modulo_id>/criar-post/',views.criar_post, name='criar-post'),  
]