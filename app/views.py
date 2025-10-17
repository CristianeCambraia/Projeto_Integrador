from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Servico, Cliente, Usuario, Orcamento, MovimentacaoEstoque, RecuperacaoSenha, Suporte, Admin
from .forms import FornecedorForm, ProdutoForm, ServicoForm, ClienteForm, UsuarioForm, SuporteForm, EditarProdutoForm, RecuperarSenhaForm, VerificarCodigoForm, NovaSenhaForm, AdminLoginForm
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
        filtro = filtro.strip()
        if filtro.isdigit():
            produtos = Produto.objects.filter(id=filtro).order_by('nome')
        else:
            produtos = Produto.objects.filter(
                models.Q(nome__icontains=filtro) |
                models.Q(fornecedor__nome__icontains=filtro)
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


# ----- SERVIÇOS -----
@login_required_custom
def cadastrar_servico(request):
    if request.method == "POST":
        form = ServicoForm(request.POST)
        if form.is_valid():
            # Se já existir serviço com mesmo nome (case-insensitive), somar quantitades
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
                existente = Servico.objects.filter(
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
                messages.success(request, f'Serviço "{existente.nome}" atualizado: quantidade somada.')
            else:
                form.save()
                messages.success(request, 'Serviço cadastrado com sucesso.')

            return redirect('lista_servicos')
    else:
        form = ServicoForm()
    return render(request, 'produtos/cadastrar_servico.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Serviço' 
    })

def lista_servicos(request):
    filtro = request.GET.get('filtro')
    
    if filtro:
        filtro = filtro.strip()
        if filtro.isdigit():
            servicos = Servico.objects.filter(id=filtro).order_by('nome')
        else:
            servicos = Servico.objects.filter(
                models.Q(nome__icontains=filtro) |
                models.Q(fornecedor__nome__icontains=filtro)
            ).order_by('nome')
    else:
        servicos = Servico.objects.all().order_by('nome')

    return render(request, 'produtos/lista_servicos.html', {
        'servicos': servicos,
        'filtro': filtro
    })


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
        # Agrega as unidades, descrições, quantidades e valores dos itens vindos do formulário
        unidades = []
        descricoes = []
        quantidades = []
        valores = []
        i = 1
        while True:
            u = request.POST.get(f'unidade_{i}', '').strip()
            d = request.POST.get(f'descricao_{i}', '').strip()
            q = request.POST.get(f'quantidade_{i}', '').strip()
            v = request.POST.get(f'valor_{i}', '').strip()
            
            if not u and not d and not q and not v:  # Se todos estão vazios, para o loop
                break
                
            unidades.append(u)
            descricoes.append(d)
            quantidades.append(q)
            valores.append(v)
            i += 1

        unidades_agregadas = ' / '.join([x for x in unidades if x])
        descricao_agregada = ' / '.join([x for x in descricoes if x])
        quantidades_agregadas = ' / '.join([x for x in quantidades if x])
        valores_agregados = ' / '.join([x for x in valores if x])
        observacao = request.POST.get('observacao', '').strip()
        desconto = request.POST.get('desconto', '').strip()
        
        # Converter desconto para decimal
        desconto_decimal = 0
        if desconto:
            try:
                desconto_decimal = float(desconto)
            except ValueError:
                desconto_decimal = 0

        orcamento = Orcamento(
            cliente=cliente,
            cnpj=cnpj,
            endereco=endereco,
            cidade=cidade,
            telefone=telefone,
            email=email,
            itens_unidades=unidades_agregadas,
            descricao=descricao_agregada,
            itens_quantidades=quantidades_agregadas,
            itens_valores=valores_agregados,
            observacao=observacao,
            desconto=desconto_decimal,
            data=data_obj
        )
        orcamento.save()
        return redirect('orcamentos_emitidos')
    else:
        return redirect('emitir_orcamento')


def orcamentos_emitidos(request):
    filtro = request.GET.get('filtro')
    email_enviado = request.GET.get('email_enviado')
    
    if email_enviado:
        messages.success(request, 'Orçamento enviado por email com sucesso!')
    
    orcamentos = Orcamento.objects.all()
    
    if filtro:
        filtro = filtro.strip()
        if filtro.isdigit():
            orcamentos = orcamentos.filter(id=filtro)
        else:
            orcamentos = orcamentos.filter(cliente__icontains=filtro)
    
    orcamentos = orcamentos.order_by('-data')
    
    # Processar itens de cada orçamento
    orcamentos_processados = []
    for orc in orcamentos:
        unidades = [p.strip() for p in orc.itens_unidades.split(' / ')] if orc.itens_unidades else []
        descricoes = [p.strip() for p in orc.descricao.split(' / ')] if orc.descricao else []
        quantidades = [p.strip() for p in orc.itens_quantidades.split(' / ')] if orc.itens_quantidades else []
        valores = [p.strip() for p in orc.itens_valores.split(' / ')] if orc.itens_valores else []
        
        max_itens = max(len(unidades), len(descricoes), len(quantidades), len(valores))
        
        itens = []
        subtotal = 0
        for i in range(max_itens):
            quantidade = quantidades[i] if i < len(quantidades) else ''
            valor = valores[i] if i < len(valores) else ''
            
            # Calcular subtotal
            try:
                qtd = float(quantidade.replace(',', '.')) if quantidade else 0
                val = float(valor.replace(',', '.')) if valor else 0
                subtotal += qtd * val
            except ValueError:
                pass
            
            itens.append({
                'unidade': unidades[i] if i < len(unidades) else '',
                'descricao': descricoes[i] if i < len(descricoes) else '',
                'quantidade': quantidade,
                'valor': valor
            })
        
        # Calcular desconto e valor final
        desconto_percent = float(orc.desconto) if orc.desconto else 0
        valor_desconto = subtotal * (desconto_percent / 100)
        valor_total = subtotal - valor_desconto
        
        orc.itens_processados = itens
        orc.subtotal = f"{subtotal:.2f}".replace('.', ',')
        orc.valor_desconto = f"{valor_desconto:.2f}".replace('.', ',')
        orc.valor_total = f"{valor_total:.2f}".replace('.', ',')
        orcamentos_processados.append(orc)
    
    return render(request, 'lista_orcamentos.html', {
        'orcamentos': orcamentos_processados,
        'filtro': filtro
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

    # Dividir os dados agregados em listas
    unidades = [p.strip() for p in orc.itens_unidades.split(' / ')] if orc.itens_unidades else []
    descricoes = [p.strip() for p in orc.descricao.split(' / ')] if orc.descricao else []
    quantidades = [p.strip() for p in orc.itens_quantidades.split(' / ')] if orc.itens_quantidades else []
    valores = [p.strip() for p in orc.itens_valores.split(' / ')] if orc.itens_valores else []
    
    # Determinar o número máximo de itens
    max_itens = max(len(unidades), len(descricoes), len(quantidades), len(valores)) if any([unidades, descricoes, quantidades, valores]) else 0
    
    # Criar lista de linhas com todos os itens e calcular subtotal
    linhas = []
    subtotal = 0
    for i in range(max_itens):
        quantidade = quantidades[i] if i < len(quantidades) else ''
        valor = valores[i] if i < len(valores) else ''
        
        # Calcular subtotal
        try:
            qtd = float(quantidade.replace(',', '.')) if quantidade else 0
            val = float(valor.replace(',', '.')) if valor else 0
            subtotal += qtd * val
        except ValueError:
            pass
        
        linhas.append({
            'unidade': unidades[i] if i < len(unidades) else '',
            'descricao': descricoes[i] if i < len(descricoes) else '',
            'quantidade': quantidade,
            'valor': valor
        })
    
    # Se não houver itens, criar pelo menos uma linha vazia
    if not linhas:
        linhas = [{'unidade': '', 'descricao': '', 'quantidade': '', 'valor': ''}]
    
    # Calcular desconto e valor final
    desconto_percent = float(orc.desconto) if orc.desconto else 0
    valor_desconto = subtotal * (desconto_percent / 100)
    valor_total = subtotal - valor_desconto
    
    # Adicionar valores calculados ao orçamento
    orc.subtotal_calculado = f"{subtotal:.2f}".replace('.', ',')
    orc.valor_desconto_calculado = f"{valor_desconto:.2f}".replace('.', ',')
    orc.valor_total_calculado = f"{valor_total:.2f}".replace('.', ',')

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

def lista_suporte(request):
    # Verificar se é admin
    if 'admin_logado' not in request.session:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar o suporte.')
        return redirect('home')
    filtro = request.GET.get('filtro')
    
    if filtro:
        filtro = filtro.strip()
        if filtro.isdigit():
            demandas = Suporte.objects.filter(
                models.Q(id=filtro) |
                models.Q(telefone=filtro)
            ).order_by('-data_criacao')
        else:
            demandas = Suporte.objects.filter(
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

# ----- ADMIN -----
def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            senha = form.cleaned_data['senha']
            
            try:
                admin = Admin.objects.get(email=email, senha=senha)
                request.session['admin_logado'] = admin.id
                messages.success(request, f'Bem-vindo, Admin!')
                return redirect('home')
            except Admin.DoesNotExist:
                messages.error(request, 'Email ou senha de admin incorretos')
    else:
        form = AdminLoginForm()
    
    return render(request, 'admin_login.html', {'form': form})

def admin_logout(request):
    if 'admin_logado' in request.session:
        del request.session['admin_logado']
    return redirect('login')

# ----- BUSCAR CLIENTES PARA AUTOCOMPLETE -----
def buscar_clientes(request):
    if request.method == 'GET':
        termo = request.GET.get('termo', '').strip()
        if termo:
            clientes = Cliente.objects.filter(nome__icontains=termo)[:10]
            resultados = []
            for cliente in clientes:
                resultados.append({
                    'nome': cliente.nome,
                    'email': cliente.email,
                    'telefone': cliente.telefone,
                    'endereco': cliente.endereco,
                    'cidade': cliente.cidade,
                    'cpf': cliente.cpf
                })
            return JsonResponse({'clientes': resultados})
    return JsonResponse({'clientes': []})

# ----- EXPORTAR PDF ORÇAMENTO -----
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def exportar_pdf_orcamento(request, orcamento_id):
    try:
        orcamento = Orcamento.objects.get(id=orcamento_id)
    except Orcamento.DoesNotExist:
        return redirect('orcamentos_emitidos')
    
    # Processar itens do orçamento
    descricoes = orcamento.descricao.split(' / ') if orcamento.descricao else []
    quantidades = orcamento.itens_quantidades.split(' / ') if orcamento.itens_quantidades else []
    valores = orcamento.itens_valores.split(' / ') if orcamento.itens_valores else []
    
    itens = []
    for i in range(max(len(descricoes), len(quantidades), len(valores))):
        itens.append({
            'descricao': descricoes[i] if i < len(descricoes) else '',
            'quantidade': quantidades[i] if i < len(quantidades) else '',
            'valor': valores[i] if i < len(valores) else ''
        })
    
    context = {
        'orcamento': orcamento,
        'linhas': itens
    }
    
    template = get_template('orcamento_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="orcamento_{orcamento.id}.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    return response

# ----- BUSCAR PRODUTO POR CÓDIGO -----
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def buscar_produto_por_codigo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo_barras = data.get('codigo_barras', '').strip()
            
            if codigo_barras:
                try:
                    produto = Produto.objects.get(codigo_barras=codigo_barras)
                    return JsonResponse({
                        'encontrado': True,
                        'nome': produto.nome,
                        'preco': str(produto.preco),
                        'descricao': produto.descricao or '',
                        'fornecedor': produto.fornecedor.id if produto.fornecedor else '',
                        'unidade': produto.unidade,
                        'observacao': produto.observacao or ''
                    })
                except Produto.DoesNotExist:
                    return JsonResponse({'encontrado': False})
            
            return JsonResponse({'encontrado': False})
        except:
            return JsonResponse({'encontrado': False})
    
    return JsonResponse({'encontrado': False})

# ----- ENVIAR ORÇAMENTO POR EMAIL -----
@csrf_exempt
def enviar_orcamento_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            orcamento_id = data.get('orcamento_id')
            email_destino = data.get('email')
            
            if not orcamento_id or not email_destino:
                return JsonResponse({'success': False, 'error': 'Dados incompletos'})
            
            orcamento = Orcamento.objects.get(id=orcamento_id)
            
            # Gerar PDF
            descricoes = orcamento.descricao.split(' / ') if orcamento.descricao else []
            quantidades = orcamento.itens_quantidades.split(' / ') if orcamento.itens_quantidades else []
            valores = orcamento.itens_valores.split(' / ') if orcamento.itens_valores else []
            
            itens = []
            for i in range(max(len(descricoes), len(quantidades), len(valores))):
                itens.append({
                    'descricao': descricoes[i] if i < len(descricoes) else '',
                    'quantidade': quantidades[i] if i < len(quantidades) else '',
                    'valor': valores[i] if i < len(valores) else ''
                })
            
            context = {'orcamento': orcamento, 'linhas': itens}
            template = get_template('orcamento_pdf.html')
            html = template.render(context)
            
            # Criar PDF em memória
            from io import BytesIO
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
            
            if pisa_status.err:
                return JsonResponse({'success': False, 'error': 'Erro ao gerar PDF'})
            
            pdf_buffer.seek(0)
            
            # Enviar email com anexo
            from django.core.mail import EmailMessage
            email = EmailMessage(
                f'Orçamento #{orcamento.id} - {orcamento.cliente}',
                f'Segue em anexo o orçamento solicitado.\n\nCliente: {orcamento.cliente}\nData: {orcamento.data.strftime("%d/%m/%Y")}',
                settings.DEFAULT_FROM_EMAIL,
                [email_destino]
            )
            email.attach(f'orcamento_{orcamento.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send()
            
            return JsonResponse({'success': True})
            
        except Orcamento.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Orçamento não encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})