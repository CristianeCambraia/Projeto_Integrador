from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.cadastros, name='cadastros'),  

    # ----- FORNECEDORES -----
    path('fornecedores/', views.abrir_fornecedor, name='fornecedores'),
    path('fornecedores/salvar/', views.salvar_fornecedor, name='salvar_fornecedor'),
    path('fornecedores/lista/', views.lista_fornecedores, name='lista_fornecedores'),

    # ----- PRODUTOS -----
    path('produtos/', views.abrir_produto, name='produtos'),
    path('produtos/salvar/', views.salvar_produto, name='salvar_produto'),
    path('produtos/lista/', views.lista_produtos, name='lista_produtos'),
]
