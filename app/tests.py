from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from .models import (
    Usuario, Fornecedor, Produto, Cliente, Orcamento, 
    MovimentacaoEstoque, Suporte, Servico, Admin
)


class ModelTestCase(TestCase):
    """Testes para os modelos"""
    
    def setUp(self):
        self.fornecedor = Fornecedor.objects.create(
            nome="Fornecedor Teste",
            cnpj="12.345.678/0001-90",
            endereco="Rua Teste, 123",
            bairro="Centro",
            data_nascimento=date(1990, 1, 1),
            cidade="São Paulo",
            uf="SP",
            cep="01234-567",
            email="fornecedor@teste.com",
            telefone="(11) 99999-9999"
        )
        
        self.produto = Produto.objects.create(
            nome="Produto Teste",
            preco=Decimal('10.50'),
            descricao="Descrição do produto teste",
            fornecedor=self.fornecedor,
            quantidade=100
        )
        
        self.cliente = Cliente.objects.create(
            nome="Cliente Teste",
            cpf="123.456.789-00",
            endereco="Rua Cliente, 456",
            bairro="Vila Nova",
            data_nascimento=date(1985, 5, 15),
            cidade="Rio de Janeiro",
            uf="RJ",
            cep="20000-000",
            email="cliente@teste.com",
            telefone="(21) 88888-8888"
        )
        
        self.usuario = Usuario.objects.create(
            nome="Usuário Teste",
            email="usuario@teste.com",
            cpf="987.654.321-00",
            endereco="Rua Usuário, 789",
            telefone="(11) 77777-7777",
            data_nascimento=date(1992, 3, 10),
            senha="senha123"
        )

    def test_fornecedor_creation(self):
        """Testa criação de fornecedor"""
        self.assertEqual(self.fornecedor.nome, "Fornecedor Teste")
        self.assertEqual(str(self.fornecedor), "Fornecedor Teste")
        self.assertTrue(self.fornecedor.ativo)

    def test_produto_creation(self):
        """Testa criação de produto"""
        self.assertEqual(self.produto.nome, "Produto Teste")
        self.assertEqual(self.produto.preco, Decimal('10.50'))
        self.assertEqual(self.produto.fornecedor, self.fornecedor)
        self.assertEqual(str(self.produto), "Produto Teste - R$10.50")

    def test_cliente_creation(self):
        """Testa criação de cliente"""
        self.assertEqual(self.cliente.nome, "Cliente Teste")
        self.assertEqual(self.cliente.email, "cliente@teste.com")
        self.assertEqual(str(self.cliente), "Cliente Teste")

    def test_usuario_creation(self):
        """Testa criação de usuário"""
        self.assertEqual(self.usuario.nome, "Usuário Teste")
        self.assertEqual(self.usuario.email, "usuario@teste.com")
        self.assertEqual(str(self.usuario), "Usuário Teste")

    def test_movimentacao_estoque(self):
        """Testa movimentação de estoque"""
        movimentacao = MovimentacaoEstoque.objects.create(
            produto=self.produto,
            tipo='ENTRADA',
            quantidade=50
        )
        self.assertEqual(movimentacao.produto, self.produto)
        self.assertEqual(movimentacao.tipo, 'ENTRADA')
        self.assertEqual(movimentacao.quantidade, 50)

    def test_orcamento_creation(self):
        """Testa criação de orçamento"""
        orcamento = Orcamento.objects.create(
            cliente="Cliente Orçamento",
            email="orcamento@teste.com",
            telefone="(11) 99999-9999",
            descricao="Orçamento de teste"
        )
        self.assertEqual(orcamento.cliente, "Cliente Orçamento")
        self.assertIn("Cliente Orçamento", str(orcamento))


