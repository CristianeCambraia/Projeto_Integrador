import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Fornecedor, Cliente, Produto, Servico, Orcamento, Notificacao

def limpar_banco():
    """Limpa todos os dados do banco"""
    print("Limpando banco de dados...")
    Notificacao.objects.all().delete()
    Orcamento.objects.all().delete()
    Produto.objects.all().delete()
    Servico.objects.all().delete()
    Cliente.objects.all().delete()
    Fornecedor.objects.all().delete()
    print("Banco limpo!")

def criar_fornecedores():
    """Cria 5 fornecedores da área da saúde"""
    print("Criando fornecedores...")
    
    fornecedores = [
        {"nome": "MedSupply Ltda", "cnpj": "12.345.678/0001-90", "telefone": "(11) 3456-7890", "email": "contato@medsupply.com.br", "endereco": "Rua das Medicinas, 123", "bairro": "Vila Madalena", "cidade": "São Paulo", "uf": "SP", "cep": "05000-000", "data_nascimento": datetime(1990, 1, 1).date()},
        {"nome": "Hospitalar Distribuidora", "cnpj": "23.456.789/0001-01", "telefone": "(21) 2345-6789", "email": "vendas@hospitalar.com.br", "endereco": "Av. Saúde, 456", "bairro": "Tijuca", "cidade": "Rio de Janeiro", "uf": "RJ", "cep": "20000-000", "data_nascimento": datetime(1985, 6, 15).date()},
        {"nome": "Cirúrgica Premium", "cnpj": "34.567.890/0001-12", "telefone": "(31) 3567-8901", "email": "comercial@cirurgica.com.br", "endereco": "Rua Bisturi, 789", "bairro": "Funcionários", "cidade": "Belo Horizonte", "uf": "MG", "cep": "30000-000", "data_nascimento": datetime(1982, 9, 20).date()},
        {"nome": "Farmacêutica Central", "cnpj": "45.678.901/0001-23", "telefone": "(41) 4678-9012", "email": "pedidos@farmaceutica.com.br", "endereco": "Av. Remédios, 321", "bairro": "Batel", "cidade": "Curitiba", "uf": "PR", "cep": "80000-000", "data_nascimento": datetime(1978, 11, 5).date()},
        {"nome": "Equipamentos Médicos Sul", "cnpj": "56.789.012/0001-34", "telefone": "(51) 5789-0123", "email": "atendimento@equipmed.com.br", "endereco": "Rua Aparelhos, 654", "bairro": "Moinhos de Vento", "cidade": "Porto Alegre", "uf": "RS", "cep": "90000-000", "data_nascimento": datetime(1987, 4, 12).date()}
    ]
    
    for data in fornecedores:
        Fornecedor.objects.create(**data)
    print(f"Criados {len(fornecedores)} fornecedores!")

def criar_clientes():
    """Cria 5 clientes da área da saúde"""
    print("Criando clientes...")
    
    clientes = [
        {"nome": "Hospital São Lucas", "cpf": "11.111.111-11", "telefone": "(11) 1111-1111", "email": "compras@saolucas.com.br", "endereco": "Rua Hospital, 100", "bairro": "Centro", "cidade": "São Paulo", "uf": "SP", "cep": "01000-000", "data_nascimento": datetime(1990, 1, 1).date()},
        {"nome": "Clínica Vida Nova", "cpf": "22.222.222-22", "telefone": "(21) 2222-2222", "email": "suprimentos@vidanova.com.br", "endereco": "Av. Saúde, 200", "bairro": "Copacabana", "cidade": "Rio de Janeiro", "uf": "RJ", "cep": "22000-000", "data_nascimento": datetime(1985, 5, 15).date()},
        {"nome": "Centro Médico Esperança", "cpf": "33.333.333-33", "telefone": "(31) 3333-3333", "email": "compras@esperanca.com.br", "endereco": "Rua Cura, 300", "bairro": "Savassi", "cidade": "Belo Horizonte", "uf": "MG", "cep": "30000-000", "data_nascimento": datetime(1980, 8, 20).date()},
        {"nome": "Hospital Municipal Central", "cpf": "44.444.444-44", "telefone": "(41) 4444-4444", "email": "almoxarifado@municipal.gov.br", "endereco": "Av. Central, 400", "bairro": "Centro", "cidade": "Curitiba", "uf": "PR", "cep": "80000-000", "data_nascimento": datetime(1975, 12, 10).date()},
        {"nome": "Clínica Especializada Norte", "cpf": "55.555.555-55", "telefone": "(51) 5555-5555", "email": "materiais@norte.com.br", "endereco": "Rua Norte, 500", "bairro": "Moinhos", "cidade": "Porto Alegre", "uf": "RS", "cep": "90000-000", "data_nascimento": datetime(1988, 3, 25).date()}
    ]
    
    for data in clientes:
        Cliente.objects.create(**data)
    print(f"Criados {len(clientes)} clientes!")

