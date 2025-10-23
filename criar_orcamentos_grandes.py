import os
import sys
import django
from datetime import datetime
from decimal import Decimal
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Cliente, Servico, Produto, Orcamento

def criar_orcamentos_grandes():
    """Cria orçamentos com valores altos para testar formatação de milhares"""
    print("Criando orçamentos com valores grandes...")
    
    clientes = list(Cliente.objects.all())
    servicos = list(Servico.objects.all())
    produtos = list(Produto.objects.all())
    
    if not clientes or not produtos:
        print("Erro: Não há clientes ou produtos no banco")
        return
    
    # Criar 3 orçamentos com valores altos
    for i in range(3):
        cliente = random.choice(clientes)
        
        # Criar listas de itens com valores altos
        itens_descricao = []
        itens_quantidades = []
        itens_valores = []
        itens_unidades = []
        
        # Adicionar produtos com valores e quantidades altas
        produtos_selecionados = random.sample(produtos, min(4, len(produtos)))
        
        for produto in produtos_selecionados:
            # Aumentar valores para testar formatação
            quantidade = random.randint(50, 200)
            valor_alto = produto.preco * random.randint(5, 20)  # Multiplicar por 5-20
            
            itens_descricao.append(produto.nome)
            itens_quantidades.append(str(quantidade))
            itens_valores.append(str(valor_alto))
            itens_unidades.append(produto.unidade)
        
        # Adicionar serviços com valores altos
        if servicos:
            servicos_selecionados = random.sample(servicos, min(2, len(servicos)))
            for servico in servicos_selecionados:
                quantidade = random.randint(10, 50)
                valor_alto = servico.preco * random.randint(3, 15)
                
                itens_descricao.append(servico.nome)
                itens_quantidades.append(str(quantidade))
                itens_valores.append(str(valor_alto))
                itens_unidades.append(servico.unidade)
        
        # Desconto alto em reais
        desconto = Decimal(str(random.randint(500, 2000)))
        
        # Criar orçamento
        Orcamento.objects.create(
            cliente=cliente.nome,
            endereco=cliente.endereco,
            cidade=cliente.cidade,
            uf=cliente.uf,
            telefone=cliente.telefone,
            email=cliente.email,
            descricao=' / '.join(itens_descricao),
            itens_quantidades=' / '.join(itens_quantidades),
            itens_valores=' / '.join(itens_valores),
            itens_unidades=' / '.join(itens_unidades),
            observacao=f"Orçamento ALTO VALOR {i+1:03d}/2025 - Desconto especial para grande volume",
            desconto=desconto
        )
    
    print("Criados 3 orçamentos com valores altos!")

if __name__ == "__main__":
    criar_orcamentos_grandes()