from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Cliente, Usuario, Orcamento, MovimentacaoEstoque
from .forms import FornecedorForm, ProdutoForm, ClienteForm, UsuarioForm, SuporteForm, EditarProdutoForm
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .decorators import login_required_custom

# Página inicial (exibe primeiro fornecedor só como exemplo)
def cadastros(request):
    fornecedor = Fornecedor.objects.first()
    return render(request, 'base.html', {'fornecedor': fornecedor})


# Página inicial
def pagina_home(request):
    return render(request, 'home.html')


# Página Sobre Nós
def sobre_nos(request):
    return render(request, 'sobre_nos.html')


# ----- FORNECEDORES -----
@login_required_custom
def abrir_fornecedor(request):
    form = FornecedorForm()
    return render(request, 'fornecedores.html', {'form': form, 'titulo_pagina': 'Novo Fornecedor'})


@login_required_custom
def salvar_fornecedor(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedores.html', {'form': form, 'titulo_pagina': 'Novo Fornecedor'})


@login_required_custom
def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'lista_fornecedores.html', {'fornecedores': fornecedores})


# ----- PRODUTOS -----
@login_required_custom
def cadastrar(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            # Se já existir produto com mesmo nome (case-insensitive), somar quantitades
            nome = form.cleaned_data.get('nome', '').strip()
            quantidade_nova = form.cleaned_data.get('quantidade') or 0
            try:
                quantidade_nova = int(quantidade_nova)
            except (TypeError, ValueError):
                quantidade_nova = 0

            preco_novo = form.cleaned_data.get('preco')
            descricao_nova = form.cleaned_data.get('descricao')
            if descricao_nova is None:
                descricao_nova = ''
            descricao_nova = descricao_nova.strip()
            fornecedor_novo = form.cleaned_data.get('fornecedor')
            unidade_nova = form.cleaned_data.get('unidade')

            # Somar apenas se nome (case-insensitive), descricao (trim) e preco coincidirem
            existente = None
            try:
                existente = Produto.objects.filter(
                    nome__iexact=nome,
                    descricao__iexact=descricao_nova,
                    preco=preco_novo
                ).first()
            except Exception:
                # Em caso de qualquer problema com a query (ex: preco None), garantir que existente seja None
                existente = None

            if existente:
                existente.quantidade = (existente.quantidade or 0) + quantidade_nova
                existente.data_hora = timezone.now()
                existente.save()
                messages.success(request, f'Produto "{existente.nome}" atualizado: quantidade somada.')
            else:
                form.save()
                messages.success(request, 'Produto cadastrado com sucesso.')

            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Produto' 
    })

    

def lista_produtos(request):
    produtos = Produto.objects.all()

    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})



    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos
    })

def salvar_produto(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos.html', {'form': form, 'titulo_pagina': 'Novo Produto'})


def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'Produtos/lista_produtos.html', {'produtos': produtos})


# ----- CLIENTES -----
@login_required_custom
def abrir_cliente(request):
    form = ClienteForm()
    return render(request, 'clientes.html', {'form': form, 'titulo_pagina': 'Novo Cliente'})


def salvar_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_cliente')
    else:
        form = ClienteForm()
    return render(request, 'clientes.html', {'form': form, 'titulo_pagina': 'Novo Cliente'})


def lista_cliente(request):
    clientes = Cliente.objects.all()
    return render(request, 'lista_cliente.html', {'clientes': clientes})


# ----- ORÇAMENTOS ----
@login_required_custom
def emitir_orcamento(request):
    return render(request, 'emitir_orcamento.html', {'range_3': range(1, 4)})


