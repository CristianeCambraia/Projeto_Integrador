import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Fornecedor, Produto, Notificacao
from django.utils import timezone

def criar_produtos_baixa_saida():
    """Cria produtos com data antiga para gerar notificações de baixa saída"""
    print("Criando produtos com baixa saída...")
    
    fornecedores = list(Fornecedor.objects.all())
    if not fornecedores:
        print("Erro: Não há fornecedores no banco")
        return
    
    # Criar 5 produtos com data muito antiga (mais de 90 dias)
    produtos_antigos = [
        {"nome": "Equipamento de Ultrassom Antigo", "codigo_barras": "ULTRA001", "preco": Decimal("8500.00"), "quantidade": 120, "dias_atras": 150},
        {"nome": "Monitor Cardíaco Parado", "codigo_barras": "CARD001", "preco": Decimal("12000.00"), "quantidade": 95, "dias_atras": 180},
        {"nome": "Ventilador Mecânico Estocado", "codigo_barras": "VENT001", "preco": Decimal("25000.00"), "quantidade": 200, "dias_atras": 120},
        {"nome": "Desfibrilador Sem Saída", "codigo_barras": "DESF001", "preco": Decimal("15000.00"), "quantidade": 85, "dias_atras": 200},
        {"nome": "Bomba de Infusão Parada", "codigo_barras": "BOMB001", "preco": Decimal("3500.00"), "quantidade": 150, "dias_atras": 100}
    ]
    
    for dados in produtos_antigos:
        # Calcular data antiga
        data_antiga = timezone.now() - timedelta(days=dados['dias_atras'])
        
        produto = Produto.objects.create(
            nome=dados['nome'],
            codigo_barras=dados['codigo_barras'],
            preco=dados['preco'],
            quantidade=dados['quantidade'],
            validade=datetime.now().date() + timedelta(days=365),  # Validade OK
            fornecedor=fornecedores[0],
            data_hora=data_antiga  # Data antiga para simular baixa saída
        )
        
        # Criar notificação de baixa saída
        Notificacao.objects.create(
            tipo="BAIXA_SAIDA",
            titulo="Produto com baixa saída",
            mensagem=f"{produto.nome} - {produto.quantidade} unidades paradas há {dados['dias_atras']} dias no estoque",
            produto=produto
        )
        
        print(f"Criado: {produto.nome} - {dados['dias_atras']} dias parado")
    
    print(f"Criados {len(produtos_antigos)} produtos com baixa saída!")

if __name__ == "__main__":
    criar_produtos_baixa_saida()