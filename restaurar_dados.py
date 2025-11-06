#!/usr/bin/env python
import os
import sys
import django
import json
from datetime import datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Usuario, Cliente, Fornecedor, Produto, Orcamento, Admin

def restaurar_dados():
    """Restaurar dados do backup"""
    try:
        with open('backup_dados.json', 'r', encoding='utf-8') as f:
            backup_data = json.load(f)
        
        print("INICIANDO RESTAURACAO DOS DADOS...")
        
        # Restaurar Usuários
        for user_data in backup_data['usuarios']:
            if not Usuario.objects.filter(email=user_data['email']).exists():
                Usuario.objects.create(
                    nome=user_data['nome'],
                    email=user_data['email'],
                    cpf=user_data['cpf'],
                    endereco=user_data['endereco'],
                    cidade=user_data['cidade'],
                    uf=user_data['uf'],
                    telefone=user_data['telefone'],
                    data_nascimento=datetime.fromisoformat(user_data['data_nascimento']).date(),
                    senha=user_data['senha'],
                    ativo=user_data['ativo']
                )
        
        # Restaurar Clientes
        for cliente_data in backup_data['clientes']:
            if not Cliente.objects.filter(email=cliente_data['email']).exists():
                Cliente.objects.create(
                    nome=cliente_data['nome'],
                    cpf=cliente_data['cpf'],
                    endereco=cliente_data['endereco'],
                    bairro=cliente_data['bairro'],
                    complemento=cliente_data['complemento'],
                    data_nascimento=datetime.fromisoformat(cliente_data['data_nascimento']).date(),
                    cidade=cliente_data['cidade'],
                    uf=cliente_data['uf'],
                    cep=cliente_data['cep'],
                    email=cliente_data['email'],
                    telefone=cliente_data['telefone']
                )
        
        # Restaurar Fornecedores
        for fornecedor_data in backup_data['fornecedores']:
            if not Fornecedor.objects.filter(email=fornecedor_data['email']).exists():
                Fornecedor.objects.create(
                    nome=fornecedor_data['nome'],
                    cnpj=fornecedor_data['cnpj'],
                    endereco=fornecedor_data['endereco'],
                    bairro=fornecedor_data['bairro'],
                    complemento=fornecedor_data['complemento'],
                    data_nascimento=datetime.fromisoformat(fornecedor_data['data_nascimento']).date(),
                    cidade=fornecedor_data['cidade'],
                    uf=fornecedor_data['uf'],
                    cep=fornecedor_data['cep'],
                    email=fornecedor_data['email'],
                    telefone=fornecedor_data['telefone'],
                    ativo=fornecedor_data['ativo']
                )
        
        # Restaurar Produtos
        for produto_data in backup_data['produtos']:
            if not Produto.objects.filter(nome=produto_data['nome']).exists():
                fornecedor = None
                if produto_data['fornecedor_nome']:
                    try:
                        fornecedor = Fornecedor.objects.get(nome=produto_data['fornecedor_nome'])
                    except Fornecedor.DoesNotExist:
                        pass
                
                Produto.objects.create(
                    nome=produto_data['nome'],
                    codigo_barras=produto_data['codigo_barras'],
                    preco=produto_data['preco'],
                    preco_compra=produto_data['preco_compra'],
                    descricao=produto_data['descricao'],
                    fornecedor=fornecedor,
                    data_hora=datetime.fromisoformat(produto_data['data_hora']),
                    unidade=produto_data['unidade'],
                    quantidade=produto_data['quantidade'],
                    validade=datetime.fromisoformat(produto_data['validade']).date() if produto_data['validade'] else None,
                    observacao=produto_data['observacao']
                )
        
        # Restaurar Orçamentos
        for orcamento_data in backup_data['orcamentos']:
            Orcamento.objects.create(
                cliente=orcamento_data['cliente'],
                cnpj=orcamento_data['cnpj'],
                endereco=orcamento_data['endereco'],
                cidade=orcamento_data['cidade'],
                uf=orcamento_data['uf'],
                telefone=orcamento_data['telefone'],
                email=orcamento_data['email'],
                itens_unidades=orcamento_data['itens_unidades'],
                descricao=orcamento_data['descricao'],
                itens_quantidades=orcamento_data['itens_quantidades'],
                itens_valores=orcamento_data['itens_valores'],
                observacao=orcamento_data['observacao'],
                desconto=orcamento_data['desconto'],
                data=datetime.fromisoformat(orcamento_data['data']).date()
            )
        
        # Restaurar Admins
        for admin_data in backup_data['admins']:
            if not Admin.objects.filter(email=admin_data['email']).exists():
                Admin.objects.create(
                    email=admin_data['email'],
                    senha=admin_data['senha']
                )
        
        print("DADOS RESTAURADOS COM SUCESSO!")
        print(f"Usuarios: {Usuario.objects.count()}")
        print(f"Clientes: {Cliente.objects.count()}")
        print(f"Fornecedores: {Fornecedor.objects.count()}")
        print(f"Produtos: {Produto.objects.count()}")
        print(f"Orcamentos: {Orcamento.objects.count()}")
        print(f"Admins: {Admin.objects.count()}")
        
    except FileNotFoundError:
        print("ERRO: Arquivo backup_dados.json nao encontrado!")
    except Exception as e:
        print(f"ERRO ao restaurar dados: {str(e)}")

if __name__ == "__main__":
    restaurar_dados()