from django.urls import path
from . import views
from .views_minha_conta import minha_conta, editar_conta
from django.contrib.auth.views import LogoutView

 
urlpatterns = [
    # Página inicial
    path('', views.pagina_home, name='home'),


    
    # ----- FORNECEDORES -----
    path('fornecedores/', views.abrir_fornecedor, name='fornecedores'),
    path('fornecedores/salvar/', views.salvar_fornecedor, name='salvar_fornecedor'),
    path('fornecedores/lista/', views.lista_fornecedores, name='lista_fornecedores'),
    path('fornecedores/editar/<int:fornecedor_id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/alternar-status/<int:fornecedor_id>/', views.alternar_status_fornecedor, name='alternar_status_fornecedor'),

    # ----- PRODUTOS -----
    path('produtos/', views.cadastrar, name='produtos'),  # abrir form + salvar produto
    path('produtos/lista/', views.lista_produtos, name='lista_produtos'),
    path('produtos/cadastrar/', views.cadastrar, name='cadastrar_produto'),
    path('produtos/editar/<int:produto_id>/', views.editar_produto, name='editar_produto'),

    # ----- SERVIÇOS -----
    path('servicos/cadastrar/', views.cadastrar_servico, name='cadastrar_servico'),
    path('servicos/lista/', views.lista_servicos, name='lista_servicos'),
    path('servicos/editar/<int:servico_id>/', views.editar_servico, name='editar_servico'),
    path('servicos/excluir/<int:servico_id>/', views.excluir_servico, name='excluir_servico'),

    # ----- CLIENTES -----
    path('clientes/', views.abrir_cliente, name='clientes'),
    path('clientes/salvar/', views.salvar_cliente, name='salvar_cliente'),
    path('clientes/lista/', views.lista_cliente, name='lista_cliente'),
    path('clientes/editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),

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
    path('suporte/lista/', views.lista_suporte, name='lista_suporte'),

    # ----- RELATÓRIOS -----
    path('relatorio-estoque/', views.relatorio_estoque, name='relatorio_estoque'),
    path('relatorio-entrada/', views.relatorio_entrada, name='relatorio_entrada'),
    path('relatorio-saida/', views.relatorio_saida, name='relatorio_saida'),
    path('relatorio-movimentacao-entrada/', views.relatorio_movimentacao_entrada, name='relatorio_movimentacao_entrada'),
    path('relatorio-movimentacao-saida/', views.relatorio_movimentacao_saida, name='relatorio_movimentacao_saida'),
    
    # ----- LOGIN/LOGOUT -----
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # ----- ADMIN -----
    path('admin/', views.admin_login, name='admin'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin-login/', views.admin_login, name='admin_login_alt'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    
    # ----- BUSCAR PRODUTO -----
    path('buscar-produto-por-codigo/', views.buscar_produto_por_codigo, name='buscar_produto_por_codigo'),
    
    # ----- BUSCAR CLIENTES -----
    path('buscar-clientes/', views.buscar_clientes, name='buscar_clientes'),
    
    # ----- EXPORTAR PDF -----
    path('orcamento/<int:orcamento_id>/pdf/', views.exportar_pdf_orcamento, name='exportar_pdf_orcamento'),
    
    # ----- ENVIAR EMAIL -----
    path('enviar_orcamento_email/', views.enviar_orcamento_email, name='enviar_orcamento_email'),
    
    # ----- RECUPERAÇÃO DE SENHA -----
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
    path('verificar-codigo/', views.verificar_codigo, name='verificar_codigo'),
    path('nova-senha/', views.nova_senha, name='nova_senha'),
    
    # ----- NOTIFICAÇÕES -----
    path('notificacoes/', views.obter_notificacoes, name='obter_notificacoes'),
    path('notificacoes/marcar-lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('notificacoes/marcar-todas-lidas/', views.marcar_todas_lidas, name='marcar_todas_lidas'),
    path('notificacoes/teste/', views.teste_notificacoes, name='teste_notificacoes'),
    path('notificacao/<int:produto_id>/<str:tipo>/', views.detalhes_notificacao, name='detalhes_notificacao'),
    
    # ----- DEBUG -----
    path('debug/produtos/', views.debug_produtos, name='debug_produtos'),
    
    # ----- ESTOQUE PDF/EMAIL -----
    path('estoque/pdf/', views.exportar_estoque_pdf, name='exportar_estoque_pdf'),
    path('enviar-estoque-email/', views.enviar_estoque_email, name='enviar_estoque_email'),
    

    
    # ----- MINHA CONTA -----
    path('minha-conta/', minha_conta, name='minha_conta'),
    path('editar-conta/', editar_conta, name='editar_conta'),
    
    # ----- ADMIN - USUÁRIOS CADASTRADOS -----
    path('usuarios-cadastrados/', views.usuarios_cadastrados, name='usuarios_cadastrados'),
    
    # ----- GERAR SENHA TEMPORÁRIA -----
    path('gerar-senha-temporaria/', views.gerar_senha_temporaria, name='gerar_senha_temporaria'),
    
    # ----- DELETAR USUÁRIO -----
    path('deletar-usuario/', views.deletar_usuario, name='deletar_usuario'),
    
    # ----- ALTERNAR STATUS USUÁRIO -----
    path('alternar-status-usuario/', views.alternar_status_usuario, name='alternar_status_usuario'),
    
    # ----- RELATÓRIO FINANCEIRO -----
    path('relatorio-financeiro/', views.relatorio_financeiro, name='relatorio_financeiro'),
    path('financeiro/pdf/', views.exportar_financeiro_pdf, name='exportar_financeiro_pdf'),
    path('enviar-financeiro-email/', views.enviar_financeiro_email, name='enviar_financeiro_email'),
    
    # ----- CADASTROS MENU -----
    path('cadastros/', views.cadastros, name='cadastros'),
    
    # ----- TESTE PRODUTOS VENCIDOS -----
    path('debug-produtos-vencidos/', views.debug_produtos_vencidos, name='debug_produtos_vencidos'),
    path('criar-produtos-teste-notificacoes/', views.criar_produtos_teste_notificacoes, name='criar_produtos_teste_notificacoes'),

]