def criar_servicos():
    """Cria 10 serviços da área da saúde"""
    print("Criando serviços...")
    
    servicos = [
        {"nome": "Manutenção Preventiva de Equipamentos", "descricao": "Manutenção preventiva em equipamentos médicos e hospitalares", "preco": Decimal("450.00")},
        {"nome": "Calibração de Instrumentos Médicos", "descricao": "Calibração e certificação de instrumentos de precisão médica", "preco": Decimal("280.00")},
        {"nome": "Instalação de Sistema de Gases Medicinais", "descricao": "Instalação completa de sistema de distribuição de gases medicinais", "preco": Decimal("1200.00")},
        {"nome": "Treinamento em Equipamentos Médicos", "descricao": "Treinamento técnico para operação de equipamentos médicos", "preco": Decimal("350.00")},
        {"nome": "Consultoria em Gestão Hospitalar", "descricao": "Consultoria especializada em gestão e otimização hospitalar", "preco": Decimal("800.00")},
        {"nome": "Validação de Processos de Esterilização", "descricao": "Validação e certificação de processos de esterilização", "preco": Decimal("650.00")},
        {"nome": "Auditoria em Controle de Infecção", "descricao": "Auditoria completa em protocolos de controle de infecção hospitalar", "preco": Decimal("750.00")},
        {"nome": "Implementação de Sistema de Qualidade", "descricao": "Implementação de sistema de gestão da qualidade hospitalar", "preco": Decimal("950.00")},
        {"nome": "Manutenção Corretiva de Equipamentos", "descricao": "Reparo e manutenção corretiva de equipamentos médicos", "preco": Decimal("320.00")},
        {"nome": "Certificação de Ambiente Controlado", "descricao": "Certificação de salas limpas e ambientes controlados", "preco": Decimal("580.00")}
    ]
    
    for data in servicos:
        Servico.objects.create(**data)
    print(f"Criados {len(servicos)} serviços!")

