from django.contrib import admin
from django.urls import path
from registro_horas.views import index_view, criar_tarefa_view, encerrar_tarefa_view, visualizar_tarefa_view, export_xls
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name='index'),
    path('registrar/', criar_tarefa_view, name='registrar'),
    path('encerrar/<uuid:pk>/', encerrar_tarefa_view, name='encerrar'),
    path('visualizar/<uuid:pk>/', visualizar_tarefa_view, name='visualizar'),
     path('export_xls/', export_xls, name='export_xls'),
]