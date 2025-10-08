from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

 
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
    path('produtos/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),

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
    path('orcamento/<int:orcamento_id>/editar_descricao/', views.editar_descricao, name='editar_descricao'),
    path('orcamento/<int:orcamento_id>/', views.abrir_orcamento, name='abrir_orcamento'),
    path('novo_orcamento/', views.novo_orcamento, name='novo_orcamento'),
    path('voltar/', views.voltar, name='voltar'),

    # ----- SOBRE E SUPORTE -----
    path('sobre_nos/', views.sobre_nos, name='sobre_nos'),
    path('suporte/novo/', views.criar_suporte, name='criar_suporte'),

    # ----- RELATÓRIOS -----
    path('relatorio-estoque/', views.relatorio_estoque, name='relatorio_estoque'),
    path('relatorio-entrada/', views.relatorio_entrada, name='relatorio_entrada'),
    path('relatorio-saida/', views.relatorio_saida, name='relatorio_saida'),
    
    # ----- LOGIN/LOGOUT -----
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')

]