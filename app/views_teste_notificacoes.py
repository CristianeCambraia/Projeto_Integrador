from django.http import JsonResponse
from datetime import datetime, timedelta
from decimal import Decimal
from .models import Produto, Fornecedor

def criar_produtos_teste_notificacoes(request):
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
    
    # Criar 5 produtos com ESTOQUE CRÍTICO (≤ 5 unidades)
    for i in range(1, 6):
        produto = Produto.objects.create(
            nome=f"Produto Teste Crítico {i}",
            quantidade=i,  # 1, 2, 3, 4, 5 unidades
            unidade="UN",
            preco=Decimal('30.00'),
            preco_compra=Decimal('20.00'),
            validade=hoje + timedelta(days=365),  # Válido por 1 ano
            fornecedor=fornecedor,
            codigo_barras=f"CRIT{i:03d}"
        )
        produtos_criados.append(f"🔴 Produto Teste Crítico {i} - {i} unidades")
    
    # Criar 5 produtos com BAIXA SAÍDA (sem movimentação há 90+ dias)
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
            data_hora=data_antiga  # Data antiga para simular produto parado
        )
        produtos_criados.append(f"📦 Produto Teste Parado {i} - Parado há {dias_atras} dias")
    
    return JsonResponse({
        'status': 'success',
        'message': f'Criados {len(produtos_criados)} produtos de teste (5 de cada categoria)',
        'produtos': produtos_criados
    })