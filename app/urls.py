from django.urls import path
from . import views

urlpatterns = [
    # Página inicial
    path('', views.pagina_home, name='home'),

    # ----- FORNECEDORES -----
    path('fornecedores/', views.abrir_fornecedor, name='fornecedores'),
    path('fornecedores/salvar/', views.salvar_fornecedor, name='salvar_fornecedor'),
    path('fornecedores/lista/', views.lista_fornecedores, name='lista_fornecedores'),

    # ----- PRODUTOS -----
    path('produtos/', views.cadastrar, name='produtos'),  # abrir form + salvar produto
    path('produtos/lista/', views.lista_produtos, name='lista_produtos'),
    path('produtos/cadastrar/', views.cadastrar, name='cadastrar_produto'),

    # ----- CLIENTES -----
    path('clientes/', views.abrir_cliente, name='clientes'),
    path('clientes/salvar/', views.salvar_cliente, name='salvar_cliente'),
    path('clientes/lista/', views.lista_cliente, name='lista_cliente'),

    # ----- USUÁRIOS -----
    path('usuarios/cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),

    # ---- ORÇAMENTOS -----
    path('emitir_orcamento/', views.emitir_orcamento, name='emitir_orcamento'),
    path('salvar_orcamento/', views.salvar_orcamento, name='salvar_orcamento'),
    path('orcamentos_emitidos/', views.orcamentos_emitidos, name='orcamentos_emitidos'),
    path('novo_orcamento/', views.novo_orcamento, name='novo_orcamento'),
    path('voltar/', views.voltar, name='voltar'),

    # Sobre nós
    path('sobre_nos/', views.sobre_nos, name='sobre_nos'),
]
