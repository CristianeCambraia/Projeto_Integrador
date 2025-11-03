#!/usr/bin/env python
import os
import django
from datetime import datetime, timedelta
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Fornecedor, Produto, Cliente, Usuario, Servico, Notificacao

def populate_data():
    print("Populando dados fictícios...")
    
    # Fornecedores
    fornecedores_data = [
        {"nome": "MedSupply Ltda", "cnpj": "12.345.678/0001-90", "telefone": "(11) 3456-7890", "email": "contato@medsupply.com", "endereco": "Rua das Flores, 123", "bairro": "Centro", "cidade": "São Paulo", "uf": "SP", "cep": "01234-567", "data_nascimento": datetime.now().date()},
        {"nome": "FarmaDistribuidora", "cnpj": "98.765.432/0001-10", "telefone": "(21) 2345-6789", "email": "vendas@farmadist.com", "endereco": "Av. Brasil, 456", "bairro": "Copacabana", "cidade": "Rio de Janeiro", "uf": "RJ", "cep": "20123-456", "data_nascimento": datetime.now().date()},
        {"nome": "EquipMed Brasil", "cnpj": "11.222.333/0001-44", "telefone": "(31) 3333-4444", "email": "equipmed@gmail.com", "endereco": "Rua Minas, 789", "bairro": "Savassi", "cidade": "Belo Horizonte", "uf": "MG", "cep": "30123-789", "data_nascimento": datetime.now().date()},
    ]
    
    for f_data in fornecedores_data:
        fornecedor, created = Fornecedor.objects.get_or_create(
            cnpj=f_data["cnpj"],
            defaults=f_data
        )
        if created:
            print(f"Fornecedor criado: {fornecedor.nome}")
    
    # Produtos com diferentes situações de estoque
    produtos_data = [
        # Produtos com estoque baixo (notificação)
        {"nome": "Dipirona 500mg", "fornecedor": "MedSupply Ltda", "preco": 15.50, "quantidade": 8, "estoque_minimo": 10, "validade": datetime.now() + timedelta(days=180)},
        {"nome": "Paracetamol 750mg", "fornecedor": "FarmaDistribuidora", "preco": 12.30, "quantidade": 3, "estoque_minimo": 15, "validade": datetime.now() + timedelta(days=120)},
        
        # Produtos vencidos (notificação)
        {"nome": "Ibuprofeno 600mg", "fornecedor": "MedSupply Ltda", "preco": 18.90, "quantidade": 25, "estoque_minimo": 10, "validade": datetime.now() - timedelta(days=5)},
        {"nome": "Amoxicilina 500mg", "fornecedor": "EquipMed Brasil", "preco": 22.40, "quantidade": 12, "estoque_minimo": 8, "validade": datetime.now() - timedelta(days=15)},
        
        # Produtos próximos ao vencimento (notificação)
        {"nome": "Omeprazol 20mg", "fornecedor": "FarmaDistribuidora", "preco": 28.70, "quantidade": 30, "estoque_minimo": 12, "validade": datetime.now() + timedelta(days=25)},
        {"nome": "Losartana 50mg", "fornecedor": "MedSupply Ltda", "preco": 35.60, "quantidade": 18, "estoque_minimo": 10, "validade": datetime.now() + timedelta(days=20)},
        
        # Produtos com estoque zerado (notificação)
        {"nome": "Insulina NPH", "fornecedor": "EquipMed Brasil", "preco": 45.80, "quantidade": 0, "estoque_minimo": 5, "validade": datetime.now() + timedelta(days=90)},
        {"nome": "Captopril 25mg", "fornecedor": "FarmaDistribuidora", "preco": 16.20, "quantidade": 0, "estoque_minimo": 20, "validade": datetime.now() + timedelta(days=150)},
        
        # Produtos normais
        {"nome": "Atenolol 50mg", "fornecedor": "MedSupply Ltda", "preco": 19.90, "quantidade": 50, "estoque_minimo": 15, "validade": datetime.now() + timedelta(days=300)},
        {"nome": "Metformina 850mg", "fornecedor": "EquipMed Brasil", "preco": 24.50, "quantidade": 75, "estoque_minimo": 20, "validade": datetime.now() + timedelta(days=250)},
    ]
    
    for p_data in produtos_data:
        fornecedor = Fornecedor.objects.get(nome=p_data["fornecedor"])
        produto, created = Produto.objects.get_or_create(
            nome=p_data["nome"],
            fornecedor=fornecedor,
            defaults={
                "preco": Decimal(str(p_data["preco"])),
                "quantidade": p_data["quantidade"],
                "estoque_minimo": p_data["estoque_minimo"],
                "validade": p_data["validade"],
                "unidade": "UN",
                "observacao": "Produto de teste"
            }
        )
        if created:
            print(f"Produto criado: {produto.nome}")
    
    # Clientes
    clientes_data = [
        {"nome": "Hospital São Lucas", "cpf": "12.345.678/0001-90", "telefone": "(11) 3456-7890", "email": "compras@saolucas.com", "endereco": "Av. Paulista, 1000", "bairro": "Bela Vista", "cidade": "São Paulo", "uf": "SP", "cep": "01310-100", "data_nascimento": datetime.now().date()},
        {"nome": "Clínica Vida Nova", "cpf": "98.765.432/0001-10", "telefone": "(21) 2345-6789", "email": "clinica@vidanova.com", "endereco": "Rua Copacabana, 500", "bairro": "Copacabana", "cidade": "Rio de Janeiro", "uf": "RJ", "cep": "22070-010", "data_nascimento": datetime.now().date()},
        {"nome": "Dr. João Silva", "cpf": "123.456.789-01", "telefone": "(31) 9876-5432", "email": "drjoao@gmail.com", "endereco": "Rua das Acácias, 200", "bairro": "Centro", "cidade": "Belo Horizonte", "uf": "MG", "cep": "30112-000", "data_nascimento": datetime.now().date()},
        {"nome": "Farmácia Popular", "cpf": "11.222.333/0001-44", "telefone": "(85) 3333-4444", "email": "popular@farmacia.com", "endereco": "Av. Beira Mar, 300", "bairro": "Meireles", "cidade": "Fortaleza", "uf": "CE", "cep": "60165-121", "data_nascimento": datetime.now().date()},
    ]
    
    for c_data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            cpf=c_data["cpf"],
            defaults=c_data
        )
        if created:
            print(f"Cliente criado: {cliente.nome}")
    
    # Usuários
    usuarios_data = [
        {"nome": "Maria Santos", "email": "maria@insumed.com", "cpf": "111.222.333-44", "endereco": "Rua A, 100", "telefone": "(11) 9999-8888", "data_nascimento": datetime.now().date(), "senha": "senha123"},
        {"nome": "Pedro Oliveira", "email": "pedro@insumed.com", "cpf": "222.333.444-55", "endereco": "Rua B, 200", "telefone": "(21) 8888-7777", "data_nascimento": datetime.now().date(), "senha": "senha123"},
        {"nome": "Ana Costa", "email": "ana@insumed.com", "cpf": "333.444.555-66", "endereco": "Rua C, 300", "telefone": "(31) 7777-6666", "data_nascimento": datetime.now().date(), "senha": "senha123"},
    ]
    
    for u_data in usuarios_data:
        usuario, created = Usuario.objects.get_or_create(
            email=u_data["email"],
            defaults=u_data
        )
        if created:
            print(f"Usuário criado: {usuario.nome}")
    
    # Serviços
    servicos_data = [
        {"nome": "Consultoria Farmacêutica", "descricao": "Consultoria especializada em gestão farmacêutica", "preco": Decimal("150.00"), "unidade": "Hora"},
        {"nome": "Auditoria de Estoque", "descricao": "Auditoria completa do estoque de medicamentos", "preco": Decimal("300.00"), "unidade": "Serviço"},
        {"nome": "Treinamento de Equipe", "descricao": "Treinamento para equipe de farmácia", "preco": Decimal("200.00"), "unidade": "Hora"},
        {"nome": "Implementação de Sistema", "descricao": "Implementação e configuração do sistema", "preco": Decimal("500.00"), "unidade": "Projeto"},
    ]
    
    for s_data in servicos_data:
        servico, created = Servico.objects.get_or_create(
            nome=s_data["nome"],
            defaults=s_data
        )
        if created:
            print(f"Serviço criado: {servico.nome}")
    
    # Criar notificações para todos os tipos
    criar_notificacoes()
    
    print("✅ Dados fictícios populados com sucesso!")

