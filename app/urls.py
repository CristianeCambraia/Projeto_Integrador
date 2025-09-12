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
    path('produtos/', views.cadastrar, name='produtos'),  # abrir form + salvar produto
    path('produtos/lista/', views.lista_produtos, name='lista_produtos'),

    # ----- CADASTRAR PRODUTO (opcional, pode remover se não usar) -----
    path('produtos/cadastrar/', views.cadastrar, name='cadastrar_produto'),
]
