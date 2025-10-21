#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from app.models import Produto

def testar_relatorio_estoque():
    """Testa exatamente o que a view relatorio_estoque faz"""
    print("=== TESTE RELATÓRIO ESTOQUE ===")
    
    # Simular a view sem busca
    produtos = Produto.objects.all()
    print(f"Total de produtos (sem busca): {produtos.count()}")
    
    for produto in produtos:
        try:
            fornecedor_nome = produto.fornecedor.nome if produto.fornecedor else "Sem fornecedor"
            print(f"ID: {produto.id} - {produto.nome} - Fornecedor: {fornecedor_nome}")
        except Exception as e:
            print(f"ERRO no produto ID {produto.id}: {e}")
    
    # Simular a view com busca vazia
    busca = ""
    if busca:
        produtos_busca = Produto.objects.filter(nome__icontains=busca)
    else:
        produtos_busca = Produto.objects.all()
    
    print(f"\nTotal de produtos (busca vazia): {produtos_busca.count()}")

def testar_relatorio_entrada():
    """Testa exatamente o que a view relatorio_entrada faz"""
    print("\n=== TESTE RELATÓRIO ENTRADA ===")
    
    produtos = Produto.objects.all()
    print(f"Total de produtos para entrada: {produtos.count()}")
    
    for produto in produtos:
        try:
            fornecedor_nome = produto.fornecedor.nome if produto.fornecedor else "Sem fornecedor"
            print(f"ID: {produto.id} - {produto.nome} - Qtd: {produto.quantidade} - Fornecedor: {fornecedor_nome}")
        except Exception as e:
            print(f"ERRO no produto ID {produto.id}: {e}")

if __name__ == "__main__":
    testar_relatorio_estoque()
    testar_relatorio_entrada()