#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Usuario

# Verificar se existe o usuário
email_procurado = "zairandcruz@hotmail.com"

try:
    usuario = Usuario.objects.get(email=email_procurado)
    print(f"USUARIO ENCONTRADO:")
    print(f"   Nome: {usuario.nome}")
    print(f"   Email: {usuario.email}")
    print(f"   CPF: {usuario.cpf}")
    print(f"   Cidade: {usuario.cidade}")
    print(f"   UF: {usuario.uf}")
    print(f"   Telefone: {usuario.telefone}")
    print(f"   Data Nascimento: {usuario.data_nascimento}")
    print(f"   Ativo: {usuario.ativo}")
except Usuario.DoesNotExist:
    print(f"USUARIO NAO ENCONTRADO: {email_procurado}")
    
    # Mostrar todos os emails cadastrados para comparação
    print("\nEmails cadastrados no sistema:")
    usuarios = Usuario.objects.all().order_by('email')
    if usuarios:
        for u in usuarios:
            print(f"   - {u.email} ({u.nome})")
    else:
        print("   Nenhum usuario cadastrado no sistema")