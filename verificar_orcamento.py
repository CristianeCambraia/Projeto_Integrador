#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Orcamento

# Verificar orçamentos para Fernando Campos
nome_procurado = "fernando campos"

print("=== VERIFICANDO ORCAMENTOS ===")

# Buscar orçamentos que contenham "fernando" no nome (case insensitive)
orcamentos_fernando = Orcamento.objects.filter(cliente__icontains="fernando")

if orcamentos_fernando:
    print(f"ORCAMENTOS ENCONTRADOS para '{nome_procurado}':")
    for orc in orcamentos_fernando:
        print(f"   ID: {orc.id}")
        print(f"   Cliente: {orc.cliente}")
        print(f"   Data: {orc.data}")
        print(f"   Email: {orc.email}")
        print(f"   Telefone: {orc.telefone}")
        print(f"   Cidade: {orc.cidade}")
        print(f"   ---")
else:
    print(f"NENHUM ORCAMENTO ENCONTRADO para '{nome_procurado}'")

# Mostrar os últimos 10 orçamentos cadastrados
print("\n=== ULTIMOS 10 ORCAMENTOS CADASTRADOS ===")
ultimos_orcamentos = Orcamento.objects.all().order_by('-id')[:10]

if ultimos_orcamentos:
    for orc in ultimos_orcamentos:
        print(f"   ID: {orc.id} - Cliente: {orc.cliente} - Data: {orc.data}")
else:
    print("   Nenhum orçamento cadastrado no sistema")

# Contar total de orçamentos
total = Orcamento.objects.count()
print(f"\nTOTAL DE ORCAMENTOS NO SISTEMA: {total}")