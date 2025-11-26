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
│ + login(): Boolean                  │
│ + logout(): void                    │
│ + bloquear(): void                  │
│ + desbloquear(): void               │
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
│ + criar(): void                     │
│ + calcularTotal(): Decimal          │
│ + aplicarDesconto(): void           │
│ + gerarPDF(): void                  │
│ + enviarEmail(): void               │
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
│ + cadastrar(): void                 │
│ + editar(): void                    │
│ + buscarPorCPF(): Cliente           │
│ + buscarPorNome(): Cliente          │
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
│ + cadastrar(): void                 │
│ + editar(): void                    │
│ + ativar(): void                    │
│ + desativar(): void                 │
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
│ + cadastrar(): void                 │
│ + editar(): void                    │
│ + verificarValidade(): Boolean      │
│ + verificarEstoqueCritico(): Boolean│
│ + atualizarQuantidade(): void       │
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
│ + registrarEntrada(): void          │
│ + registrarSaida(): void            │
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
│ + cadastrar(): void                 │
│ + editar(): void                    │
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
│ + criar(): void                     │
│ + marcarComoLida(): void            │
│ + __str__(): String                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│              Admin                  │
├─────────────────────────────────────┤
│ - email: String [unique]            │
│ - senha: String                     │
├─────────────────────────────────────┤
│ + login(): Boolean                  │
│ + desbloquearUsuario(): void        │
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
│ + gerarCodigo(): String             │
│ + validarCodigo(): Boolean          │
│ + marcarComoUsado(): void           │
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
│ + enviar(): void                    │
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

## Métodos Principais por Classe

### Usuario
- **login()**: Autentica usuário no sistema
- **logout()**: Encerra sessão do usuário
- **bloquear()**: Bloqueia usuário após tentativas falhadas
- **desbloquear()**: Desbloqueia usuário

### Orcamento
- **criar()**: Cria novo orçamento
- **calcularTotal()**: Calcula valor total do orçamento
- **aplicarDesconto()**: Aplica desconto ao orçamento
- **gerarPDF()**: Gera arquivo PDF do orçamento
- **enviarEmail()**: Envia orçamento por email

### Cliente
- **cadastrar()**: Cadastra novo cliente
- **editar()**: Edita dados do cliente
- **buscarPorCPF()**: Busca cliente pelo CPF
- **buscarPorNome()**: Busca cliente pelo nome

### Fornecedor
- **cadastrar()**: Cadastra novo fornecedor
- **editar()**: Edita dados do fornecedor
- **ativar()**: Ativa fornecedor
- **desativar()**: Desativa fornecedor

### Produto
- **cadastrar()**: Cadastra novo produto
- **editar()**: Edita dados do produto
- **verificarValidade()**: Verifica se produto está próximo do vencimento
- **verificarEstoqueCritico()**: Verifica se estoque está crítico
- **atualizarQuantidade()**: Atualiza quantidade em estoque

### MovimentacaoEstoque
- **registrarEntrada()**: Registra entrada de produto
- **registrarSaida()**: Registra saída de produto

### Servico
- **cadastrar()**: Cadastra novo serviço
- **editar()**: Edita dados do serviço

### Notificacao
- **criar()**: Cria nova notificação
- **marcarComoLida()**: Marca notificação como lida

### Admin
- **login()**: Autentica administrador
- **desbloquearUsuario()**: Desbloqueia usuário bloqueado

### RecuperacaoSenha
- **gerarCodigo()**: Gera código de recuperação
- **validarCodigo()**: Valida código informado
- **marcarComoUsado()**: Marca código como usado

### Suporte
- **enviar()**: Envia solicitação de suporte