from django.contrib import admin
from django.urls import include,path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',include('registro.urls'), name='registro'),
    path('genus/',include('cursos.urls'), name='inicio'),
    path('',views.homepage, name='home'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)