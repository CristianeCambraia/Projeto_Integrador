import os
import django
from datetime import date, timedelta
import random

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insumed_pi.settings')
django.setup()

from app.models import Fornecedor, Cliente, Produto, Servico, Orcamento, Usuario, MovimentacaoEstoque
from django.utils import timezone

def criar_fornecedores():
    fornecedores_data = [
        {'nome': 'Farmácia Central LTDA', 'cnpj': '12345678000199', 'endereco': 'Rua das Flores, 123', 'bairro': 'Centro', 'cidade': 'São Paulo', 'uf': 'SP', 'cep': '01234-567', 'telefone': '(11) 99999-1111', 'email': 'contato@farmaciacentral.com.br', 'data_nascimento': date(1990, 1, 15)},
        {'nome': 'Distribuidora MedSul', 'cnpj': '98765432000188', 'endereco': 'Av. Paulista, 456', 'bairro': 'Bela Vista', 'cidade': 'São Paulo', 'uf': 'SP', 'cep': '01310-100', 'telefone': '(11) 88888-2222', 'email': 'vendas@medsul.com.br', 'data_nascimento': date(1985, 5, 20)},
        {'nome': 'Laboratório BioVida', 'cnpj': '11122233000177', 'endereco': 'Rua da Saúde, 789', 'bairro': 'Copacabana', 'cidade': 'Rio de Janeiro', 'uf': 'RJ', 'cep': '22070-011', 'telefone': '(21) 77777-3333', 'email': 'comercial@biovida.com.br', 'data_nascimento': date(1988, 8, 10)},
        {'nome': 'Suprimentos Hospitalares', 'cnpj': '44455566000166', 'endereco': 'Rua dos Médicos, 321', 'bairro': 'Savassi', 'cidade': 'Belo Horizonte', 'uf': 'MG', 'cep': '30112-000', 'telefone': '(31) 66666-4444', 'email': 'hospital@suprimentos.com.br', 'data_nascimento': date(1992, 3, 25)},
        {'nome': 'Farmacêutica Nacional', 'cnpj': '77788899000155', 'endereco': 'Av. Brasil, 654', 'bairro': 'Asa Norte', 'cidade': 'Brasília', 'uf': 'DF', 'cep': '70040-010', 'telefone': '(61) 55555-5555', 'email': 'nacional@farmaceutica.com.br', 'data_nascimento': date(1987, 12, 5)}
    ]
    
    fornecedores = []
    for data in fornecedores_data:
        fornecedor, created = Fornecedor.objects.get_or_create(
            cnpj=data['cnpj'],
            defaults=data
        )
        fornecedores.append(fornecedor)
        if created:
            print(f"Fornecedor criado: {fornecedor.nome}")
    
    return fornecedores