def criar_notificacoes():
    print("Criando notificações...")
    
    # Notificações de estoque baixo
    produtos_baixo = Produto.objects.filter(quantidade__lt=10, quantidade__gt=0)
    for produto in produtos_baixo:
        Notificacao.objects.get_or_create(
            produto=produto,
            tipo='estoque_baixo',
            defaults={'mensagem': f'Estoque baixo: {produto.quantidade} unidades restantes'}
        )
    
    # Notificações de estoque zerado
    produtos_zerado = Produto.objects.filter(quantidade=0)
    for produto in produtos_zerado:
        Notificacao.objects.get_or_create(
            produto=produto,
            tipo='estoque_zerado',
            defaults={'mensagem': 'Produto sem estoque disponível'}
        )
    
    # Notificações de produtos vencidos
    produtos_vencidos = Produto.objects.filter(validade__lt=datetime.now().date())
    for produto in produtos_vencidos:
        Notificacao.objects.get_or_create(
            produto=produto,
            tipo='produto_vencido',
            defaults={'mensagem': f'Produto vencido em {produto.validade.strftime("%d/%m/%Y")}'}
        )
    
    # Notificações de produtos próximos ao vencimento
    data_limite = datetime.now().date() + timedelta(days=30)
    produtos_vencimento = Produto.objects.filter(
        validade__gt=datetime.now().date(),
        validade__lte=data_limite
    )
    for produto in produtos_vencimento:
        dias_restantes = (produto.validade - datetime.now().date()).days
        Notificacao.objects.get_or_create(
            produto=produto,
            tipo='proximo_vencimento',
            defaults={'mensagem': f'Vence em {dias_restantes} dias ({produto.validade.strftime("%d/%m/%Y")})'}
        )
    
    print(f"✅ {Notificacao.objects.count()} notificações criadas!")

if __name__ == '__main__':
    populate_data()