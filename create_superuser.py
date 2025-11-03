#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'insumed.sistema2025@hotmail.com', 'Insumed2025')
    print('Superusuário criado: admin / Insumed2025')
else:
    print('Superusuário já existe')