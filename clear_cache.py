#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
    django.setup()
    
    # Limpar cache de templates
    from django.template.loader import get_template
    from django.template import engines
    
    # Recarregar engine de templates
    for engine in engines.all():
        if hasattr(engine, 'env'):
            engine.env.cache.clear()
    
    print("Cache de templates limpo com sucesso!")