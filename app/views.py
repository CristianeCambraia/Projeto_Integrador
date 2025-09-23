from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Cliente
from .forms import FornecedorForm, ProdutoForm, ClienteForm,SuporteForm
from .models import Orcamento
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest

# Página inicial (exibe primeiro fornecedor só como exemplo)


def cadastros(request):
    fornecedor = Fornecedor.objects.first()
    return render(request, 'base.html', {'fornecedor': fornecedor})

def pagina_home(request):
    return render(request, 'home.html')


def sobre_nos(request):
    return render(request,'sobre_nos.html')

# ----- FORNECEDORES -----
def abrir_fornecedor(request):
    form = FornecedorForm()
    return render(request, 'fornecedores.html', {'form': form, 'titulo_pagina': 'Novo Fornecedor'})


def salvar_fornecedor(request):
    if request.method == "POST":
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedores.html', {'form': form, 'titulo_pagina': 'Novo Fornecedor'})


def lista_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'lista_fornecedores.html', {'fornecedores': fornecedores})


# ----- PRODUTOS -----
def cadastrar(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Produto'
    })


def lista_produtos(request):
    produtos = Produto.objects.all()
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


def cadastrar(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {'form': form, 'titulo_pagina': 'Cadastro de Produto'})


# ----- CLIENTES -----

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

def emitir_orcamento(request):
    return render(request, 'emitir_orcamento.html', {
        'range_3': range(1, 4)  # vai gerar 1, 2, 3
    })


# Salvar orçamento no banco de dados
def salvar_orcamento(request):
    if request.method == "POST":
        cliente = request.POST.get('cliente', '').strip()
        cnpj = request.POST.get('cnpj', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        email = request.POST.get('email', '').strip()
        data = request.POST.get('data', '').strip()

        # Validação simples
        if not cliente or not data:
            return HttpResponseBadRequest("Cliente e Data são obrigatórios")

        try:
            data_obj = parse_date(data)
            if data_obj is None:
                raise ValueError()
        except ValueError:
            return HttpResponseBadRequest("Data inválida")

        orcamento = Orcamento(
            cliente=cliente,
            cnpj=cnpj,
            endereco=endereco,
            cidade=cidade,
            telefone=telefone,
            email=email,
            data=data_obj
        )
        orcamento.save()
        return redirect('orcamentos_emitidos')
    else:
        return redirect('emitir_orcamento')

# Listar orçamentos emitidos
def orcamentos_emitidos(request):
    orcamentos = Orcamento.objects.all().order_by('-data')
    return render(request, 'lista_orcamentos.html', {'orcamentos': orcamentos})

# Rota para novo orçamento (redirecionar para emitir_orcamento)
def novo_orcamento(request):
    return redirect('emitir_orcamento')

# Rota para voltar (exemplo, redirecionar para home ou outra)
def voltar(request):
    return redirect('cadastros')  # ou para a página inicial que você desejar





def criar_suporte(request):
    if request.method == "POST":
        form = SuporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("criar_suporte")  # redireciona para o próprio form
    else:
        form = SuporteForm()

    return render(request, "suporte_form.html", {"form": form})


