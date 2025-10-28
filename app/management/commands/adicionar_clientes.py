from django.core.management.base import BaseCommand
from app.models import Cliente
from datetime import date

class Command(BaseCommand):
    help = 'Adiciona clientes de teste'

    def handle(self, *args, **options):
        clientes_teste = [
            {
                'nome': 'Ana Silva Santos',
                'cpf': '123.456.789-01',
                'endereco': 'Rua das Flores, 123',
                'bairro': 'Centro',
                'complemento': 'Apt 101',
                'data_nascimento': date(1985, 3, 15),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01234-567',
                'email': 'ana.silva@email.com',
                'telefone': '(11) 98765-4321'
            },
            {
                'nome': 'Carlos Eduardo Oliveira',
                'cpf': '234.567.890-12',
                'endereco': 'Av. Paulista, 456',
                'bairro': 'Bela Vista',
                'complemento': 'Sala 205',
                'data_nascimento': date(1978, 7, 22),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01310-100',
                'email': 'carlos.oliveira@email.com',
                'telefone': '(11) 97654-3210'
            },
            {
                'nome': 'Maria José Ferreira',
                'cpf': '345.678.901-23',
                'endereco': 'Rua Augusta, 789',
                'bairro': 'Consolação',
                'complemento': '',
                'data_nascimento': date(1992, 11, 8),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01305-000',
                'email': 'maria.ferreira@email.com',
                'telefone': '(11) 96543-2109'
            },
            {
                'nome': 'João Pedro Costa',
                'cpf': '456.789.012-34',
                'endereco': 'Rua Oscar Freire, 321',
                'bairro': 'Jardins',
                'complemento': 'Casa 2',
                'data_nascimento': date(1980, 5, 30),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01426-001',
                'email': 'joao.costa@email.com',
                'telefone': '(11) 95432-1098'
            },
            {
                'nome': 'Fernanda Lima Souza',
                'cpf': '567.890.123-45',
                'endereco': 'Rua Haddock Lobo, 654',
                'bairro': 'Cerqueira César',
                'complemento': 'Bloco A',
                'data_nascimento': date(1987, 9, 12),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01414-001',
                'email': 'fernanda.souza@email.com',
                'telefone': '(11) 94321-0987'
            },
            {
                'nome': 'Roberto Almeida Santos',
                'cpf': '678.901.234-56',
                'endereco': 'Av. Faria Lima, 987',
                'bairro': 'Itaim Bibi',
                'complemento': 'Conj. 1501',
                'data_nascimento': date(1975, 12, 3),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '04538-132',
                'email': 'roberto.santos@email.com',
                'telefone': '(11) 93210-9876'
            },
            {
                'nome': 'Juliana Rodrigues Silva',
                'cpf': '789.012.345-67',
                'endereco': 'Rua Pamplona, 147',
                'bairro': 'Jardim Paulista',
                'complemento': 'Apt 802',
                'data_nascimento': date(1990, 4, 18),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01405-001',
                'email': 'juliana.silva@email.com',
                'telefone': '(11) 92109-8765'
            },
            {
                'nome': 'Marcos Vinícius Pereira',
                'cpf': '890.123.456-78',
                'endereco': 'Rua Estados Unidos, 258',
                'bairro': 'Jardins',
                'complemento': '',
                'data_nascimento': date(1983, 8, 25),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '01427-001',
                'email': 'marcos.pereira@email.com',
                'telefone': '(11) 91098-7654'
            },
            {
                'nome': 'Patrícia Mendes Oliveira',
                'cpf': '901.234.567-89',
                'endereco': 'Av. Rebouças, 369',
                'bairro': 'Pinheiros',
                'complemento': 'Torre B',
                'data_nascimento': date(1988, 1, 14),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '05402-000',
                'email': 'patricia.oliveira@email.com',
                'telefone': '(11) 90987-6543'
            },
            {
                'nome': 'Ricardo Barbosa Lima',
                'cpf': '012.345.678-90',
                'endereco': 'Rua Teodoro Sampaio, 741',
                'bairro': 'Pinheiros',
                'complemento': 'Loja 15',
                'data_nascimento': date(1979, 6, 7),
                'cidade': 'São Paulo',
                'uf': 'SP',
                'cep': '05405-000',
                'email': 'ricardo.lima@email.com',
                'telefone': '(11) 89876-5432'
            }
        ]

        self.stdout.write("Adicionando clientes de teste...")
        for cliente_data in clientes_teste:
            cliente, created = Cliente.objects.get_or_create(
                cpf=cliente_data['cpf'],
                defaults=cliente_data
            )
            if created:
                self.stdout.write(f"Cliente {cliente.nome} adicionado")
            else:
                self.stdout.write(f"Cliente {cliente.nome} ja existe")

        self.stdout.write(f"\nTotal de clientes no banco: {Cliente.objects.count()}")