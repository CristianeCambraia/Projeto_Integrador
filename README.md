# Sistema INSUMED - Gestão de Estoque Farmacêutico

Sistema desenvolvido para gerenciamento completo de estoque farmacêutico, incluindo controle de produtos, fornecedores, clientes e emissão de orçamentos.

## Funcionalidades Principais

### Gestão de Usuários
- Cadastro de usuários com validação de dados
- Sistema de login seguro com sessões de 24 horas
- Controle de acesso administrativo
- Recuperação de senha via email

### Controle de Estoque
- Cadastro de produtos com código de barras
- Controle de entrada e saída de mercadorias
- Alertas de validade próxima ao vencimento
- Notificações de estoque crítico
- Relatórios de movimentação

### Gestão de Fornecedores
- Cadastro completo de fornecedores
- Controle de status ativo/inativo
- Vinculação de produtos aos fornecedores

### Gestão de Clientes
- Cadastro de clientes pessoa física
- Busca rápida por nome ou CPF
- Histórico de relacionamento

### Emissão de Orçamentos
- Criação de orçamentos personalizados
- Autocomplete de dados do cliente
- Cálculo automático com desconto
- Exportação em PDF
- Envio por email

### Relatórios e Análises
- Relatório financeiro com lucros e perdas
- Balancete por período (dia/mês/ano)
- Relatório de estoque atual
- Exportação de relatórios em PDF

## Tecnologias Utilizadas

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Bibliotecas**: 
  - xhtml2pdf (geração de PDFs)
  - Django Email (envio de emails)

## Estrutura do Projeto

```
Projeto_Integrador/
├── app/
│   ├── models.py          # Modelos do banco de dados
│   ├── views.py           # Lógica de negócio
│   ├── forms.py           # Formulários Django
│   ├── urls.py            # Rotas da aplicação
│   ├── templates/         # Templates HTML
│   └── migrations/        # Migrações do banco
├── static/                # Arquivos estáticos (CSS, JS, imagens)
├── media/                 # Arquivos de upload
├── manage.py              # Gerenciador Django
└── requirements.txt       # Dependências do projeto
```

## Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para instalação

1. Clone o repositório:
```bash
git clone https://github.com/CristianeCambraia/Projeto_Integrador.git
cd Projeto_Integrador
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Crie um superusuário (opcional):
```bash
python manage.py createsuperuser
```

6. Execute o servidor:
```bash
python manage.py runserver
```

7. Acesse o sistema em: `http://localhost:8000`

## Configuração de Email

Para funcionalidade de envio de emails, configure as variáveis no `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-app'
```

## Configuração para Produção

### PostgreSQL
Para usar PostgreSQL em produção, instale o psycopg2 e configure:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'insumed_db',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Backup de Dados
Execute os scripts de backup incluídos:
```bash
python backup_dados.py      # Criar backup
python restaurar_dados.py   # Restaurar backup
```

## Funcionalidades Especiais

### Sistema de Notificações
- Produtos próximos ao vencimento (60 dias)
- Estoque crítico (≤ 5 unidades)
- Produtos sem movimentação (90 dias)
- Produtos vencidos

### Validações Implementadas
- CPF com formatação automática
- Telefone com máscara brasileira
- Data de nascimento com validação de idade mínima (18 anos)
- Senha com mínimo de 8 caracteres
- CNPJ com formatação e validação

### Responsividade
- Interface adaptada para dispositivos móveis
- Formulários otimizados para telas pequenas
- Navegação simplificada em smartphones

## Segurança

- Proteção CSRF em todos os formulários
- Validação de dados no frontend e backend
- Controle de sessões com timeout configurável
- Sanitização de entradas do usuário

## Suporte e Manutenção

O sistema inclui:
- Formulário de suporte integrado
- Logs de movimentação de estoque
- Backup automático de dados críticos
- Monitoramento de performance

## Contribuição

Este projeto foi desenvolvido como Projeto Integrador do curso, seguindo as melhores práticas de desenvolvimento web com Django.

## Licença

Projeto acadêmico - Todos os direitos reservados.

---

**Desenvolvido por**: Cristiane Cambraia  
**Instituição**: [Nome da Instituição]  
**Curso**: [Nome do Curso]  
**Ano**: 2024