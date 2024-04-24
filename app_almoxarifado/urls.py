from django.urls import path
from .import views

app_name = 'app_almoxarifado'

urlpatterns = [
  path('menu', views.menu, name="menu"),
  path('cadastrar_local/', views.cadastrar_local, name='cadastrar_local'),
  path('cadastrar_material/<int:construcao_id>/', views.cadastrar_material, name='cadastrar_material'),
  path('escolher_local/', views.escolher_local, name='escolher_local'),
  path('visualizar_estoque/<int:construcao_id>/', views.visualizar_estoque, name='visualizar_estoque'),
  path('deletar_local/<int:local_id>/', views.deletar_local, name='deletar_local'),
  path('visualizar_estoque/<int:material_id>/deletar/', views.deletar_material, name='deletar_material'),
  path('upload_lista_materiais/<int:construcao_id>/', views.upload_lista_materiais, name='upload_lista_materiais'),
  path('teste/', views.teste, name="teste"),
  path('detalhe_material/<int:material_id>/', views.detalhe_material, name='detalhe_material'),
  path('atualizar_quantidade/<int:material_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),
  path('movimentacoes_estoque/', views.movimentacoes_estoque, name='movimentacoes_estoque'),
  path('exportar-lista-materiais/<int:construcao_id>/', views.exportar_lista_materiais, name='exportar_lista_materiais'),

]