def criar_clientes():
    clientes_data = [
        {'nome': 'Hospital São Lucas', 'cpf': '12345678901', 'endereco': 'Rua da Esperança, 100', 'bairro': 'Vila Madalena', 'cidade': 'São Paulo', 'uf': 'SP', 'cep': '05435-000', 'telefone': '(11) 3333-1111', 'email': 'compras@saolucas.com.br', 'data_nascimento': date(1980, 6, 15)},
        {'nome': 'Clínica Vida Nova', 'cpf': '98765432109', 'endereco': 'Av. da Saúde, 200', 'bairro': 'Ipanema', 'cidade': 'Rio de Janeiro', 'uf': 'RJ', 'cep': '22421-030', 'telefone': '(21) 3333-2222', 'email': 'clinica@vidanova.com.br', 'data_nascimento': date(1975, 9, 20)},
        {'nome': 'UBS Centro', 'cpf': '11122233344', 'endereco': 'Praça Central, 50', 'bairro': 'Centro', 'cidade': 'Belo Horizonte', 'uf': 'MG', 'cep': '30112-000', 'telefone': '(31) 3333-3333', 'email': 'ubs@centro.gov.br', 'data_nascimento': date(1985, 4, 10)},
        {'nome': 'Farmácia Popular', 'cpf': '44455566677', 'endereco': 'Rua do Comércio, 300', 'bairro': 'Pelourinho', 'cidade': 'Salvador', 'uf': 'BA', 'cep': '40026-150', 'telefone': '(71) 3333-4444', 'email': 'popular@farmacia.com.br', 'data_nascimento': date(1990, 11, 25)},
        {'nome': 'Instituto de Pesquisa Médica', 'cpf': '77788899900', 'endereco': 'Campus Universitário, 400', 'bairro': 'Barão Geraldo', 'cidade': 'Campinas', 'uf': 'SP', 'cep': '13083-970', 'telefone': '(19) 3333-5555', 'email': 'pesquisa@instituto.edu.br', 'data_nascimento': date(1982, 2, 8)},
        {'nome': 'Dr. João Silva', 'cpf': '12312312312', 'endereco': 'Rua dos Médicos, 150', 'bairro': 'Jardins', 'cidade': 'São Paulo', 'uf': 'SP', 'cep': '01401-001', 'telefone': '(11) 9999-1234', 'email': 'drjoao@clinica.com.br', 'data_nascimento': date(1978, 7, 12)},
        {'nome': 'Dra. Maria Santos', 'cpf': '32132132132', 'endereco': 'Av. das Clínicas, 250', 'bairro': 'Tijuca', 'cidade': 'Rio de Janeiro', 'uf': 'RJ', 'cep': '20511-130', 'telefone': '(21) 9999-5678', 'email': 'drmaria@hospital.com.br', 'data_nascimento': date(1983, 10, 30)}
    ]
    
    clientes = []
    for data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            cpf=data['cpf'],
            defaults=data
        )
        clientes.append(cliente)
        if created:
            print(f"Cliente criado: {cliente.nome}")
    
    return clientes

