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

from app.models import Fornecedor, Cliente, Produto, Servico, Orcamento, ItemOrcamento, Notificacao

def limpar_banco():
    """Limpa todos os dados do banco"""
    print("Limpando banco de dados...")
    Notificacao.objects.all().delete()
    ItemOrcamento.objects.all().delete()
    Orcamento.objects.all().delete()
    Produto.objects.all().delete()
    Servico.objects.all().delete()
    Cliente.objects.all().delete()
    Fornecedor.objects.all().delete()
    print("Banco limpo!")

def criar_fornecedores():
    """Cria 20 fornecedores da área da saúde"""
    print("Criando fornecedores...")
    fornecedores_data = [
        {"nome": "MedSupply Ltda", "cnpj": "12.345.678/0001-90", "telefone": "(11) 3456-7890", "email": "contato@medsupply.com.br", "endereco": "Rua das Medicinas, 123 - São Paulo - SP"},
        {"nome": "Hospitalar Distribuidora", "cnpj": "23.456.789/0001-01", "telefone": "(21) 2345-6789", "email": "vendas@hospitalar.com.br", "endereco": "Av. Saúde, 456 - Rio de Janeiro - RJ"},
        {"nome": "Cirúrgica Premium", "cnpj": "34.567.890/0001-12", "telefone": "(31) 3567-8901", "email": "comercial@cirurgica.com.br", "endereco": "Rua Bisturi, 789 - Belo Horizonte - MG"},
        {"nome": "Farmacêutica Central", "cnpj": "45.678.901/0001-23", "telefone": "(41) 4678-9012", "email": "pedidos@farmaceutica.com.br", "endereco": "Av. Remédios, 321 - Curitiba - PR"},
        {"nome": "Equipamentos Médicos Sul", "cnpj": "56.789.012/0001-34", "telefone": "(51) 5789-0123", "email": "atendimento@equipmed.com.br", "endereco": "Rua Aparelhos, 654 - Porto Alegre - RS"},
        {"nome": "Laboratorial Express", "cnpj": "67.890.123/0001-45", "telefone": "(61) 6890-1234", "email": "lab@express.com.br", "endereco": "Quadra Lab, 987 - Brasília - DF"},
        {"nome": "Dental Care Suprimentos", "cnpj": "78.901.234/0001-56", "telefone": "(85) 7901-2345", "email": "dental@care.com.br", "endereco": "Rua Dentes, 147 - Fortaleza - CE"},
        {"nome": "Ortopédica Nacional", "cnpj": "89.012.345/0001-67", "telefone": "(71) 8012-3456", "email": "ortopedia@nacional.com.br", "endereco": "Av. Ossos, 258 - Salvador - BA"},
        {"nome": "Radiologia Imports", "cnpj": "90.123.456/0001-78", "telefone": "(81) 9123-4567", "email": "radio@imports.com.br", "endereco": "Rua Raio-X, 369 - Recife - PE"},
        {"nome": "Anestesia & Cia", "cnpj": "01.234.567/0001-89", "telefone": "(62) 0234-5678", "email": "anestesia@cia.com.br", "endereco": "Av. Sedação, 741 - Goiânia - GO"},
        {"nome": "Cardiologia Especializada", "cnpj": "12.345.679/0001-90", "telefone": "(27) 1345-6790", "email": "cardio@especializada.com.br", "endereco": "Rua Coração, 852 - Vitória - ES"},
        {"nome": "Neurologia Avançada", "cnpj": "23.456.780/0001-01", "telefone": "(65) 2456-7801", "email": "neuro@avancada.com.br", "endereco": "Av. Cérebro, 963 - Cuiabá - MT"},
        {"nome": "Pediatria Total", "cnpj": "34.567.891/0001-12", "telefone": "(84) 3567-8912", "email": "pediatria@total.com.br", "endereco": "Rua Criança, 174 - Natal - RN"},
        {"nome": "Ginecologia Moderna", "cnpj": "45.678.902/0001-23", "telefone": "(83) 4678-9023", "email": "gineco@moderna.com.br", "endereco": "Av. Mulher, 285 - João Pessoa - PB"},
        {"nome": "Oncologia Esperança", "cnpj": "56.789.013/0001-34", "telefone": "(82) 5789-0134", "email": "onco@esperanca.com.br", "endereco": "Rua Cura, 396 - Maceió - AL"},
        {"nome": "Dermatologia Bella", "cnpj": "67.890.124/0001-45", "telefone": "(79) 6890-1245", "email": "derma@bella.com.br", "endereco": "Av. Pele, 407 - Aracaju - SE"},
        {"nome": "Oftalmologia Visão", "cnpj": "78.901.235/0001-56", "telefone": "(68) 7901-2356", "email": "oftalmo@visao.com.br", "endereco": "Rua Olhos, 518 - Rio Branco - AC"},
        {"nome": "Urologia Masculina", "cnpj": "89.012.346/0001-67", "telefone": "(96) 8012-3467", "email": "uro@masculina.com.br", "endereco": "Av. Homem, 629 - Macapá - AP"},
        {"nome": "Psiquiatria Mental", "cnpj": "90.123.457/0001-78", "telefone": "(95) 9123-4578", "email": "psiq@mental.com.br", "endereco": "Rua Mente, 730 - Boa Vista - RR"},
        {"nome": "Emergência Rápida", "cnpj": "01.234.568/0001-89", "telefone": "(63) 0234-5689", "email": "emergencia@rapida.com.br", "endereco": "Av. Socorro, 841 - Palmas - TO"}
    ]
    
    for data in fornecedores_data:
        Fornecedor.objects.create(**data)
    print(f"Criados {len(fornecedores_data)} fornecedores!")

