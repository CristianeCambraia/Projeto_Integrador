from datetime import datetime, timedelta
from decimal import Decimal
from .models import Produto, Fornecedor

def criar_produtos_teste_notificacoes():
    """Cria 5 produtos de cada categoria para teste das notificações"""
    
    # Limpar produtos de teste anteriores
    Produto.objects.filter(nome__startswith="Produto Teste").delete()
    
    # Criar fornecedor de teste se não existir
    fornecedor, created = Fornecedor.objects.get_or_create(
        nome="Fornecedor Teste",
        defaults={
            'cnpj': '12345678000199',
            'telefone': '11999999999',
            'email': 'teste@teste.com'
        }
    )
    
    hoje = datetime.now().date()
    produtos_criados = []
    
    # Criar 5 produtos VENCIDOS (já passaram da validade)
    for i in range(1, 6):
        dias_atras = 5 + (i * 5)  # 10, 15, 20, 25, 30 dias atrás
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
        produtos_criados.append(f"❌ Produto Teste Vencido {i} - Venceu em {data_vencimento}")
    
    # Criar 5 produtos PRÓXIMOS DO VENCIMENTO (vencerão em 1-7 dias)
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
        produtos_criados.append(f"⚠️ Produto Teste Próximo {i} - Vence em {data_vencimento}")
    
    return produtos_criados