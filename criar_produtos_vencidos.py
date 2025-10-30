import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Produto, Fornecedor
from datetime import datetime, timedelta
from decimal import Decimal

# Limpar produtos de teste anteriores
Produto.objects.filter(nome__startswith="Produto Teste").delete()

hoje = datetime.now().date()

# Criar fornecedor de teste
fornecedor, created = Fornecedor.objects.get_or_create(
    nome="Fornecedor Teste",
    defaults={
        'cnpj': '12345678000199',
        'telefone': '11999999999',
        'email': 'teste@teste.com',
        'data_nascimento': hoje,
        'endereco': 'Rua Teste, 123',
        'cidade': 'Cidade Teste'
    }
)
produtos_criados = []

# 5 produtos VENCIDOS
for i in range(1, 6):
    dias_atras = 10 + (i * 5)  # 15, 20, 25, 30, 35 dias atrás
    data_vencimento = hoje - timedelta(days=dias_atras)
    
    produto = Produto.objects.create(
        nome=f"Produto Teste Vencido {i}",
        quantidade=10 + i,
        unidade="UN",
        preco=Decimal('15.50'),
        preco_compra=Decimal('10.00'),
        validade=data_vencimento,
        fornecedor=fornecedor,
        codigo_barras=f"VENC{i:03d}"
    )
    produtos_criados.append(f"❌ {produto.nome} - Venceu em {data_vencimento}")

# 5 produtos PRÓXIMOS DO VENCIMENTO
for i in range(1, 6):
    dias_futuro = i  # 1, 2, 3, 4, 5 dias no futuro
    data_vencimento = hoje + timedelta(days=dias_futuro)
    
    produto = Produto.objects.create(
        nome=f"Produto Teste Próximo {i}",
        quantidade=20 + i,
        unidade="UN",
        preco=Decimal('25.50'),
        preco_compra=Decimal('15.00'),
        validade=data_vencimento,
        fornecedor=fornecedor,
        codigo_barras=f"PROX{i:03d}"
    )
    produtos_criados.append(f"⚠️ {produto.nome} - Vence em {data_vencimento}")

# 5 produtos com ESTOQUE CRÍTICO
for i in range(1, 6):
    produto = Produto.objects.create(
        nome=f"Produto Teste Crítico {i}",
        quantidade=i,  # 1, 2, 3, 4, 5 unidades
        unidade="UN",
        preco=Decimal('30.00'),
        preco_compra=Decimal('20.00'),
        validade=hoje + timedelta(days=365),
        fornecedor=fornecedor,
        codigo_barras=f"CRIT{i:03d}"
    )
    produtos_criados.append(f"🔴 {produto.nome} - {i} unidades")

# 5 produtos com BAIXA SAÍDA
for i in range(1, 6):
    dias_atras = 90 + (i * 10)  # 100, 110, 120, 130, 140 dias atrás
    data_antiga = datetime.now() - timedelta(days=dias_atras)
    
    produto = Produto.objects.create(
        nome=f"Produto Teste Parado {i}",
        quantidade=30 + i,
        unidade="UN",
        preco=Decimal('40.00'),
        preco_compra=Decimal('25.00'),
        validade=hoje + timedelta(days=365),
        fornecedor=fornecedor,
        codigo_barras=f"PARA{i:03d}",
        data_hora=data_antiga
    )
    produtos_criados.append(f"📦 {produto.nome} - Parado há {dias_atras} dias")

print(f"Criados {len(produtos_criados)} produtos de teste:")
for produto in produtos_criados:
    print(produto)

print("\nVerificando produtos vencidos no banco:")
vencidos = Produto.objects.filter(validade__lt=hoje)
print(f"Total de produtos vencidos: {vencidos.count()}")
for v in vencidos:
    print(f"- {v.nome}: validade {v.validade}")