def salvar_orcamento(request):
    if request.method == "POST":
        cliente = request.POST.get('cliente', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        email = request.POST.get('email', '').strip()
        data = request.POST.get('data', '').strip()

        if not cliente or not data:
            return HttpResponseBadRequest("Cliente e Data são obrigatórios")

        try:
            data_obj = parse_date(data)
            if data_obj is None:
                raise ValueError()
        except ValueError:
            return HttpResponseBadRequest("Data inválida")
        # Agrega as descrições, quantidades e valores dos itens (1..3) vindos do formulário
        descricoes = []
        quantidades = []
        valores = []
        for i in range(1, 4):
            d = request.POST.get(f'descricao_{i}', '').strip()
            q = request.POST.get(f'quantidade_{i}', '').strip()
            v = request.POST.get(f'valor_{i}', '').strip()
            descricoes.append(d)
            quantidades.append(q)
            valores.append(v)

        descricao_agregada = ' / '.join([x for x in descricoes if x])
        quantidades_agregadas = ' / '.join([x for x in quantidades if x])
        valores_agregados = ' / '.join([x for x in valores if x])

        orcamento = Orcamento(
            cliente=cliente,
            cnpj=cnpj,
            endereco=endereco,
            cidade=cidade,
            telefone=telefone,
            email=email,
            descricao=descricao_agregada,
            itens_quantidades=quantidades_agregadas,
            itens_valores=valores_agregados,
            data=data_obj
        )
        orcamento.save()
        return redirect('orcamentos_emitidos')
    else:
        return redirect('emitir_orcamento')


def orcamentos_emitidos(request):
    filtro_id = request.GET.get('filtro_id')
    
    if filtro_id:
        try:
            orcamentos = Orcamento.objects.filter(id=filtro_id).order_by('-data')
        except ValueError:
            orcamentos = Orcamento.objects.none()
    else:
        orcamentos = Orcamento.objects.all().order_by('-data')
    
    return render(request, 'lista_orcamentos.html', {
        'orcamentos': orcamentos,
        'filtro_id': filtro_id
    })


@login_required_custom
def editar_descricao(request, orcamento_id):
    try:
        orc = Orcamento.objects.get(id=orcamento_id)
    except Orcamento.DoesNotExist:
        return redirect('orcamentos_emitidos')

    if request.method == 'POST':
        desc = request.POST.get('descricao', '').strip()
        orc.descricao = desc
        orc.save()
        return redirect('orcamentos_emitidos')

    return render(request, 'editar_descricao.html', {'orcamento': orc})


@login_required_custom
def abrir_orcamento(request, orcamento_id):
    try:
        orc = Orcamento.objects.get(id=orcamento_id)
    except Orcamento.DoesNotExist:
        return redirect('orcamentos_emitidos')

    # Aqui podemos formatar os itens se houver necessidade
    # dividir a descricao agregada em até 3 itens (se foi salva como ' / ')
    # construir listas de descricoes, quantidades e valores (mantendo 3 posições)
    descrs = [''] * 3
    qts = [''] * 3
    vals = [''] * 3
    if orc.descricao:
        parts = [p.strip() for p in orc.descricao.split(' / ')]
        for i, p in enumerate(parts[:3]):
            descrs[i] = p
    if orc.itens_quantidades:
        parts_q = [p.strip() for p in orc.itens_quantidades.split(' / ')]
        for i, p in enumerate(parts_q[:3]):
            qts[i] = p
    if orc.itens_valores:
        parts_v = [p.strip() for p in orc.itens_valores.split(' / ')]
        for i, p in enumerate(parts_v[:3]):
            vals[i] = p

    linhas = []
    for i in range(3):
        linhas.append({'descricao': descrs[i], 'quantidade': qts[i], 'valor': vals[i]})

    return render(request, 'abrir_orcamento.html', {
        'orcamento': orc,
        'linhas': linhas,
    })


def novo_orcamento(request):
    return redirect('emitir_orcamento')


def voltar(request):
    return redirect('home')  # alterei para 'home', que existe

# ----- RELATÓRIOS -----
@login_required_custom
def relatorio_estoque(request):
    busca = request.GET.get('q')
    if busca:
        produtos = Produto.objects.filter(nome__icontains=busca)
    else:
        produtos = Produto.objects.all()
    return render(request, 'relatorio_estoque.html', {'produtos': produtos})

def relatorio_entrada(request):
    produtos = Produto.objects.all()

    if request.method == "POST":
        for produto in produtos:
            qtd_recebida = request.POST.get(f"quantidade_{produto.id}")
            if qtd_recebida and qtd_recebida.isdigit() and int(qtd_recebida) > 0:
                qtd = int(qtd_recebida)
                produto.quantidade += qtd
                produto.data_hora = timezone.now()
                produto.save()
                
                # Registrar movimentação
                MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='ENTRADA',
                    quantidade=qtd
                )
        return redirect('relatorio_entrada')

    return render(request, 'relatorio_entrada.html', {'produtos': produtos})