def criar_produtos(fornecedores):
    hoje = date.today()
    
    # Produtos VENCIDOS (para notificações)
    produtos_vencidos = [
        {'nome': 'Aspirina 500mg VENCIDA', 'quantidade': 15, 'unidade': 'Comprimido', 'preco': 12.50, 'preco_compra': 8.00, 'validade': hoje - timedelta(days=30), 'codigo_barras': '7891234567890'},
        {'nome': 'Dipirona 500mg VENCIDA', 'quantidade': 8, 'unidade': 'Comprimido', 'preco': 15.00, 'preco_compra': 10.00, 'validade': hoje - timedelta(days=15), 'codigo_barras': '7891234567891'},
        {'nome': 'Xarope Infantil VENCIDO', 'quantidade': 3, 'unidade': 'Frasco', 'preco': 25.00, 'preco_compra': 18.00, 'validade': hoje - timedelta(days=60), 'codigo_barras': '7891234567892'},
        {'nome': 'Vitamina C VENCIDA', 'quantidade': 20, 'unidade': 'Comprimido', 'preco': 18.00, 'preco_compra': 12.00, 'validade': hoje - timedelta(days=5), 'codigo_barras': '7891234567893'}
    ]
    
    # Produtos PRÓXIMOS DA VALIDADE (30-60 dias)
    produtos_proximos_validade = [
        {'nome': 'Paracetamol 750mg', 'quantidade': 50, 'unidade': 'Comprimido', 'preco': 8.50, 'preco_compra': 5.00, 'validade': hoje + timedelta(days=45), 'codigo_barras': '7891234567894'},
        {'nome': 'Ibuprofeno 600mg', 'quantidade': 30, 'unidade': 'Comprimido', 'preco': 22.00, 'preco_compra': 15.00, 'validade': hoje + timedelta(days=30), 'codigo_barras': '7891234567895'},
        {'nome': 'Amoxicilina 500mg', 'quantidade': 25, 'unidade': 'Cápsula', 'preco': 35.00, 'preco_compra': 25.00, 'validade': hoje + timedelta(days=50), 'codigo_barras': '7891234567896'},
        {'nome': 'Omeprazol 20mg', 'quantidade': 40, 'unidade': 'Cápsula', 'preco': 28.00, 'preco_compra': 20.00, 'validade': hoje + timedelta(days=35), 'codigo_barras': '7891234567897'}
    ]
    
    # Produtos ESTOQUE CRÍTICO (≤ 5 unidades)
    produtos_estoque_critico = [
        {'nome': 'Insulina NPH', 'quantidade': 2, 'unidade': 'Frasco', 'preco': 85.00, 'preco_compra': 60.00, 'validade': hoje + timedelta(days=180), 'codigo_barras': '7891234567898'},
        {'nome': 'Captopril 25mg', 'quantidade': 5, 'unidade': 'Comprimido', 'preco': 12.00, 'preco_compra': 8.00, 'validade': hoje + timedelta(days=365), 'codigo_barras': '7891234567899'},
        {'nome': 'Losartana 50mg', 'quantidade': 3, 'unidade': 'Comprimido', 'preco': 18.00, 'preco_compra': 12.00, 'validade': hoje + timedelta(days=300), 'codigo_barras': '7891234567800'},
        {'nome': 'Metformina 850mg', 'quantidade': 1, 'unidade': 'Comprimido', 'preco': 15.00, 'preco_compra': 10.00, 'validade': hoje + timedelta(days=400), 'codigo_barras': '7891234567801'}
    ]
    
    # Produtos SEM MOVIMENTAÇÃO (para baixa saída - data antiga)
    produtos_baixa_saida = [
        {'nome': 'Pomada Cicatrizante', 'quantidade': 25, 'unidade': 'Tubo', 'preco': 32.00, 'preco_compra': 22.00, 'validade': hoje + timedelta(days=500), 'codigo_barras': '7891234567802', 'data_antiga': True},
        {'nome': 'Colírio Lubrificante', 'quantidade': 18, 'unidade': 'Frasco', 'preco': 28.00, 'preco_compra': 20.00, 'validade': hoje + timedelta(days=450), 'codigo_barras': '7891234567803', 'data_antiga': True},
        {'nome': 'Protetor Solar FPS 60', 'quantidade': 12, 'unidade': 'Frasco', 'preco': 45.00, 'preco_compra': 30.00, 'validade': hoje + timedelta(days=600), 'codigo_barras': '7891234567804', 'data_antiga': True}
    ]
    
    # Produtos NORMAIS (estoque bom)
    produtos_normais = [
        {'nome': 'Soro Fisiológico 500ml', 'quantidade': 100, 'unidade': 'Frasco', 'preco': 8.00, 'preco_compra': 5.00, 'validade': hoje + timedelta(days=730), 'codigo_barras': '7891234567805'},
        {'nome': 'Álcool 70% 1L', 'quantidade': 80, 'unidade': 'Frasco', 'preco': 12.00, 'preco_compra': 8.00, 'validade': hoje + timedelta(days=1095), 'codigo_barras': '7891234567806'},
        {'nome': 'Gaze Estéril 10x10', 'quantidade': 200, 'unidade': 'Pacote', 'preco': 5.50, 'preco_compra': 3.00, 'validade': hoje + timedelta(days=1460), 'codigo_barras': '7891234567807'},
        {'nome': 'Luva Descartável M', 'quantidade': 150, 'unidade': 'Caixa', 'preco': 25.00, 'preco_compra': 18.00, 'validade': hoje + timedelta(days=1095), 'codigo_barras': '7891234567808'},
        {'nome': 'Termômetro Digital', 'quantidade': 35, 'unidade': 'Unidade', 'preco': 45.00, 'preco_compra': 30.00, 'validade': None, 'codigo_barras': '7891234567809'},
        {'nome': 'Estetoscópio Adulto', 'quantidade': 20, 'unidade': 'Unidade', 'preco': 120.00, 'preco_compra': 80.00, 'validade': None, 'codigo_barras': '7891234567810'},
        {'nome': 'Máscara Cirúrgica', 'quantidade': 500, 'unidade': 'Caixa', 'preco': 35.00, 'preco_compra': 25.00, 'validade': hoje + timedelta(days=1095), 'codigo_barras': '7891234567811'},
        {'nome': 'Seringa 10ml', 'quantidade': 300, 'unidade': 'Unidade', 'preco': 2.50, 'preco_compra': 1.50, 'validade': hoje + timedelta(days=1825), 'codigo_barras': '7891234567812'}
    ]
    
    todos_produtos = produtos_vencidos + produtos_proximos_validade + produtos_estoque_critico + produtos_baixa_saida + produtos_normais
    
    produtos_criados = []
    for i, produto_data in enumerate(todos_produtos):
        fornecedor = fornecedores[i % len(fornecedores)]
        
        # Data de cadastro antiga para produtos de baixa saída
        if produto_data.get('data_antiga'):
            data_cadastro = timezone.now() - timedelta(days=120)
        else:
            data_cadastro = timezone.now() - timedelta(days=random.randint(1, 30))
        
        produto, created = Produto.objects.get_or_create(
            codigo_barras=produto_data['codigo_barras'],
            defaults={
                'nome': produto_data['nome'],
                'quantidade': produto_data['quantidade'],
                'unidade': produto_data['unidade'],
                'preco': produto_data['preco'],
                'preco_compra': produto_data['preco_compra'],
                'validade': produto_data['validade'],
                'fornecedor': fornecedor,
                'data_hora': data_cadastro,
                'descricao': f"Produto médico-hospitalar - {produto_data['nome']}"
            }
        )
        
        if created:
            # Atualizar data_hora para produtos antigos
            if produto_data.get('data_antiga'):
                produto.data_hora = data_cadastro
                produto.save()
            
            produtos_criados.append(produto)
            print(f"Produto criado: {produto.nome}")
    
    return produtos_criados

