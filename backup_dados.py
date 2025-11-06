#!/usr/bin/env python
import os
import sys
import django
import json
from datetime import date, datetime

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Usuario, Cliente, Fornecedor, Produto, Orcamento, Admin

def serialize_date(obj):
    """Serializar datas para JSON"""
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

def fazer_backup():
    """Fazer backup de todos os dados importantes"""
    backup_data = {
        'usuarios': [],
        'clientes': [],
        'fornecedores': [],
        'produtos': [],
        'orcamentos': [],
        'admins': []
    }
    
    # Backup Usuários
    for usuario in Usuario.objects.all():
        backup_data['usuarios'].append({
            'nome': usuario.nome,
            'email': usuario.email,
            'cpf': usuario.cpf,
            'endereco': usuario.endereco,
            'cidade': usuario.cidade,
            'uf': usuario.uf,
            'telefone': usuario.telefone,
            'data_nascimento': usuario.data_nascimento,
            'senha': usuario.senha,
            'ativo': usuario.ativo
        })
    
    # Backup Clientes
    for cliente in Cliente.objects.all():
        backup_data['clientes'].append({
            'nome': cliente.nome,
            'cpf': cliente.cpf,
            'endereco': cliente.endereco,
            'bairro': cliente.bairro,
            'complemento': cliente.complemento,
            'data_nascimento': cliente.data_nascimento,
            'cidade': cliente.cidade,
            'uf': cliente.uf,
            'cep': cliente.cep,
            'email': cliente.email,
            'telefone': cliente.telefone
        })
    
    # Backup Fornecedores
    for fornecedor in Fornecedor.objects.all():
        backup_data['fornecedores'].append({
            'nome': fornecedor.nome,
            'cnpj': fornecedor.cnpj,
            'endereco': fornecedor.endereco,
            'bairro': fornecedor.bairro,
            'complemento': fornecedor.complemento,
            'data_nascimento': fornecedor.data_nascimento,
            'cidade': fornecedor.cidade,
            'uf': fornecedor.uf,
            'cep': fornecedor.cep,
            'email': fornecedor.email,
            'telefone': fornecedor.telefone,
            'ativo': fornecedor.ativo
        })
    
    # Backup Produtos
    for produto in Produto.objects.all():
        backup_data['produtos'].append({
            'nome': produto.nome,
            'codigo_barras': produto.codigo_barras,
            'preco': float(produto.preco) if produto.preco else 0,
            'preco_compra': float(produto.preco_compra) if produto.preco_compra else 0,
            'descricao': produto.descricao,
            'fornecedor_nome': produto.fornecedor.nome if produto.fornecedor else None,
            'data_hora': produto.data_hora,
            'unidade': produto.unidade,
            'quantidade': produto.quantidade,
            'validade': produto.validade,
            'observacao': produto.observacao
        })
    
    # Backup Orçamentos
    for orcamento in Orcamento.objects.all():
        backup_data['orcamentos'].append({
            'cliente': orcamento.cliente,
            'cnpj': orcamento.cnpj,
            'endereco': orcamento.endereco,
            'cidade': orcamento.cidade,
            'uf': orcamento.uf,
            'telefone': orcamento.telefone,
            'email': orcamento.email,
            'itens_unidades': orcamento.itens_unidades,
            'descricao': orcamento.descricao,
            'itens_quantidades': orcamento.itens_quantidades,
            'itens_valores': orcamento.itens_valores,
            'observacao': orcamento.observacao,
            'desconto': float(orcamento.desconto) if orcamento.desconto else 0,
            'data': orcamento.data
        })
    
    # Backup Admins
    for admin in Admin.objects.all():
        backup_data['admins'].append({
            'email': admin.email,
            'senha': admin.senha
        })
    
    # Salvar backup em arquivo JSON
    with open('backup_dados.json', 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2, default=serialize_date)
    
    print("BACKUP REALIZADO COM SUCESSO!")
    print(f"Usuarios: {len(backup_data['usuarios'])}")
    print(f"Clientes: {len(backup_data['clientes'])}")
    print(f"Fornecedores: {len(backup_data['fornecedores'])}")
    print(f"Produtos: {len(backup_data['produtos'])}")
    print(f"Orcamentos: {len(backup_data['orcamentos'])}")
    print(f"Admins: {len(backup_data['admins'])}")
    print(f"Arquivo salvo: backup_dados.json")

if __name__ == "__main__":
    fazer_backup()