def criar_produtos():
    """Cria produtos da área da saúde com diferentes situações"""
    print("Criando produtos...")
    
    fornecedores = list(Fornecedor.objects.all())
    
    # Produtos com validade próxima (8 produtos)
    produtos_validade_proxima = [
        {"nome": "Soro Fisiológico 500ml", "codigo_barras": "SF500", "preco": Decimal("3.50"), "quantidade": 45, "validade": datetime.now().date() + timedelta(days=15), "fornecedor": fornecedores[0]},
        {"nome": "Dipirona 500mg", "codigo_barras": "DIP500", "preco": Decimal("12.80"), "quantidade": 28, "validade": datetime.now().date() + timedelta(days=20), "fornecedor": fornecedores[1]},
        {"nome": "Paracetamol 750mg", "codigo_barras": "PAR750", "preco": Decimal("8.90"), "quantidade": 35, "validade": datetime.now().date() + timedelta(days=18), "fornecedor": fornecedores[2]},
        {"nome": "Omeprazol 20mg", "codigo_barras": "OME20", "preco": Decimal("15.60"), "quantidade": 22, "validade": datetime.now().date() + timedelta(days=25), "fornecedor": fornecedores[3]},
        {"nome": "Amoxicilina 500mg", "codigo_barras": "AMO500", "preco": Decimal("18.40"), "quantidade": 18, "validade": datetime.now().date() + timedelta(days=12), "fornecedor": fornecedores[4]},
        {"nome": "Ibuprofeno 600mg", "codigo_barras": "IBU600", "preco": Decimal("11.20"), "quantidade": 31, "validade": datetime.now().date() + timedelta(days=22), "fornecedor": fornecedores[0]},
        {"nome": "Captopril 25mg", "codigo_barras": "CAP25", "preco": Decimal("9.75"), "quantidade": 26, "validade": datetime.now().date() + timedelta(days=16), "fornecedor": fornecedores[1]},
        {"nome": "Losartana 50mg", "codigo_barras": "LOS50", "preco": Decimal("13.90"), "quantidade": 29, "validade": datetime.now().date() + timedelta(days=19), "fornecedor": fornecedores[2]}
    ]
    
    # Produtos com estoque crítico (8 produtos)
    produtos_estoque_critico = [
        {"nome": "Luvas Cirúrgicas Estéreis", "codigo_barras": "LCE001", "preco": Decimal("45.00"), "quantidade": 3, "validade": datetime.now().date() + timedelta(days=180), "fornecedor": fornecedores[0]},
        {"nome": "Máscara N95", "codigo_barras": "MN95", "preco": Decimal("8.50"), "quantidade": 2, "validade": datetime.now().date() + timedelta(days=365), "fornecedor": fornecedores[1]},
        {"nome": "Seringa 10ml Descartável", "codigo_barras": "SER10", "preco": Decimal("1.20"), "quantidade": 4, "validade": datetime.now().date() + timedelta(days=720), "fornecedor": fornecedores[2]},
        {"nome": "Cateter Venoso Central", "codigo_barras": "CVC001", "preco": Decimal("85.00"), "quantidade": 1, "validade": datetime.now().date() + timedelta(days=540), "fornecedor": fornecedores[3]},
        {"nome": "Fio de Sutura Absorvível", "codigo_barras": "FSA001", "preco": Decimal("25.80"), "quantidade": 3, "validade": datetime.now().date() + timedelta(days=450), "fornecedor": fornecedores[4]},
        {"nome": "Eletrodo Descartável", "codigo_barras": "ELE001", "preco": Decimal("2.40"), "quantidade": 2, "validade": datetime.now().date() + timedelta(days=300), "fornecedor": fornecedores[0]},
        {"nome": "Sonda Nasogástrica", "codigo_barras": "SNG001", "preco": Decimal("12.60"), "quantidade": 4, "validade": datetime.now().date() + timedelta(days=600), "fornecedor": fornecedores[1]},
        {"nome": "Compressa Estéril", "codigo_barras": "CE001", "preco": Decimal("3.80"), "quantidade": 1, "validade": datetime.now().date() + timedelta(days=240), "fornecedor": fornecedores[2]}
    ]
    
    # Produtos com baixa saída (5 produtos)
    produtos_baixa_saida = [
        {"nome": "Equipamento Raio-X Portátil", "codigo_barras": "RXP001", "preco": Decimal("15000.00"), "quantidade": 150, "validade": datetime.now().date() + timedelta(days=1800), "fornecedor": fornecedores[3]},
        {"nome": "Monitor Multiparâmetros", "codigo_barras": "MMP001", "preco": Decimal("8500.00"), "quantidade": 85, "validade": datetime.now().date() + timedelta(days=1500), "fornecedor": fornecedores[4]},
        {"nome": "Desfibrilador Automático", "codigo_barras": "DEF001", "preco": Decimal("12000.00"), "quantidade": 120, "validade": datetime.now().date() + timedelta(days=2000), "fornecedor": fornecedores[0]},
        {"nome": "Ventilador Pulmonar", "codigo_barras": "VP001", "preco": Decimal("25000.00"), "quantidade": 95, "validade": datetime.now().date() + timedelta(days=1650), "fornecedor": fornecedores[1]},
        {"nome": "Bomba de Infusão", "codigo_barras": "BI001", "preco": Decimal("3500.00"), "quantidade": 200, "validade": datetime.now().date() + timedelta(days=1200), "fornecedor": fornecedores[2]}
    ]
    
    # Produtos normais (50 produtos)
    nomes_produtos = [
        "Álcool 70%", "Água Oxigenada", "Betadine", "Gaze Estéril", "Esparadrapo", "Atadura Elástica",
        "Termômetro Digital", "Esfigmomanômetro", "Estetoscópio", "Otoscópio", "Oftalmoscópio",
        "Bisturi Descartável", "Pinça Anatômica", "Tesoura Cirúrgica", "Porta-agulhas", "Afastador",
        "Cânula Nasal", "Máscara de Oxigênio", "Nebulizador", "Aspirador Portátil", "Oxímetro",
        "Glicosímetro", "Tiras Glicemia", "Lancetas", "Algodão Hidrófilo", "Curativo Adesivo",
        "Band-Aid", "Micropore", "Sonda Vesical", "Coletor de Urina", "Frasco Coletor",
        "Agulha 25x7", "Agulha 30x8", "Agulha 40x12", "Seringa 1ml", "Seringa 3ml", "Seringa 5ml",
        "Scalp 21G", "Scalp 23G", "Scalp 25G", "Equipo Macrogotas", "Equipo Microgotas",
        "Soro Glicosado 5%", "Soro Ringer", "Manitol 20%", "Bicarbonato de Sódio", "Cloreto de Sódio",
        "Heparina", "Insulina NPH", "Insulina Regular", "Adrenalina"
    ]
    
    produtos_normais = []
    for i, nome in enumerate(nomes_produtos):
        produto = {
            "nome": nome,
            "codigo_barras": f"PROD{i+22:03d}",
            "preco": Decimal(str(round(random.uniform(5.0, 500.0), 2))),
            "quantidade": random.randint(20, 80),
            "validade": datetime.now().date() + timedelta(days=random.randint(90, 1095)),
            "fornecedor": random.choice(fornecedores)
        }
        produtos_normais.append(produto)
    
    # Criar todos os produtos
    todos_produtos = produtos_validade_proxima + produtos_estoque_critico + produtos_baixa_saida + produtos_normais
    
    for data in todos_produtos:
        Produto.objects.create(**data)
    
    print(f"Criados {len(todos_produtos)} produtos!")

