from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Cliente, Usuario, Orcamento, MovimentacaoEstoque, RecuperacaoSenha, Suporte
from .forms import FornecedorForm, ProdutoForm, ClienteForm, UsuarioForm, SuporteForm, EditarProdutoForm, RecuperarSenhaForm, VerificarCodigoForm, NovaSenhaForm
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .decorators import login_required_custom
from django.conf import settings
from django.db import models

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
    filtro = request.GET.get('filtro')
    
    if filtro:
        fornecedores = Fornecedor.objects.filter(
            models.Q(nome__icontains=filtro) |
            models.Q(cnpj__icontains=filtro)
        ).order_by('nome')
    else:
        fornecedores = Fornecedor.objects.all().order_by('nome')
    
    return render(request, 'lista_fornecedores.html', {
        'fornecedores': fornecedores,
        'filtro': filtro
    })


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
    filtro = request.GET.get('filtro')
    
    if filtro:
        produtos = Produto.objects.filter(
            models.Q(nome__icontains=filtro) |
            models.Q(id__icontains=filtro)
        ).order_by('nome')
    else:
        produtos = Produto.objects.all().order_by('nome')

    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'filtro': filtro
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
        # Agrega as descrições, quantidades e valores dos itens vindos do formulário
        descricoes = []
        quantidades = []
        valores = []
        i = 1
        while True:
            d = request.POST.get(f'descricao_{i}', '').strip()
            q = request.POST.get(f'quantidade_{i}', '').strip()
            v = request.POST.get(f'valor_{i}', '').strip()
            
            if not d and not q and not v:  # Se todos estão vazios, para o loop
                break
                
            descricoes.append(d)
            quantidades.append(q)
            valores.append(v)
            i += 1

        descricao_agregada = ' / '.join([x for x in descricoes if x])
        quantidades_agregadas = ' / '.join([x for x in quantidades if x])
        valores_agregados = ' / '.join([x for x in valores if x])
        observacao = request.POST.get('observacao', '').strip()

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
            observacao=observacao,
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
            suporte = form.save()
            
            # Enviar email real
            try:
                from django.core.mail import send_mail
                send_mail(
                    f'Nova Solicitação de Suporte - #{suporte.id}',
                    f'Nome: {suporte.nome}\nEmail: {suporte.email}\nTelefone: {suporte.telefone}\nDescrição: {suporte.descreva}',
                    settings.DEFAULT_FROM_EMAIL,
                    ['insumed.sistema2025@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, 'Solicitação salva, mas houve problema no envio do email.')
            
            messages.success(request, 'Solicitação enviada por email com sucesso!')
            return redirect("criar_suporte")
    else:
        form = SuporteForm()

    return render(request, "suporte_form.html", {"form": form})

@login_required_custom
def lista_suporte(request):
    filtro = request.GET.get('filtro')
    
    if filtro:
        demandas = Suporte.objects.filter(
            models.Q(id__icontains=filtro) |
            models.Q(nome__icontains=filtro) |
            models.Q(telefone__icontains=filtro)
        ).order_by('-data_criacao')
    else:
        demandas = Suporte.objects.all().order_by('-data_criacao')
    
    return render(request, 'lista_suporte.html', {
        'demandas': demandas,
        'filtro': filtro
    })


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
def alternar_status_fornecedor(request, fornecedor_id):
    fornecedor = Fornecedor.objects.get(id=fornecedor_id)
    fornecedor.ativo = not fornecedor.ativo
    fornecedor.save()
    status = "ativado" if fornecedor.ativo else "desativado"
    messages.success(request, f'Fornecedor {fornecedor.nome} foi {status} com sucesso!')
    return redirect('lista_fornecedores')

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
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import RecuperacaoSenha
from .forms import RecuperarSenhaForm, VerificarCodigoForm, NovaSenhaForm
from datetime import timedelta

def recuperar_senha(request):
    if request.method == 'POST':
        form = RecuperarSenhaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Verificar se o email existe
            try:
                usuario = Usuario.objects.get(email=email)
                
                # Gerar código de 6 dígitos
                codigo = ''.join(random.choices(string.digits, k=6))
                
                # Salvar código no banco
                RecuperacaoSenha.objects.create(email=email, codigo=codigo)
                
                # Enviar email (simulado - você precisa configurar SMTP)
                try:
                    send_mail(
                        'Código de Recuperação - INSUMED',
                        f'Seu código de recuperação é: {codigo}',
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Código enviado para seu email!')
                    request.session['email_recuperacao'] = email
                    return redirect('verificar_codigo')
                except:
                    messages.error(request, 'Erro ao enviar email. Tente novamente.')
                    request.session['email_recuperacao'] = email
                    return redirect('verificar_codigo')
                    
            except Usuario.DoesNotExist:
                messages.error(request, 'Email não encontrado')
    else:
        form = RecuperarSenhaForm()
    
    return render(request, 'recuperar_senha.html', {'form': form})

def verificar_codigo(request):
    email = request.session.get('email_recuperacao')
    if not email:
        return redirect('recuperar_senha')
    
    if request.method == 'POST':
        form = VerificarCodigoForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            
            # Verificar código (válido por 30 minutos)
            try:
                recuperacao = RecuperacaoSenha.objects.get(
                    email=email,
                    codigo=codigo,
                    usado=False,
                    criado_em__gte=timezone.now() - timedelta(minutes=30)
                )
                request.session['codigo_valido'] = True
                return redirect('nova_senha')
            except RecuperacaoSenha.DoesNotExist:
                messages.error(request, 'Código inválido ou expirado')
    else:
        form = VerificarCodigoForm()
    
    return render(request, 'verificar_codigo.html', {'form': form, 'email': email})

def nova_senha(request):
    email = request.session.get('email_recuperacao')
    codigo_valido = request.session.get('codigo_valido')
    
    if not email or not codigo_valido:
        return redirect('recuperar_senha')
    
    if request.method == 'POST':
        form = NovaSenhaForm(request.POST)
        if form.is_valid():
            nova_senha = form.cleaned_data['nova_senha']
            
            # Atualizar senha do usuário
            usuario = Usuario.objects.get(email=email)
            usuario.senha = nova_senha
            usuario.save()
            
            # Marcar código como usado
            RecuperacaoSenha.objects.filter(email=email, usado=False).update(usado=True)
            
            # Limpar sessão
            del request.session['email_recuperacao']
            del request.session['codigo_valido']
            
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('login')
    else:
        form = NovaSenhaForm()
    
    return render(request, 'nova_senha.html', {'form': form})