def criar_clientes():
    """Cria 30 clientes da área da saúde"""
    print("Criando clientes...")
    clientes_data = [
        {"nome": "Hospital São Lucas", "cnpj": "11.111.111/0001-11", "telefone": "(11) 1111-1111", "email": "compras@saolucas.com.br", "endereco": "Rua Hospital, 100 - São Paulo - SP"},
        {"nome": "Clínica Vida Nova", "cnpj": "22.222.222/0001-22", "telefone": "(21) 2222-2222", "email": "suprimentos@vidanova.com.br", "endereco": "Av. Saúde, 200 - Rio de Janeiro - RJ"},
        {"nome": "Centro Médico Esperança", "cnpj": "33.333.333/0001-33", "telefone": "(31) 3333-3333", "email": "compras@esperanca.com.br", "endereco": "Rua Cura, 300 - Belo Horizonte - MG"},
        {"nome": "Hospital Municipal Central", "cnpj": "44.444.444/0001-44", "telefone": "(41) 4444-4444", "email": "almoxarifado@municipal.gov.br", "endereco": "Av. Central, 400 - Curitiba - PR"},
        {"nome": "Clínica Especializada Norte", "cnpj": "55.555.555/0001-55", "telefone": "(51) 5555-5555", "email": "materiais@norte.com.br", "endereco": "Rua Norte, 500 - Porto Alegre - RS"},
        {"nome": "Hospital Universitário", "cnpj": "66.666.666/0001-66", "telefone": "(61) 6666-6666", "email": "compras@universitario.edu.br", "endereco": "Campus Saúde, 600 - Brasília - DF"},
        {"nome": "Clínica Odontológica Sorriso", "cnpj": "77.777.777/0001-77", "telefone": "(85) 7777-7777", "email": "dental@sorriso.com.br", "endereco": "Rua Sorriso, 700 - Fortaleza - CE"},
        {"nome": "Centro de Reabilitação Vida", "cnpj": "88.888.888/0001-88", "telefone": "(71) 8888-8888", "email": "fisio@vida.com.br", "endereco": "Av. Reabilitação, 800 - Salvador - BA"},
        {"nome": "Laboratório Diagnóstico Plus", "cnpj": "99.999.999/0001-99", "telefone": "(81) 9999-9999", "email": "lab@diagnostico.com.br", "endereco": "Rua Exames, 900 - Recife - PE"},
        {"nome": "Clínica Cardiológica Coração", "cnpj": "10.101.010/0001-10", "telefone": "(62) 1010-1010", "email": "cardio@coracao.com.br", "endereco": "Av. Coração, 1000 - Goiânia - GO"},
        {"nome": "Hospital Materno Infantil", "cnpj": "20.202.020/0001-20", "telefone": "(27) 2020-2020", "email": "maternoinfantil@hospital.com.br", "endereco": "Rua Mãe e Filho, 1100 - Vitória - ES"},
        {"nome": "Centro Oncológico Esperança", "cnpj": "30.303.030/0001-30", "telefone": "(65) 3030-3030", "email": "onco@esperanca.com.br", "endereco": "Av. Esperança, 1200 - Cuiabá - MT"},
        {"nome": "Clínica Neurológica Mente", "cnpj": "40.404.040/0001-40", "telefone": "(84) 4040-4040", "email": "neuro@mente.com.br", "endereco": "Rua Neurônio, 1300 - Natal - RN"},
        {"nome": "Hospital Geral do Estado", "cnpj": "50.505.050/0001-50", "telefone": "(83) 5050-5050", "email": "compras@hge.gov.br", "endereco": "Av. Estado, 1400 - João Pessoa - PB"},
        {"nome": "Clínica Dermatológica Pele", "cnpj": "60.606.060/0001-60", "telefone": "(82) 6060-6060", "email": "derma@pele.com.br", "endereco": "Rua Pele Saudável, 1500 - Maceió - AL"},
        {"nome": "Centro Oftalmológico Visão", "cnpj": "70.707.070/0001-70", "telefone": "(79) 7070-7070", "email": "oftalmo@visao.com.br", "endereco": "Av. Boa Vista, 1600 - Aracaju - SE"},
        {"nome": "Hospital de Emergência 24h", "cnpj": "80.808.080/0001-80", "telefone": "(68) 8080-8080", "email": "emergencia@24h.com.br", "endereco": "Rua Socorro, 1700 - Rio Branco - AC"},
        {"nome": "Clínica Urológica Masculina", "cnpj": "90.909.090/0001-90", "telefone": "(96) 9090-9090", "email": "uro@masculina.com.br", "endereco": "Av. Saúde Masculina, 1800 - Macapá - AP"},
        {"nome": "Centro Psiquiátrico Mente Sã", "cnpj": "11.121.212/0001-11", "telefone": "(95) 1212-1212", "email": "psiq@mentesa.com.br", "endereco": "Rua Equilíbrio, 1900 - Boa Vista - RR"},
        {"nome": "Hospital Pediátrico Criança", "cnpj": "22.232.323/0001-22", "telefone": "(63) 2323-2323", "email": "pediatria@crianca.com.br", "endereco": "Av. Infância, 2000 - Palmas - TO"},
        {"nome": "Clínica Ginecológica Mulher", "cnpj": "33.343.434/0001-33", "telefone": "(47) 3434-3434", "email": "gineco@mulher.com.br", "endereco": "Rua Feminina, 2100 - Joinville - SC"},
        {"nome": "Centro Cirúrgico Avançado", "cnpj": "44.454.545/0001-44", "telefone": "(48) 4545-4545", "email": "cirurgia@avancado.com.br", "endereco": "Av. Cirurgia, 2200 - Florianópolis - SC"},
        {"nome": "Hospital Ortopédico Ossos", "cnpj": "55.565.656/0001-55", "telefone": "(49) 5656-5656", "email": "ortopedia@ossos.com.br", "endereco": "Rua Esqueleto, 2300 - Chapecó - SC"},
        {"nome": "Clínica Radiológica Imagem", "cnpj": "66.676.767/0001-66", "telefone": "(54) 6767-6767", "email": "radio@imagem.com.br", "endereco": "Av. Raio-X, 2400 - Caxias do Sul - RS"},
        {"nome": "Centro de Anestesia Sono", "cnpj": "77.787.878/0001-77", "telefone": "(53) 7878-7878", "email": "anestesia@sono.com.br", "endereco": "Rua Sedação, 2500 - Pelotas - RS"},
        {"nome": "Hospital Geriátrico Idoso", "cnpj": "88.898.989/0001-88", "telefone": "(55) 8989-8989", "email": "geriatria@idoso.com.br", "endereco": "Av. Terceira Idade, 2600 - Santa Maria - RS"},
        {"nome": "Clínica de Fisioterapia Movimento", "cnpj": "99.909.090/0001-99", "telefone": "(16) 9090-9191", "email": "fisio@movimento.com.br", "endereco": "Rua Reabilitação, 2700 - Ribeirão Preto - SP"},
        {"nome": "Centro de Hemodiálise Rim", "cnpj": "10.111.213/0001-10", "telefone": "(17) 1213-1415", "email": "hemodialise@rim.com.br", "endereco": "Av. Nefrologia, 2800 - São José do Rio Preto - SP"},
        {"nome": "Hospital de Queimados Pele Nova", "cnpj": "20.212.324/0001-20", "telefone": "(18) 2324-2526", "email": "queimados@pelenova.com.br", "endereco": "Rua Recuperação, 2900 - Presidente Prudente - SP"},
        {"nome": "Clínica de Transplantes Vida Nova", "cnpj": "30.313.435/0001-30", "telefone": "(19) 3435-3637", "email": "transplantes@vidanova.com.br", "endereco": "Av. Doação, 3000 - Campinas - SP"}
    ]
    
    for data in clientes_data:
        Cliente.objects.create(**data)
    print(f"Criados {len(clientes_data)} clientes!")