def criar_orcamentos():
    """Cria alguns orçamentos de exemplo com itens separados"""
    print("Criando orçamentos...")
    
    clientes = list(Cliente.objects.all())
    servicos = list(Servico.objects.all())
    produtos = list(Produto.objects.all()[:20])
    
    observacoes_desconto = [
        "Desconto à vista",
        "Desconto por pagamento antecipado",
        "Desconto para cliente fiel",
        "Promoção especial",
        "Desconto por volume",
        "Condição especial"
    ]
    
    for i in range(15):
        cliente = random.choice(clientes)
        
        # Criar listas de itens separados
        itens_descricao = []
        itens_quantidades = []
        itens_valores = []
        itens_unidades = []
        
        # Adicionar serviços (1-2 itens)
        num_servicos = random.randint(1, 2)
        servicos_selecionados = random.sample(servicos, min(num_servicos, len(servicos)))
        
        for servico in servicos_selecionados:
            quantidade = random.randint(1, 3)
            itens_descricao.append(servico.nome)
            itens_quantidades.append(str(quantidade))
            itens_valores.append(str(servico.preco))
            itens_unidades.append(servico.unidade)
        
        # Adicionar produtos (3-6 itens)
        num_produtos = random.randint(3, 6)
        produtos_selecionados = random.sample(produtos, min(num_produtos, len(produtos)))
        
        for produto in produtos_selecionados:
            quantidade = random.randint(1, 15)
            itens_descricao.append(produto.nome)
            itens_quantidades.append(str(quantidade))
            itens_valores.append(str(produto.preco))
            itens_unidades.append(produto.unidade)
        
        # Calcular subtotal para definir desconto em reais
        subtotal = Decimal('0.00')
        quantidades = [int(q) for q in itens_quantidades]
        valores = [Decimal(v) for v in itens_valores]
        
        for quantidade, valor in zip(quantidades, valores):
            subtotal += quantidade * valor
        
        # Definir desconto (30% dos orçamentos terão desconto)
        tem_desconto = random.choice([True, False, False])  # 33% de chance
        desconto = Decimal('0.00')
        observacao_final = f"Orçamento {i+1:03d}/2025"
        
        if tem_desconto:
            # Desconto fixo entre R$ 10 e R$ 99
            desconto = Decimal(str(random.randint(10, 99)))
            obs_desconto = random.choice(observacoes_desconto)
            observacao_final = f"Orçamento {i+1:03d}/2025 - {obs_desconto}"
        else:
            observacao_final = f"Orçamento {i+1:03d}/2025 - Pagamento em 30 dias"
        
        # Criar orçamento
        Orcamento.objects.create(
            cliente=cliente.nome,
            cnpj=getattr(cliente, 'cnpj', ''),
            endereco=cliente.endereco,
            cidade=cliente.cidade,
            uf=cliente.uf,
            telefone=cliente.telefone,
            email=cliente.email,
            descricao=' / '.join(itens_descricao),  # Separador esperado pela view
            itens_quantidades=' / '.join(itens_quantidades),
            itens_valores=' / '.join(itens_valores),
            itens_unidades=' / '.join(itens_unidades),
            observacao=observacao_final,
            desconto=desconto
        )
    
    print("Criados 15 orçamentos com itens separados!")

