#!/usr/bin/env python
import os
import sys
import django
import json
import requests

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from app.models import Produto

def testar_busca_local():
    """Testa a busca diretamente no banco"""
    print("=== TESTE LOCAL ===")
    
    # Listar produtos com código de barras
    produtos = Produto.objects.filter(codigo_barras__isnull=False).exclude(codigo_barras='')
    print(f"Produtos com código de barras: {produtos.count()}")
    
    for produto in produtos:
        print(f"ID: {produto.id}, Nome: '{produto.nome}', Código: '{produto.codigo_barras}'")
        
        # Testar busca exata
        try:
            encontrado = Produto.objects.get(codigo_barras=produto.codigo_barras)
            print(f"[OK] Busca exata funcionou para código '{produto.codigo_barras}'")
        except Produto.DoesNotExist:
            print(f"[ERRO] Busca exata falhou para código '{produto.codigo_barras}'")

def testar_busca_api():
    """Testa a busca via API"""
    print("\n=== TESTE API ===")
    
    # Testar com código conhecido
    codigo_teste = "111111"
    
    try:
        response = requests.post(
            'http://127.0.0.1:8000/buscar-produto-por-codigo/',
            json={'codigo_barras': codigo_teste},
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Resposta da API para código '{codigo_teste}': {data}")
        else:
            print(f"Erro na API: Status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("[ERRO] Servidor não está rodando. Execute: python manage.py runserver")
    except Exception as e:
        print(f"[ERRO] Erro na requisição: {e}")

if __name__ == "__main__":
    testar_busca_local()
    testar_busca_api()