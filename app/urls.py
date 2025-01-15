from django.contrib import admin
from django.urls import path
from registro_horas.views import IndexView, CriarTarefaView, EncerrarTarefaView, VisualizarTarefaView, ExportXLSView, PararTarefaView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('registrar/', CriarTarefaView.as_view(), name='registrar'),
    path('encerrar/<uuid:pk>/', EncerrarTarefaView.as_view(), name='encerrar'),
    path('visualizar/<uuid:pk>/', VisualizarTarefaView.as_view(), name='visualizar'),
    path('export_xls/', ExportXLSView.as_view(), name='export_xls'),
    path('pausar/<uuid:pk>/', PararTarefaView.as_view(), name='pausar'),
]