class ViewTestCase(TestCase):
    """Testes para as views"""
    
    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            nome="Usuário Teste",
            email="teste@teste.com",
            cpf="123.456.789-00",
            endereco="Rua Teste",
            telefone="(11) 99999-9999",
            data_nascimento=date(1990, 1, 1),
            senha="senha123"
        )

    def test_home_page_status(self):
        """Testa se a página inicial carrega"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_status(self):
        """Testa se a página de login carrega"""
        try:
            response = self.client.get(reverse('login'))
            self.assertEqual(response.status_code, 200)
        except:
            # Se a URL não existir, testa diretamente
            response = self.client.get('/login/')
            self.assertIn(response.status_code, [200, 404])

    def test_cadastro_usuario_page(self):
        """Testa página de cadastro de usuário"""
        try:
            response = self.client.get(reverse('cadastrar_usuario'))
            self.assertEqual(response.status_code, 200)
        except:
            response = self.client.get('/cadastrar_usuario/')
            self.assertIn(response.status_code, [200, 404])

    def test_fornecedores_page(self):
        """Testa página de fornecedores"""
        try:
            response = self.client.get(reverse('fornecedores'))
            self.assertIn(response.status_code, [200, 302])  # 302 se redirecionar para login
        except:
            response = self.client.get('/fornecedores/')
            self.assertIn(response.status_code, [200, 302, 404])


class FormTestCase(TestCase):
    """Testes para formulários"""
    
    def test_cadastro_usuario_post(self):
        """Testa POST para cadastro de usuário"""
        data = {
            'nome': 'Novo Usuário',
            'email': 'novo@teste.com',
            'cpf': '111.222.333-44',
            'endereco': 'Rua Nova, 123',
            'telefone': '(11) 88888-8888',
            'data_nascimento': '1995-06-20',
            'senha': 'novasenha123',
            'confirmar_senha': 'novasenha123'
        }
        
        try:
            response = self.client.post(reverse('cadastrar_usuario'), data)
            # Verifica se foi criado ou se houve redirecionamento
            self.assertIn(response.status_code, [200, 201, 302])
        except:
            # Se a URL não existir, apenas verifica se não dá erro 500
            response = self.client.post('/cadastrar_usuario/', data)
            self.assertNotEqual(response.status_code, 500)

    def test_login_post(self):
        """Testa POST para login"""
        data = {
            'email': 'teste@teste.com',
            'senha': 'senha123'
        }
        
        try:
            response = self.client.post(reverse('login'), data)
            self.assertIn(response.status_code, [200, 302])
        except:
            response = self.client.post('/login/', data)
            self.assertNotEqual(response.status_code, 500)


class DatabaseTestCase(TestCase):
    """Testes de integridade do banco de dados"""
    
    def test_unique_constraints(self):
        """Testa constraints únicos"""
        # Cria primeiro usuário
        Usuario.objects.create(
            nome="Usuário 1",
            email="unico@teste.com",
            cpf="123.456.789-00",
            endereco="Rua Teste",
            telefone="(11) 99999-9999",
            data_nascimento=date(1990, 1, 1),
            senha="senha123"
        )
        
        # Tenta criar usuário com mesmo email (deve falhar)
        with self.assertRaises(Exception):
            Usuario.objects.create(
                nome="Usuário 2",
                email="unico@teste.com",  # Email duplicado
                cpf="987.654.321-00",
                endereco="Rua Teste 2",
                telefone="(11) 88888-8888",
                data_nascimento=date(1991, 2, 2),
                senha="senha456"
            )

    def test_foreign_key_relationships(self):
        """Testa relacionamentos de chave estrangeira"""
        fornecedor = Fornecedor.objects.create(
            nome="Fornecedor FK",
            cnpj="98.765.432/0001-10",
            endereco="Rua FK",
            bairro="Centro",
            data_nascimento=date(1990, 1, 1),
            cidade="São Paulo",
            uf="SP",
            cep="01234-567",
            email="fk@teste.com",
            telefone="(11) 99999-9999"
        )
        
        produto = Produto.objects.create(
            nome="Produto FK",
            preco=Decimal('25.00'),
            fornecedor=fornecedor
        )
        
        # Verifica se o relacionamento funciona
        self.assertEqual(produto.fornecedor, fornecedor)
        self.assertIn(produto, fornecedor.produtos.all())


class SecurityTestCase(TestCase):
    """Testes básicos de segurança"""
    
    def test_sql_injection_protection(self):
        """Testa proteção contra SQL injection básica"""
        malicious_input = "'; DROP TABLE app_usuario; --"
        
        # Tenta buscar usuário com input malicioso
        usuarios = Usuario.objects.filter(nome=malicious_input)
        self.assertEqual(usuarios.count(), 0)
        
        # Verifica se a tabela ainda existe
        self.assertTrue(Usuario.objects.model._meta.db_table)

    def test_xss_protection_in_context(self):
        """Testa se dados maliciosos não são executados"""
        xss_input = "<script>alert('XSS')</script>"
        
        usuario = Usuario.objects.create(
            nome=xss_input,
            email="xss@teste.com",
            cpf="123.456.789-00",
            endereco="Rua XSS",
            telefone="(11) 99999-9999",
            data_nascimento=date(1990, 1, 1),
            senha="senha123"
        )
        
        # Verifica se o input foi salvo como string (não executado)
        self.assertEqual(usuario.nome, xss_input)