def criar_servicos():
    """Cria 10 serviços da área da saúde"""
    print("Criando serviços...")
    servicos_data = [
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
    
    for data in servicos_data:
        Servico.objects.create(**data)
    print(f"Criados {len(servicos_data)} serviços!")

def criar_produtos():
    """Cria 150 produtos da área da saúde com diferentes situações de estoque e validade"""
    print("Criando produtos...")
    
    # Produtos com validade próxima (8 produtos)
    produtos_validade_proxima = [
        {"nome": "Soro Fisiológico 500ml", "codigo": "SF500", "preco": Decimal("3.50"), "quantidade_estoque": 45, "data_validade": datetime.now().date() + timedelta(days=15), "fornecedor_id": 1},
        {"nome": "Dipirona 500mg", "codigo": "DIP500", "preco": Decimal("12.80"), "quantidade_estoque": 28, "data_validade": datetime.now().date() + timedelta(days=20), "fornecedor_id": 2},
        {"nome": "Paracetamol 750mg", "codigo": "PAR750", "preco": Decimal("8.90"), "quantidade_estoque": 35, "data_validade": datetime.now().date() + timedelta(days=18), "fornecedor_id": 3},
        {"nome": "Omeprazol 20mg", "codigo": "OME20", "preco": Decimal("15.60"), "quantidade_estoque": 22, "data_validade": datetime.now().date() + timedelta(days=25), "fornecedor_id": 4},
        {"nome": "Amoxicilina 500mg", "codigo": "AMO500", "preco": Decimal("18.40"), "quantidade_estoque": 18, "data_validade": datetime.now().date() + timedelta(days=12), "fornecedor_id": 5},
        {"nome": "Ibuprofeno 600mg", "codigo": "IBU600", "preco": Decimal("11.20"), "quantidade_estoque": 31, "data_validade": datetime.now().date() + timedelta(days=22), "fornecedor_id": 6},
        {"nome": "Captopril 25mg", "codigo": "CAP25", "preco": Decimal("9.75"), "quantidade_estoque": 26, "data_validade": datetime.now().date() + timedelta(days=16), "fornecedor_id": 7},
        {"nome": "Losartana 50mg", "codigo": "LOS50", "preco": Decimal("13.90"), "quantidade_estoque": 29, "data_validade": datetime.now().date() + timedelta(days=19), "fornecedor_id": 8}
    ]
    
    # Produtos com estoque crítico (8 produtos)
    produtos_estoque_critico = [
        {"nome": "Luvas Cirúrgicas Estéreis", "codigo": "LCE001", "preco": Decimal("45.00"), "quantidade_estoque": 3, "data_validade": datetime.now().date() + timedelta(days=180), "fornecedor_id": 9},
        {"nome": "Máscara N95", "codigo": "MN95", "preco": Decimal("8.50"), "quantidade_estoque": 2, "data_validade": datetime.now().date() + timedelta(days=365), "fornecedor_id": 10},
        {"nome": "Seringa 10ml Descartável", "codigo": "SER10", "preco": Decimal("1.20"), "quantidade_estoque": 4, "data_validade": datetime.now().date() + timedelta(days=720), "fornecedor_id": 11},
        {"nome": "Cateter Venoso Central", "codigo": "CVC001", "preco": Decimal("85.00"), "quantidade_estoque": 1, "data_validade": datetime.now().date() + timedelta(days=540), "fornecedor_id": 12},
        {"nome": "Fio de Sutura Absorvível", "codigo": "FSA001", "preco": Decimal("25.80"), "quantidade_estoque": 3, "data_validade": datetime.now().date() + timedelta(days=450), "fornecedor_id": 13},
        {"nome": "Eletrodo Descartável", "codigo": "ELE001", "preco": Decimal("2.40"), "quantidade_estoque": 2, "data_validade": datetime.now().date() + timedelta(days=300), "fornecedor_id": 14},
        {"nome": "Sonda Nasogástrica", "codigo": "SNG001", "preco": Decimal("12.60"), "quantidade_estoque": 4, "data_validade": datetime.now().date() + timedelta(days=600), "fornecedor_id": 15},
        {"nome": "Compressa Estéril", "codigo": "CE001", "preco": Decimal("3.80"), "quantidade_estoque": 1, "data_validade": datetime.now().date() + timedelta(days=240), "fornecedor_id": 16}
    ]
    
    # Produtos com baixa saída (5 produtos)
    produtos_baixa_saida = [
        {"nome": "Equipamento Raio-X Portátil", "codigo": "RXP001", "preco": Decimal("15000.00"), "quantidade_estoque": 150, "data_validade": datetime.now().date() + timedelta(days=1800), "fornecedor_id": 17},
        {"nome": "Monitor Multiparâmetros", "codigo": "MMP001", "preco": Decimal("8500.00"), "quantidade_estoque": 85, "data_validade": datetime.now().date() + timedelta(days=1500), "fornecedor_id": 18},
        {"nome": "Desfibrilador Automático", "codigo": "DEF001", "preco": Decimal("12000.00"), "quantidade_estoque": 120, "data_validade": datetime.now().date() + timedelta(days=2000), "fornecedor_id": 19},
        {"nome": "Ventilador Pulmonar", "codigo": "VP001", "preco": Decimal("25000.00"), "quantidade_estoque": 95, "data_validade": datetime.now().date() + timedelta(days=1650), "fornecedor_id": 20},
        {"nome": "Bomba de Infusão", "codigo": "BI001", "preco": Decimal("3500.00"), "quantidade_estoque": 200, "data_validade": datetime.now().date() + timedelta(days=1200), "fornecedor_id": 1}
    ]
    
    # Produtos normais (129 produtos restantes)
    produtos_normais = []
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
        "Heparina", "Insulina NPH", "Insulina Regular", "Adrenalina", "Atropina", "Morfina",
        "Tramadol", "Fentanil", "Midazolam", "Propofol", "Succinilcolina", "Rocurônio",
        "Cefalexina", "Ciprofloxacino", "Azitromicina", "Clindamicina", "Vancomicina", "Ceftriaxona",
        "Dexametasona", "Prednisolona", "Hidrocortisona", "Furosemida", "Espironolactona",
        "Atenolol", "Propranolol", "Anlodipino", "Enalapril", "Sinvastatina", "Atorvastatina",
        "Metformina", "Glibenclamida", "Levotiroxina", "Carbonato de Cálcio", "Sulfato Ferroso",
        "Ácido Fólico", "Vitamina B12", "Vitamina D", "Complexo B", "Vitamina C",
        "Ranitidina", "Domperidona", "Bromoprida", "Simeticona", "Lactulose", "Óleo Mineral",
        "Diclofenaco", "Cetoprofeno", "Meloxicam", "Nimesulida", "Aspirina", "Clopidogrel",
        "Loratadina", "Cetirizina", "Dexclorfeniramina", "Prometazina", "Salbutamol", "Budesonida",
        "Fluticasona", "Montelucaste", "Teofilina", "Aminofilina", "Digoxina", "Amiodarona",
        "Carvedilol", "Metoprolol", "Verapamil", "Diltiazem", "Isossorbida", "Nitroglicerina",
        "Haloperidol", "Risperidona", "Quetiapina", "Olanzapina", "Clozapina", "Fluoxetina",
        "Sertralina", "Paroxetina", "Venlafaxina", "Amitriptilina", "Clomipramina", "Carbamazepina",
        "Fenitoína", "Ácido Valproico", "Lamotrigina", "Topiramato", "Gabapentina", "Pregabalina",
        "Clonazepam", "Diazepam", "Lorazepam", "Alprazolam", "Zolpidem", "Melatonina"
    ]
    
    for i, nome in enumerate(nomes_produtos[:129]):
        produto = {
            "nome": nome,
            "codigo": f"PROD{i+22:03d}",
            "preco": Decimal(str(round(random.uniform(5.0, 500.0), 2))),
            "quantidade_estoque": random.randint(20, 200),
            "data_validade": datetime.now().date() + timedelta(days=random.randint(90, 1095)),
            "fornecedor_id": random.randint(1, 20)
        }
        produtos_normais.append(produto)
    
    # Criar todos os produtos
    todos_produtos = produtos_validade_proxima + produtos_estoque_critico + produtos_baixa_saida + produtos_normais
    
    for data in todos_produtos:
        Produto.objects.create(**data)
    
    print(f"Criados {len(todos_produtos)} produtos!")

