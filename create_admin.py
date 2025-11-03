#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Admin

# Criar admin customizado
if not Admin.objects.filter(email='insumed.sistema2025@hotmail.com').exists():
    Admin.objects.create(
        email='insumed.sistema2025@hotmail.com',
        senha='Insumed2025'
    )
    print('Admin criado: insumed.sistema2025@hotmail.com / Insumed2025')
else:
    print('Admin já existe')