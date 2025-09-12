from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Cliente
from .forms import FornecedorForm, ProdutoForm, ClienteForm


# Página inicial (exibe primeiro fornecedor só como exemplo)
def cadastros(request):
    fornecedor = Fornecedor.objects.first()
    return render(request, 'base.html', {'fornecedor': fornecedor})


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
def abrir_produto(request):
    form = ProdutoForm()
    return render(request, 'produtos.html', {'form': form, 'titulo_pagina': 'Novo Produto'})


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


