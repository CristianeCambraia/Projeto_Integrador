#!/usr/bin/env python
import os
import sys
import shutil
from pathlib import Path

def limpar_cache_completo():
    """Remove todos os tipos de cache possíveis"""
    
    # Diretório base do projeto
    base_dir = Path(__file__).parent
    
    print("Limpando cache completo...")
    
    # 1. Remover arquivos .pyc
    for pyc_file in base_dir.rglob("*.pyc"):
        try:
            pyc_file.unlink()
            print(f"   Removido: {pyc_file}")
        except:
            pass
    
    # 2. Remover pastas __pycache__
    for pycache_dir in base_dir.rglob("__pycache__"):
        try:
            shutil.rmtree(pycache_dir)
            print(f"   Removido: {pycache_dir}")
        except:
            pass
    
    # 3. Criar arquivo de timestamp para forçar reload
    timestamp_file = base_dir / "static" / "cache_bust.txt"
    with open(timestamp_file, "w") as f:
        import time
        f.write(str(int(time.time())))
    
    print("   Arquivo de cache bust criado")
    
    # 4. Mostrar instruções
    print("\nPROXIMOS PASSOS:")
    print("1. Pare o servidor Django (Ctrl+C)")
    print("2. Execute: python manage.py runserver")
    print("3. Abra o navegador em modo privado/anonimo")
    print("4. Ou pressione Ctrl+Shift+R para hard refresh")
    
    print("\nLimpeza completa finalizada!")

if __name__ == "__main__":
    limpar_cache_completo()