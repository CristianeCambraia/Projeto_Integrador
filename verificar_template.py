#!/usr/bin/env python
import os
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from django.template.loader import get_template

def verificar_template():
    print("Verificando qual template está sendo usado...")
    
    try:
        # Carregar o template do balancete
        template = get_template('balancete.html')
        
        # Ler o conteúdo do arquivo
        with open(template.origin.name, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"Template encontrado em: {template.origin.name}")
        
        # Verificar se contém PREJUÍZO
        if 'PREJUÍZO' in content or 'prejuízo' in content:
            print("PROBLEMA: Template ainda contém 'PREJUÍZO'")
            
            # Mostrar linhas que contêm prejuízo
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'prejuízo' in line.lower():
                    print(f"   Linha {i}: {line.strip()}")
        else:
            print("Template correto: não contém 'PREJUÍZO'")
        
        # Verificar se contém SALDO
        if 'SALDO' in content:
            print("Template correto: contém 'SALDO'")
        else:
            print("PROBLEMA: Template não contém 'SALDO'")
            
        # Verificar cache bust
        if 'CACHE BUST' in content:
            print("Cache bust presente")
        else:
            print("Cache bust ausente")
            
    except Exception as e:
        print(f"Erro ao verificar template: {e}")

if __name__ == "__main__":
    verificar_template()