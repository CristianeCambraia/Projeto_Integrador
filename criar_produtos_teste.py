import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto_integrador.settings')
django.setup()

from app.models import Produto, Fornecedor

def criar_produtos_teste():
    print("Criando produtos de teste para notificações...")
    
    # Limpar produtos de teste anteriores
    Produto.objects.filter(nome__startswith="Produto Teste").delete()
    print("Produtos de teste anteriores removidos.")
    
    # Criar fornecedor de teste se não existir
    fornecedor, created = Fornecedor.objects.get_or_create(
        nome="Fornecedor Teste",
        defaults={
            'cnpj': '12345678000199',
            'telefone': '11999999999',
            'email': 'teste@teste.com'
        }
    )
    
    if created:
        print("Fornecedor de teste criado.")
    
    hoje = datetime.now().date()
    produtos_criados = []
    
    # Criar 5 produtos com ESTOQUE CRÍTICO (≤ 5 unidades)
    print("\nCriando produtos com estoque crítico...")
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
        produtos_criados.append(f"🔴 {produto.nome} - {i} unidades")
        print(f"  ✓ {produto.nome} criado com {i} unidades")
    
    # Criar 5 produtos VENCIDOS
    print("\nCriando produtos vencidos...")
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
        produtos_criados.append(f"❌ {produto.nome} - Venceu há {dias_atras} dias")
        print(f"  ✓ {produto.nome} criado (venceu em {data_vencimento})")
    
    # Criar 5 produtos PRÓXIMOS DO VENCIMENTO
    print("\nCriando produtos próximos do vencimento...")
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
        produtos_criados.append(f"⚠️ {produto.nome} - Vence em {dias_futuro} dias")
        print(f"  ✓ {produto.nome} criado (vence em {data_vencimento})")
    
    # Criar 5 produtos com BAIXA SAÍDA
    print("\nCriando produtos com baixa saída...")
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
        produtos_criados.append(f"📦 {produto.nome} - Parado há {dias_atras} dias")
        print(f"  ✓ {produto.nome} criado (parado há {dias_atras} dias)")
    
    print(f"\n✅ CONCLUÍDO! Criados {len(produtos_criados)} produtos de teste:")
    print("   - 5 produtos com estoque crítico (1-5 unidades)")
    print("   - 5 produtos vencidos")
    print("   - 5 produtos próximos do vencimento")
    print("   - 5 produtos com baixa saída")
    print("\nAgora você pode testar as notificações no sistema!")

if __name__ == "__main__":
    criar_produtos_teste()