def criar_orcamentos():
    """Cria alguns orçamentos de exemplo"""
    print("Criando orçamentos...")
    
    clientes = list(Cliente.objects.all()[:10])
    servicos = list(Servico.objects.all())
    produtos = list(Produto.objects.all()[:20])
    
    for i in range(15):
        cliente = random.choice(clientes)
        orcamento = Orcamento.objects.create(
            cliente=cliente,
            data_orcamento=datetime.now().date() - timedelta(days=random.randint(0, 60)),
            observacoes=f"Orçamento {i+1} para {cliente.nome}",
            subtotal=Decimal("0.00"),
            desconto=Decimal("0.00"),
            valor_total=Decimal("0.00")
        )
        
        # Adicionar alguns itens ao orçamento
        total = Decimal("0.00")
        
        # Adicionar serviços
        for _ in range(random.randint(1, 3)):
            servico = random.choice(servicos)
            quantidade = random.randint(1, 5)
            valor_unitario = servico.preco
            valor_total_item = valor_unitario * quantidade
            
            ItemOrcamento.objects.create(
                orcamento=orcamento,
                servico=servico,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total_item
            )
            total += valor_total_item
        
        # Adicionar produtos
        for _ in range(random.randint(2, 5)):
            produto = random.choice(produtos)
            quantidade = random.randint(1, 10)
            valor_unitario = produto.preco
            valor_total_item = valor_unitario * quantidade
            
            ItemOrcamento.objects.create(
                orcamento=orcamento,
                produto=produto,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total_item
            )
            total += valor_total_item
        
        # Atualizar totais do orçamento
        desconto = total * Decimal("0.05") if random.choice([True, False]) else Decimal("0.00")
        orcamento.subtotal = total
        orcamento.desconto = desconto
        orcamento.valor_total = total - desconto
        orcamento.save()
    
    print("Criados 15 orçamentos!")

