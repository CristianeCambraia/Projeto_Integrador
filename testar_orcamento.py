#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Orcamento
from datetime import date

# Criar orçamento de teste para Fernando Campos
try:
    orcamento_teste = Orcamento.objects.create(
        cliente="Fernando Campos",
        cnpj="12.345.678/0001-90",
        endereco="Rua Teste, 123",
        cidade="Pouso Alegre",
        uf="MG",
        telefone="(35) 99999-9999",
        email="fernando@teste.com",
        itens_unidades="Serviço",
        descricao="Consultoria em TI",
        itens_quantidades="1",
        itens_valores="500.00",
        observacao="Orçamento de teste",
        desconto=0,
        data=date.today()
    )
    
    print(f"ORCAMENTO CRIADO COM SUCESSO!")
    print(f"   ID: {orcamento_teste.id}")
    print(f"   Cliente: {orcamento_teste.cliente}")
    print(f"   Data: {orcamento_teste.data}")
    print(f"   Descricao: {orcamento_teste.descricao}")
    
    # Verificar se foi salvo
    verificacao = Orcamento.objects.get(id=orcamento_teste.id)
    print(f"VERIFICACAO: Orcamento encontrado no banco - {verificacao.cliente}")
    
except Exception as e:
    print(f"ERRO ao criar orcamento: {str(e)}")
    import traceback
    traceback.print_exc()

# Listar todos os orçamentos
print(f"\nTODOS OS ORCAMENTOS NO SISTEMA:")
orcamentos = Orcamento.objects.all().order_by('-id')
for orc in orcamentos:
    print(f"   ID: {orc.id} - Cliente: {orc.cliente} - Data: {orc.data}")