def criar_notificacoes():
    """Cria notificações baseadas nos produtos criados"""
    print("Criando notificações...")
    
    # Notificações de produtos próximos da validade
    produtos_validade = Produto.objects.filter(
        validade__lte=datetime.now().date() + timedelta(days=30)
    )[:8]
    
    for produto in produtos_validade:
        dias_restantes = (produto.validade - datetime.now().date()).days
        Notificacao.objects.create(
            tipo="VALIDADE",
            titulo=f"Produto próximo da validade",
            mensagem=f"{produto.nome} vence em {dias_restantes} dias",
            produto=produto
        )
    
    # Notificações de estoque crítico
    produtos_estoque_critico = Produto.objects.filter(quantidade__lte=5)[:8]
    
    for produto in produtos_estoque_critico:
        Notificacao.objects.create(
            tipo="ESTOQUE_CRITICO",
            titulo=f"Estoque crítico",
            mensagem=f"{produto.nome} - Apenas {produto.quantidade} unidades em estoque",
            produto=produto
        )
    
    # Notificações de baixa saída
    produtos_baixa_saida = Produto.objects.filter(quantidade__gte=80)[:5]
    
    for produto in produtos_baixa_saida:
        Notificacao.objects.create(
            tipo="BAIXA_SAIDA",
            titulo=f"Produto com baixa saída",
            mensagem=f"{produto.nome} - {produto.quantidade} unidades paradas no estoque",
            produto=produto
        )
    
    print("Criadas notificações!")

def main():
    """Função principal"""
    print("=== POPULANDO BANCO DE DADOS ===")
    
    limpar_banco()
    criar_fornecedores()
    criar_clientes()
    criar_servicos()
    criar_produtos()
    criar_orcamentos()
    criar_notificacoes()
    
    print("\n=== RESUMO ===")
    print(f"Fornecedores: {Fornecedor.objects.count()}")
    print(f"Clientes: {Cliente.objects.count()}")
    print(f"Serviços: {Servico.objects.count()}")
    print(f"Produtos: {Produto.objects.count()}")
    print(f"Orçamentos: {Orcamento.objects.count()}")
    
    # Mostrar alguns exemplos de orçamentos criados
    print("\n=== EXEMPLOS DE ORÇAMENTOS ===\n")
    orcamentos_exemplo = Orcamento.objects.all()[:3]
    for orc in orcamentos_exemplo:
        print(f"Cliente: {orc.cliente}")
        print(f"Desconto: R$ {orc.desconto}")
        print(f"Observação: {orc.observacao}")
        print(f"Itens: {len(orc.descricao.split(chr(10)))} itens")
        print("---")
    print(f"Notificações: {Notificacao.objects.count()}")
    print("\nBanco populado com sucesso!")

if __name__ == "__main__":
    main()