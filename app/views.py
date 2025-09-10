from django.shortcuts import render, redirect, get_object_or_404
from .models import Fornecedor
from .forms import FornecedorForm

def cadastros (request):
    fornecedor = Fornecedor.objects.first()
    return render(request, 'base.html', {'fornecedor': fornecedor})




def abrir_fornecedor(request):
    form = FornecedorForm()
    return render(request, 'fornecedores.html',{'form': form, 'titulo_pagina':'Novo cadastro'})

