from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    # Página inicial, lista de carros (com barra de pesquisa)
    path('', views.listar_carros, name='listar_carros'),  
    
    # URL para visualizar os detalhes de um carro específico
    path('detalhes/<int:carro_id>/', views.detalhes_carro, name='detalhes_carro'),  
    
    # URL para marcar um carro como comprado
    path('comprar/<int:carro_id>/', views.comprar_carro, name='comprar_carro'), 
    
    # URL para a página inicial (home)
    path('home/', views.home, name='home'),
    
    # URL para adicionar um carro novo
    path('adicionar/', views.adicionar_carro, name='adicionar_carro'),
    
    # URL para enviar formulário de contato
    path('enviar-contato/', views.enviar_contato, name='enviar_contato'),
    
    # URL para remover carros
    path('remover/', views.remover_carro, name='remover_carro'),
    
    # URL para editar um carro específico
    path('editar/<int:carro_id>/', views.editar_carro, name='editar_carro'),  

    # URL para visualizar o histórico de compras
    path('historico/', views.historico_compras, name='historico_compras'),  # Nova URL para o histórico de compras
]

# Adicionar suporte para arquivos de mídia em ambiente de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
