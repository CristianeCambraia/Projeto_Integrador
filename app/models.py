from django.db import models
from django.utils import timezone



class Suporte(models.Model):
    nome = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(max_length=200)
    descreva = models.CharField(max_length=1000)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"#{self.id} - {self.nome}"




class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20)  # Usar CharField pois pode conter caracteres especiais
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200, blank=True, null=True)  # Pode ser opcional
    data_nascimento = models.DateField()
    cidade = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)  # Também CharField por conta do formato
    email = models.EmailField(max_length=200)  # Melhor usar EmailField para validação
    telefone = models.CharField(max_length=20)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    UNIDADE_CHOICES = [
        ('Unidades', 'Unidades'),
        ('Caixa', 'Caixa'),
    ]
    
    nome = models.CharField(max_length=100)
    codigo_barras = models.CharField(max_length=50, blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name="produtos", null=True, blank=True)
    data_hora = models.DateTimeField(default=timezone.now)
    unidade = models.CharField(max_length=50, choices=UNIDADE_CHOICES, default="Unidades")
    quantidade = models.IntegerField(default=1)
    validade = models.DateField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.nome} - R${self.preco}"

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=20)  # Usar CharField pois pode conter caracteres especiais
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200, blank=True, null=True)  # Pode ser opcional
    data_nascimento = models.DateField()
    cidade = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)  # Também CharField por conta do formato
    email = models.EmailField(max_length=200)  # Melhor usar EmailField para validação
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome
    
class Orcamento(models.Model):
    cliente = models.CharField(max_length=100)
    cnpj = models.CharField(max_length=20, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    itens_unidades = models.TextField(blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    itens_quantidades = models.TextField(blank=True, null=True)
    itens_valores = models.TextField(blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    data = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Orçamento para {self.cliente} em {self.data}'

class Usuario(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    cpf = models.CharField(max_length=20, unique=True)
    endereco = models.CharField(max_length=200)
    telefone = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    senha = models.CharField(max_length=128)

    def __str__(self):
        return self.nome

class MovimentacaoEstoque(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SAIDA', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data_hora = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'{self.tipo} - {self.produto.nome} - {self.quantidade}'
    
    class Meta:
        ordering = ['-data_hora']

class RecuperacaoSenha(models.Model):
    email = models.EmailField()
    codigo = models.CharField(max_length=6)
    criado_em = models.DateTimeField(default=timezone.now)
    usado = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.email} - {self.codigo}'
    
    class Meta:
        ordering = ['-criado_em']

class Admin(models.Model):
    email = models.EmailField(max_length=200, unique=True)
    senha = models.CharField(max_length=128)
    
    def __str__(self):
        return self.email