def criar_servicos(fornecedores):
    servicos_data = [
        {'nome': 'Consulta Médica Domiciliar', 'preco': 150.00, 'unidade': 'Consulta', 'descricao': 'Atendimento médico no domicílio do paciente'},
        {'nome': 'Aplicação de Injeção', 'preco': 25.00, 'unidade': 'Aplicação', 'descricao': 'Aplicação de medicamentos injetáveis'},
        {'nome': 'Curativo Especializado', 'preco': 45.00, 'unidade': 'Procedimento', 'descricao': 'Realização de curativos especializados'},
        {'nome': 'Aferição de Pressão', 'preco': 15.00, 'unidade': 'Procedimento', 'descricao': 'Verificação da pressão arterial'},
        {'nome': 'Teste de Glicemia', 'preco': 20.00, 'unidade': 'Teste', 'descricao': 'Medição da glicose no sangue'},
        {'nome': 'Nebulização', 'preco': 30.00, 'unidade': 'Sessão', 'descricao': 'Tratamento respiratório com nebulizador'},
        {'nome': 'Orientação Farmacêutica', 'preco': 35.00, 'unidade': 'Consulta', 'descricao': 'Orientação sobre uso correto de medicamentos'}
    ]
    
    servicos_criados = []
    for i, servico_data in enumerate(servicos_data):
        fornecedor = fornecedores[i % len(fornecedores)]
        
        servico, created = Servico.objects.get_or_create(
            nome=servico_data['nome'],
            defaults={
                'preco': servico_data['preco'],
                'unidade': servico_data['unidade'],
                'descricao': servico_data['descricao'],
                'fornecedor': fornecedor
            }
        )
        
        if created:
            servicos_criados.append(servico)
            print(f"Serviço criado: {servico.nome}")
    
    return servicos_criados