def criar_notificacoes():
    """Cria notificações baseadas nos produtos criados"""
    print("Criando notificações...")
    
    # Notificações de produtos próximos da validade
    produtos_validade = Produto.objects.filter(
        data_validade__lte=datetime.now().date() + timedelta(days=30)
    )[:8]
    
    for produto in produtos_validade:
        dias_restantes = (produto.data_validade - datetime.now().date()).days
        Notificacao.objects.create(
            tipo="validade",
            titulo=f"Produto próximo da validade",
            mensagem=f"{produto.nome} vence em {dias_restantes} dias",
            produto=produto
        )
    
    # Notificações de estoque crítico
    produtos_estoque_critico = Produto.objects.filter(quantidade_estoque__lte=5)[:8]
    
    for produto in produtos_estoque_critico:
        Notificacao.objects.create(
            tipo="estoque_critico",
            titulo=f"Estoque crítico",
            mensagem=f"{produto.nome} - Apenas {produto.quantidade_estoque} unidades em estoque",
            produto=produto
        )
    
    # Notificações de baixa saída (produtos com muito estoque)
    produtos_baixa_saida = Produto.objects.filter(quantidade_estoque__gte=80)[:5]
    
    for produto in produtos_baixa_saida:
        Notificacao.objects.create(
            tipo="baixa_saida",
            titulo=f"Produto com baixa saída",
            mensagem=f"{produto.nome} - {produto.quantidade_estoque} unidades paradas no estoque",
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
    print(f"Itens de Orçamento: {ItemOrcamento.objects.count()}")
    print(f"Notificações: {Notificacao.objects.count()}")
    print("\nBanco populado com sucesso!")

if __name__ == "__main__":
    main()