def relatorio_saida(request):
    produtos = Produto.objects.all()

    if request.method == "POST":
        for produto in produtos:
            qtd_retirada = request.POST.get(f"quantidade_{produto.id}")
            if qtd_retirada and int(qtd_retirada) > 0:
                qtd_retirada = int(qtd_retirada)

                if produto.quantidade - qtd_retirada >= 0:
                    produto.quantidade -= qtd_retirada
                    produto.save()
                    
                    # Registrar movimentação
                    MovimentacaoEstoque.objects.create(
                        produto=produto,
                        tipo='SAIDA',
                        quantidade=qtd_retirada
                    )
                else:
                    messages.error(request, f"O produto {produto.nome} não pode sofrer de retirada por falta de estoque!")

        return redirect("relatorio_saida")

    return render(request, "relatorio_saida.html", {"produtos": produtos})

# ----- SUPORTE -----
def criar_suporte(request):
    if request.method == "POST":
        form = SuporteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Solicitação enviada com sucesso!')
            return redirect("criar_suporte")  # redireciona para o próprio form
    else:
        form = SuporteForm()

    return render(request, "suporte_form.html", {"form": form})


# ----- USUÁRIO -----
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # redireciona para home depois do cadastro
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/cadastrar_usuario.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Usuário'
    })
    



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            
            try:
                usuario = Usuario.objects.get(email=email, senha=senha)
                request.session['usuario_logado'] = usuario.id
                
                remember = form.cleaned_data.get('remember', False)
                if remember:
                    request.session.set_expiry(None)  # Não expira
                else:
                    request.session.set_expiry(1800)  # 30 minutos
                    
                messages.success(request, f'Bem-vindo, {usuario.nome}!')
                return redirect('home')
            except Usuario.DoesNotExist:
                messages.error(request, 'Email ou senha incorretos')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

def dashboard(request):
    return render(request, 'login.html', {'titulo_pagina': 'login'})

def logout_view(request):
    if 'usuario_logado' in request.session:
        del request.session['usuario_logado']
    return redirect('login')
 

@login_required_custom
def editar_produto(request, produto_id):
    produto = Produto.objects.get(id=produto_id)
    if request.method == "POST":
        form = EditarProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = EditarProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {
        'form': form,
        'produto': produto,
        'titulo_pagina': 'Editar Produto'
    })
@login_required_custom
def editar_fornecedor(request, fornecedor_id):
    fornecedor = Fornecedor.objects.get(id=fornecedor_id)
    if request.method == "POST":
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)
    return render(request, 'editar_fornecedor.html', {
        'form': form,
        'fornecedor': fornecedor,
        'titulo_pagina': 'Editar Fornecedor'
    })

@login_required_custom
def editar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_cliente')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {
        'form': form,
        'cliente': cliente,
        'titulo_pagina': 'Editar Cliente'
    })
@login_required_custom
def relatorio_movimentacao_entrada(request):
    movimentacoes = MovimentacaoEstoque.objects.filter(tipo='ENTRADA').order_by('-data_hora')
    return render(request, 'relatorio_movimentacao_entrada.html', {'movimentacoes': movimentacoes})

@login_required_custom
def relatorio_movimentacao_saida(request):
    movimentacoes = MovimentacaoEstoque.objects.filter(tipo='SAIDA').order_by('-data_hora')
    return render(request, 'relatorio_movimentacao_saida.html', {'movimentacoes': movimentacoes})