def criar_orcamentos(clientes):
    hoje = date.today()
    
    orcamentos_data = [
        {
            'cliente': 'Hospital São Lucas',
            'cnpj': '12345678000199',
            'endereco': 'Rua da Esperança, 100',
            'cidade': 'São Paulo',
            'uf': 'SP',
            'telefone': '(11) 3333-1111',
            'email': 'compras@saolucas.com.br',
            'itens_unidades': 'Caixa / Frasco / Unidade',
            'descricao': 'Luva Descartável M / Álcool 70% 1L / Termômetro Digital',
            'itens_quantidades': '10 / 20 / 5',
            'itens_valores': '25,00 / 12,00 / 45,00',
            'observacao': 'Entrega urgente - Hospital',
            'desconto': 5.0,
            'data': hoje - timedelta(days=2)
        },
        {
            'cliente': 'Clínica Vida Nova',
            'cnpj': '98765432000188',
            'endereco': 'Av. da Saúde, 200',
            'cidade': 'Rio de Janeiro',
            'uf': 'RJ',
            'telefone': '(21) 3333-2222',
            'email': 'clinica@vidanova.com.br',
            'itens_unidades': 'Comprimido / Frasco / Pacote',
            'descricao': 'Paracetamol 750mg / Soro Fisiológico 500ml / Gaze Estéril 10x10',
            'itens_quantidades': '100 / 50 / 20',
            'itens_valores': '8,50 / 8,00 / 5,50',
            'observacao': 'Pagamento à vista - desconto aplicado',
            'desconto': 10.0,
            'data': hoje - timedelta(days=5)
        },
        {
            'cliente': 'Dr. João Silva',
            'cnpj': '12312312000112',
            'endereco': 'Rua dos Médicos, 150',
            'cidade': 'São Paulo',
            'uf': 'SP',
            'telefone': '(11) 9999-1234',
            'email': 'drjoao@clinica.com.br',
            'itens_unidades': 'Unidade / Caixa / Frasco',
            'descricao': 'Estetoscópio Adulto / Máscara Cirúrgica / Colírio Lubrificante',
            'itens_quantidades': '2 / 5 / 10',
            'itens_valores': '120,00 / 35,00 / 28,00',
            'observacao': 'Consultório particular',
            'desconto': 0.0,
            'data': hoje - timedelta(days=1)
        },
        {
            'cliente': 'UBS Centro',
            'cnpj': '11122233000144',
            'endereco': 'Praça Central, 50',
            'cidade': 'Belo Horizonte',
            'uf': 'MG',
            'telefone': '(31) 3333-3333',
            'email': 'ubs@centro.gov.br',
            'itens_unidades': 'Unidade / Frasco / Comprimido',
            'descricao': 'Seringa 10ml / Insulina NPH / Captopril 25mg',
            'itens_quantidades': '200 / 10 / 500',
            'itens_valores': '2,50 / 85,00 / 12,00',
            'observacao': 'Licitação pública - prazo 30 dias',
            'desconto': 15.0,
            'data': hoje - timedelta(days=7)
        },
        {
            'cliente': 'Farmácia Popular',
            'cnpj': '44455566000177',
            'endereco': 'Rua do Comércio, 300',
            'cidade': 'Salvador',
            'uf': 'BA',
            'telefone': '(71) 3333-4444',
            'email': 'popular@farmacia.com.br',
            'itens_unidades': 'Comprimido / Cápsula / Frasco',
            'descricao': 'Ibuprofeno 600mg / Amoxicilina 500mg / Protetor Solar FPS 60',
            'itens_quantidades': '50 / 30 / 15',
            'itens_valores': '22,00 / 35,00 / 45,00',
            'observacao': 'Revenda autorizada',
            'desconto': 8.0,
            'data': hoje
        }
    ]
    
    orcamentos_criados = []
    for orcamento_data in orcamentos_data:
        orcamento, created = Orcamento.objects.get_or_create(
            cliente=orcamento_data['cliente'],
            data=orcamento_data['data'],
            defaults=orcamento_data
        )
        
        if created:
            orcamentos_criados.append(orcamento)
            print(f"Orçamento criado: {orcamento.cliente} - {orcamento.data}")
    
    return orcamentos_criados

