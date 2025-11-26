# Diagrama de Classes - Sistema INSUMED

## Representação UML das Classes Principais

```
┌─────────────────────────────────────┐
│              Usuario                │
├─────────────────────────────────────┤
│ - nome: CharField(200) [unique]     │
│ - email: EmailField(200) [unique]   │
│ - cpf: CharField(20) [unique]       │
│ - endereco: CharField(200)          │
│ - cidade: CharField(200)            │
│ - uf: CharField(2)                  │
│ - telefone: CharField(20)           │
│ - data_nascimento: DateField        │
│ - senha: CharField(128)             │
│ - ativo: BooleanField               │
│ - tentativas_login: IntegerField    │
│ - bloqueado: BooleanField           │
│ - data_bloqueio: DateTimeField      │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────────┐
│           Orcamento                 │
├─────────────────────────────────────┤
│ - cliente: CharField(100)           │
│ - cnpj: CharField(20)               │
│ - endereco: CharField(200)          │
│ - cidade: CharField(50)             │
│ - uf: CharField(2)                  │
│ - telefone: CharField(20)           │
│ - email: EmailField                 │
│ - itens_unidades: TextField         │
│ - descricao: TextField              │
│ - itens_quantidades: TextField      │
│ - itens_valores: TextField          │
│ - observacao: TextField             │
│ - desconto: DecimalField(5,2)       │
│ - data: DateField                   │
│ - usuario: ForeignKey(Usuario)      │
│ - data_hora_criacao: DateTimeField  │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Cliente                  │
├─────────────────────────────────────┤
│ - nome: CharField(200) [unique]     │
│ - cpf: CharField(20) [unique]       │
│ - endereco: CharField(200)          │
│ - bairro: CharField(200)            │
│ - complemento: CharField(200)       │
│ - data_nascimento: DateField        │
│ - cidade: CharField(200)            │
│ - uf: CharField(2)                  │
│ - cep: CharField(10)                │
│ - email: EmailField(200)            │
│ - telefone: CharField(20)           │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           Fornecedor                │
├─────────────────────────────────────┤
│ - nome: CharField(200) [unique]     │
│ - cnpj: CharField(20) [unique]      │
│ - endereco: CharField(200)          │
│ - bairro: CharField(200)            │
│ - complemento: CharField(200)       │
│ - data_nascimento: DateField        │
│ - cidade: CharField(200)            │
│ - uf: CharField(2)                  │
│ - cep: CharField(10)                │
│ - email: EmailField(200)            │
│ - telefone: CharField(20)           │
│ - ativo: BooleanField               │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────────┐
│             Produto                 │
├─────────────────────────────────────┤
│ - nome: CharField(100)              │
│ - codigo_barras: CharField(50)      │
│   [unique]                          │
│ - preco: DecimalField(10,2)         │
│ - preco_compra: DecimalField(10,2)  │
│ - descricao: TextField              │
│ - fornecedor: ForeignKey(Fornecedor)│
│ - data_hora: DateTimeField          │
│ - unidade: CharField(50)            │
│   [Unidades, Caixa]                 │
│ - quantidade: IntegerField          │
│ - validade: DateField               │
│ - observacao: TextField             │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────────┐
│        MovimentacaoEstoque          │
├─────────────────────────────────────┤
│ - produto: ForeignKey(Produto)      │
│ - tipo: CharField(10)               │
│   [ENTRADA, SAIDA]                  │
│ - quantidade: IntegerField          │
│ - data_hora: DateTimeField          │
│ - usuario: ForeignKey(Usuario)      │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Servico                  │
├─────────────────────────────────────┤
│ - nome: CharField(100)              │
│ - codigo_barras: CharField(50)      │
│ - preco: DecimalField(10,2)         │
│ - descricao: TextField              │
│ - fornecedor: ForeignKey(Fornecedor)│
│ - data_hora: DateTimeField          │
│ - unidade: CharField(50)            │
│   [Hora, Semana, Mês, Ano, Serviço]│
│ - quantidade: IntegerField          │
│ - validade: DateField               │
│ - observacao: TextField             │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           Notificacao               │
├─────────────────────────────────────┤
│ - produto: ForeignKey(Produto)      │
│ - tipo: CharField(20)               │
│   [VALIDADE, BAIXA_SAIDA,           │
│    ESTOQUE_CRITICO]                 │
│ - titulo: CharField(200)            │
│ - mensagem: TextField               │
│ - data_criacao: DateTimeField       │
│ - lida: BooleanField                │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│              Admin                  │
├─────────────────────────────────────┤
│ - email: EmailField(200) [unique]   │
│ - senha: CharField(128)             │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         RecuperacaoSenha            │
├─────────────────────────────────────┤
│ - email: EmailField                 │
│ - codigo: CharField(6)              │
│ - criado_em: DateTimeField          │
│ - usado: BooleanField               │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│             Suporte                 │
├─────────────────────────────────────┤
│ - nome: CharField(200)              │
│ - telefone: CharField(20)           │
│ - email: EmailField(200)            │
│ - descreva: CharField(1000)         │
│ - data_criacao: DateTimeField       │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
```

## Relacionamentos Principais

### 1. Usuario → Orcamento (1:N)
- Um usuário pode criar vários orçamentos
- Cada orçamento pertence a um usuário

### 2. Usuario → MovimentacaoEstoque (1:N)
- Um usuário pode realizar várias movimentações
- Cada movimentação é registrada por um usuário

### 3. Fornecedor → Produto (1:N)
- Um fornecedor pode fornecer vários produtos
- Cada produto pertence a um fornecedor

### 4. Fornecedor → Servico (1:N)
- Um fornecedor pode oferecer vários serviços
- Cada serviço pertence a um fornecedor

### 5. Produto → MovimentacaoEstoque (1:N)
- Um produto pode ter várias movimentações
- Cada movimentação refere-se a um produto

### 6. Produto → Notificacao (1:N)
- Um produto pode gerar várias notificações
- Cada notificação refere-se a um produto

## Características do Sistema

### Entidades Principais:
- **Usuario**: Gerencia usuários do sistema com controle de acesso
- **Cliente**: Cadastro de clientes para orçamentos
- **Fornecedor**: Fornecedores de produtos e serviços
- **Produto**: Itens físicos do estoque
- **Servico**: Serviços oferecidos pela empresa

### Funcionalidades:
- **Orcamento**: Geração de orçamentos para clientes
- **MovimentacaoEstoque**: Controle de entrada/saída de produtos
- **Notificacao**: Sistema de alertas (validade, estoque crítico)
- **Suporte**: Sistema de suporte ao usuário
- **RecuperacaoSenha**: Recuperação de senha via email
- **Admin**: Administração do sistema

### Constraints Importantes:
- Campos únicos: nome, email, cpf (Usuario/Cliente)
- Campos únicos: nome, cnpj (Fornecedor)
- Código de barras único (Produto)
- Controle de usuários bloqueados
- Fornecedores ativos/inativos