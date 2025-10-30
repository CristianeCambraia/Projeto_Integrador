import os
import django
import sys

# Adicionar o diretório do projeto ao path
sys.path.append('c:\\Users\\crist\\OneDrive\\Área de Trabalho\\Projeto_Integrador')

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Projeto_Integrador.settings')
django.setup()

from app.models import Produto, Fornecedor
from datetime import datetime, timedelta
from decimal import Decimal

def criar_produtos():
    print("Criando produtos de teste...")
    
    # Criar fornecedor
    fornecedor, created = Fornecedor.objects.get_or_create(
        nome="Teste Fornecedor",
        defaults={
            'cnpj': '12345678000199',
            'telefone': '11999999999',
            'email': 'teste@teste.com'
        }
    )
    
    # Criar 3 produtos com estoque crítico
    for i in range(1, 4):
        produto, created = Produto.objects.get_or_create(
            nome=f"Produto Crítico {i}",
            defaults={
                'quantidade': i,  # 1, 2, 3 unidades
                'unidade': "UN",
                'preco': Decimal('30.00'),
                'preco_compra': Decimal('20.00'),
                'validade': datetime.now().date() + timedelta(days=365),
                'fornecedor': fornecedor,
                'codigo_barras': f"CRIT{i:03d}",
                'descricao': f"Produto de teste com estoque crítico - {i} unidades"
            }
        )
        if created:
            print(f"✓ Criado: {produto.nome} com {i} unidades")
    
    print("Produtos criados com sucesso!")

if __name__ == "__main__":
    criar_produtos()