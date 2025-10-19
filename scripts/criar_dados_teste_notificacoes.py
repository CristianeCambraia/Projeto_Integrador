#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Produto, Fornecedor, MovimentacaoEstoque
from django.utils import timezone

def criar_dados_teste():
    print("Criando dados de teste para notificações...")
    
    # Criar fornecedor se não existir
    fornecedor, created = Fornecedor.objects.get_or_create(
        nome="Fornecedor Teste",
        defaults={
            'cnpj': '12.345.678/0001-90',
            'endereco': 'Rua Teste, 123',
            'bairro': 'Centro',
            'data_nascimento': datetime(1990, 1, 1).date(),
            'cidade': 'Cidade Teste',
            'uf': 'MG',
            'cep': '12345-678',
            'email': 'teste@fornecedor.com',
            'telefone': '(35) 99999-9999'
        }
    )
    
    hoje = timezone.now().date()
    
    # 1. Produtos próximos da validade
    produtos_validade = [
        {
            'nome': 'Medicamento A - Vence em 30 dias',
            'validade': hoje + timedelta(days=30),
            'quantidade': 50
        },
        {
            'nome': 'Medicamento B - Vence em 15 dias',
            'validade': hoje + timedelta(days=15),
            'quantidade': 25
        },
        {
            'nome': 'Medicamento C - Vence em 5 dias',
            'validade': hoje + timedelta(days=5),
            'quantidade': 10
        }
    ]
    
    for produto_data in produtos_validade:
        produto, created = Produto.objects.get_or_create(
            nome=produto_data['nome'],
            defaults={
                'preco': 50.00,
                'descricao': 'Produto de teste para notificação de validade',
                'fornecedor': fornecedor,
                'quantidade': produto_data['quantidade'],
                'validade': produto_data['validade']
            }
        )
        if created:
            print(f"Criado produto: {produto.nome}")
    
    # 2. Produtos com baixa saída (sem movimentação há 100 dias)
    produtos_baixa_saida = [
        'Produto Parado A - Sem saída há 100 dias',
        'Produto Parado B - Sem saída há 120 dias'
    ]
    
    for nome in produtos_baixa_saida:
        produto, created = Produto.objects.get_or_create(
            nome=nome,
            defaults={
                'preco': 30.00,
                'descricao': 'Produto de teste para notificação de baixa saída',
                'fornecedor': fornecedor,
                'quantidade': 100,
                'data_hora': timezone.now() - timedelta(days=100)
            }
        )
        if created:
            # Definir data antiga manualmente
            produto.data_hora = timezone.now() - timedelta(days=100)
            produto.save()
            print(f"Criado produto com baixa saída: {produto.nome}")
    
    # 3. Produtos com estoque crítico
    produtos_criticos = [
        {'nome': 'Produto Crítico A - 2 unidades', 'quantidade': 2},
        {'nome': 'Produto Crítico B - 1 unidade', 'quantidade': 1},
        {'nome': 'Produto Crítico C - 0 unidades', 'quantidade': 0}
    ]
    
    for produto_data in produtos_criticos:
        produto, created = Produto.objects.get_or_create(
            nome=produto_data['nome'],
            defaults={
                'preco': 75.00,
                'descricao': 'Produto de teste para notificação de estoque crítico',
                'fornecedor': fornecedor,
                'quantidade': produto_data['quantidade']
            }
        )
        if created:
            print(f"Criado produto com estoque crítico: {produto.nome}")
    
    print("\nDados de teste criados com sucesso!")
    print("\nPara testar as notificações:")
    print("1. Faça login no sistema")
    print("2. Clique no ícone do sininho no header")
    print("3. Você verá as notificações de:")
    print("   - Produtos próximos da validade")
    print("   - Produtos com baixa saída")
    print("   - Produtos com estoque crítico")

if __name__ == '__main__':
    criar_dados_teste()