#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Orcamento

print("=== DEBUG DA VIEW ORCAMENTOS_EMITIDOS ===")

# Simular o que a view faz
filtro = None  # Sem filtro
orcamentos = Orcamento.objects.all()

if filtro:
    filtro = filtro.strip()
    if filtro.isdigit():
        orcamentos = orcamentos.filter(id=int(filtro))
    else:
        try:
            from datetime import datetime
            if '/' in filtro:
                data_filtro = datetime.strptime(filtro, '%d/%m/%Y').date()
                orcamentos = orcamentos.filter(data=data_filtro)
            else:
                orcamentos = orcamentos.filter(cliente__icontains=filtro)
        except ValueError:
            orcamentos = orcamentos.filter(cliente__icontains=filtro)

orcamentos = orcamentos.order_by('-data')

print(f"Total de orçamentos encontrados: {orcamentos.count()}")
print(f"Filtro aplicado: {filtro}")

print("\nOrçamentos que seriam exibidos:")
for orc in orcamentos:
    print(f"   ID: {orc.id} - Cliente: {orc.cliente} - Data: {orc.data}")

# Verificar especificamente Fernando Campos
fernando_orcamentos = Orcamento.objects.filter(cliente__icontains="fernando")
print(f"\nOrçamentos de Fernando Campos: {fernando_orcamentos.count()}")
for orc in fernando_orcamentos:
    print(f"   ID: {orc.id} - Cliente: {orc.cliente} - Data: {orc.data}")

# Verificar processamento de itens
print(f"\nProcessamento de itens do primeiro orçamento de Fernando:")
if fernando_orcamentos.exists():
    orc = fernando_orcamentos.first()
    
    unidades = [p.strip() for p in orc.itens_unidades.split(' / ')] if orc.itens_unidades else []
    descricoes = [p.strip() for p in orc.descricao.split(' / ')] if orc.descricao else []
    quantidades = [p.strip() for p in orc.itens_quantidades.split(' / ')] if orc.itens_quantidades else []
    valores = [p.strip() for p in orc.itens_valores.split(' / ')] if orc.itens_valores else []
    
    print(f"   Unidades: {unidades}")
    print(f"   Descrições: {descricoes}")
    print(f"   Quantidades: {quantidades}")
    print(f"   Valores: {valores}")
    
    max_itens = max(len(unidades), len(descricoes), len(quantidades), len(valores))
    print(f"   Max itens: {max_itens}")
    
    itens = []
    subtotal = 0
    for i in range(max_itens):
        quantidade = quantidades[i] if i < len(quantidades) else ''
        valor = valores[i] if i < len(valores) else ''
        
        try:
            qtd = float(quantidade.replace(',', '.')) if quantidade else 0
            val = float(valor.replace(',', '.')) if valor else 0
            subtotal += qtd * val
        except ValueError:
            pass
        
        itens.append({
            'unidade': unidades[i] if i < len(unidades) else '',
            'descricao': descricoes[i] if i < len(descricoes) else '',
            'quantidade': quantidade,
            'valor': valor
        })
    
    print(f"   Itens processados: {len(itens)}")
    print(f"   Subtotal: {subtotal}")
else:
    print("   Nenhum orçamento de Fernando encontrado")