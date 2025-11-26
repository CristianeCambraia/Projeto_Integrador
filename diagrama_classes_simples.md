# Diagrama de Classes - Sistema INSUMED

## Representação UML das Classes Principais

```
┌─────────────────────────────────────┐
│              Usuario                │
├─────────────────────────────────────┤
│ - nome: String [unique]             │
│ - email: String [unique]            │
│ - cpf: String [unique]              │
│ - endereco: String                  │
│ - cidade: String                    │
│ - uf: String                        │
│ - telefone: String                  │
│ - data_nascimento: Date             │
│ - senha: String                     │
│ - ativo: Boolean                    │
│ - tentativas_login: Integer         │
│ - bloqueado: Boolean                │
│ - data_bloqueio: DateTime           │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────────┐
│           Orcamento                 │
├─────────────────────────────────────┤
│ - cliente: String                   │
│ - cnpj: String                      │
│ - endereco: String                  │
│ - cidade: String                    │
│ - uf: String                        │
│ - telefone: String                  │
│ - email: String                     │
│ - itens_unidades: Text              │
│ - descricao: Text                   │
│ - itens_quantidades: Text           │
│ - itens_valores: Text               │
│ - observacao: Text                  │
│ - desconto: Decimal                 │
│ - data: Date                        │
│ - usuario: Usuario                  │
│ - data_hora_criacao: DateTime       │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Cliente                  │
├─────────────────────────────────────┤
│ - nome: String [unique]             │
│ - cpf: String [unique]              │
│ - endereco: String                  │
│ - bairro: String                    │
│ - complemento: String               │
│ - data_nascimento: Date             │
│ - cidade: String                    │
│ - uf: String                        │
│ - cep: String                       │
│ - email: String                     │
│ - telefone: String                  │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           Fornecedor                │
├─────────────────────────────────────┤
│ - nome: String [unique]             │
│ - cnpj: String [unique]             │
│ - endereco: String                  │
│ - bairro: String                    │
│ - complemento: String               │
│ - data_nascimento: Date             │
│ - cidade: String                    │
│ - uf: String                        │
│ - cep: String                       │
│ - email: String                     │
│ - telefone: String                  │
│ - ativo: Boolean                    │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────────┐
│             Produto                 │
├─────────────────────────────────────┤
│ - nome: String                      │
│ - codigo_barras: String [unique]    │
│ - preco: Decimal                    │
│ - preco_compra: Decimal             │
│ - descricao: Text                   │
│ - fornecedor: Fornecedor            │
│ - data_hora: DateTime               │
│ - unidade: String                   │
│   [Unidades, Caixa]                 │
│ - quantidade: Integer               │
│ - validade: Date                    │
│ - observacao: Text                  │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌─────────────────────────────────────┐
│        MovimentacaoEstoque          │
├─────────────────────────────────────┤
│ - produto: Produto                  │
│ - tipo: String                      │
│   [ENTRADA, SAIDA]                  │
│ - quantidade: Integer               │
│ - data_hora: DateTime               │
│ - usuario: Usuario                  │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│            Servico                  │
├─────────────────────────────────────┤
│ - nome: String                      │
│ - codigo_barras: String             │
│ - preco: Decimal                    │
│ - descricao: Text                   │
│ - fornecedor: Fornecedor            │
│ - data_hora: DateTime               │
│ - unidade: String                   │
│   [Hora, Semana, Mês, Ano, Serviço]│
│ - quantidade: Integer               │
│ - validade: Date                    │
│ - observacao: Text                  │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           Notificacao               │
├─────────────────────────────────────┤
│ - produto: Produto                  │
│ - tipo: String                      │
│   [VALIDADE, BAIXA_SAIDA,           │
│    ESTOQUE_CRITICO]                 │
│ - titulo: String                    │
│ - mensagem: Text                    │
│ - data_criacao: DateTime            │
│ - lida: Boolean                     │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│              Admin                  │
├─────────────────────────────────────┤
│ - email: String [unique]            │
│ - senha: String                     │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│         RecuperacaoSenha            │
├─────────────────────────────────────┤
│ - email: String                     │
│ - codigo: String                    │
│ - criado_em: DateTime               │
│ - usado: Boolean                    │
├─────────────────────────────────────┤
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│             Suporte                 │
├─────────────────────────────────────┤
│ - nome: String                      │
│ - telefone: String                  │
│ - email: String                     │
│ - descreva: String                  │
│ - data_criacao: DateTime            │
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