def criar_usuarios():
    usuarios_data = [
        {'nome': 'Ana Silva', 'email': 'ana@insumed.com', 'senha': '123456', 'cpf': '11111111111', 'endereco': 'Rua A, 100', 'telefone': '(11) 99999-0001', 'data_nascimento': date(1990, 1, 15)},
        {'nome': 'Carlos Santos', 'email': 'carlos@insumed.com', 'senha': '123456', 'cpf': '22222222222', 'endereco': 'Rua B, 200', 'telefone': '(11) 99999-0002', 'data_nascimento': date(1985, 5, 20)},
        {'nome': 'Fernanda Costa', 'email': 'fernanda@insumed.com', 'senha': '123456', 'cpf': '33333333333', 'endereco': 'Rua C, 300', 'telefone': '(11) 99999-0003', 'data_nascimento': date(1988, 8, 10)},
        {'nome': 'Roberto Lima', 'email': 'roberto@insumed.com', 'senha': '123456', 'cpf': '44444444444', 'endereco': 'Rua D, 400', 'telefone': '(11) 99999-0004', 'data_nascimento': date(1992, 3, 25)},
        {'nome': 'Juliana Oliveira', 'email': 'juliana@insumed.com', 'senha': '123456', 'cpf': '55555555555', 'endereco': 'Rua E, 500', 'telefone': '(11) 99999-0005', 'data_nascimento': date(1987, 12, 5)}
    ]
    
    usuarios_criados = []
    for usuario_data in usuarios_data:
        usuario, created = Usuario.objects.get_or_create(
            email=usuario_data['email'],
            defaults=usuario_data
        )
        
        if created:
            usuarios_criados.append(usuario)
            print(f"Usuário criado: {usuario.nome}")
    
    return usuarios_criados

def criar_movimentacoes(produtos):
    # Criar algumas movimentações de entrada e saída para produtos
    movimentacoes_criadas = []
    
    for produto in produtos[:10]:  # Apenas para os primeiros 10 produtos
        # Movimentação de entrada
        entrada = MovimentacaoEstoque.objects.create(
            produto=produto,
            tipo='ENTRADA',
            quantidade=random.randint(10, 50),
            data_hora=timezone.now() - timedelta(days=random.randint(5, 30))
        )
        movimentacoes_criadas.append(entrada)
        
        # Movimentação de saída (se não for produto de baixa saída)
        if 'VENCID' not in produto.nome.upper() and 'Pomada' not in produto.nome and 'Colírio' not in produto.nome and 'Protetor' not in produto.nome:
            saida = MovimentacaoEstoque.objects.create(
                produto=produto,
                tipo='SAIDA',
                quantidade=random.randint(1, 10),
                data_hora=timezone.now() - timedelta(days=random.randint(1, 15))
            )
            movimentacoes_criadas.append(saida)
    
    print(f"Criadas {len(movimentacoes_criadas)} movimentações de estoque")
    return movimentacoes_criadas

def main():
    print("=== POPULANDO BANCO DE DADOS ===")
    
    print("\n1. Criando fornecedores...")
    fornecedores = criar_fornecedores()
    
    print("\n2. Criando clientes...")
    clientes = criar_clientes()
    
    print("\n3. Criando produtos...")
    produtos = criar_produtos(fornecedores)
    
    print("\n4. Criando serviços...")
    servicos = criar_servicos(fornecedores)
    
    print("\n5. Criando orçamentos...")
    orcamentos = criar_orcamentos(clientes)
    
    print("\n6. Criando usuários...")
    usuarios = criar_usuarios()
    
    print("\n7. Criando movimentações de estoque...")
    movimentacoes = criar_movimentacoes(produtos)
    
    print("\n=== RESUMO ===")
    print(f"Fornecedores: {len(fornecedores)}")
    print(f"Clientes: {len(clientes)}")
    print(f"Produtos: {len(produtos)}")
    print(f"Serviços: {len(servicos)}")
    print(f"Orçamentos: {len(orcamentos)}")
    print(f"Usuários: {len(usuarios)}")
    print(f"Movimentações: {len(movimentacoes)}")
    
    print("\n=== PRODUTOS PARA NOTIFICAÇÕES ===")
    print("[OK] Produtos vencidos: 4 produtos")
    print("[OK] Produtos próximos da validade: 4 produtos")
    print("[OK] Produtos com estoque crítico: 4 produtos")
    print("[OK] Produtos com baixa saída: 3 produtos")
    print("[OK] Produtos normais: 8 produtos")
    
    print("\n*** BANCO POPULADO COM SUCESSO! ***")

if __name__ == "__main__":
    main()