from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Servico, Cliente, Usuario, Orcamento, MovimentacaoEstoque, RecuperacaoSenha, Suporte, Admin, Notificacao
from .forms import FornecedorForm, ProdutoForm, ServicoForm, ClienteForm, UsuarioForm, SuporteForm, EditarProdutoForm, RecuperarSenhaForm, VerificarCodigoForm, NovaSenhaForm, AdminLoginForm
from django.utils.dateparse import parse_date
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .decorators import login_required_custom
from django.conf import settings
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
import json
from datetime import datetime, timedelta

def formatar_valor_brasileiro(valor):
    """Formata valor para padrão brasileiro: 1.234,56"""
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Página de cadastros - menu principal
@login_required_custom
def cadastros(request):
    return render(request, 'menu_cadastros.html')


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
        try:
            # Dados obrigatórios
            nome = request.POST.get('nome', '').strip()
            preco = request.POST.get('preco', '0')
            unidade = request.POST.get('unidade', 'Unidade')
            quantidade = request.POST.get('quantidade', '0')
            
            if not nome or not preco or not unidade or not quantidade:
                messages.error(request, 'Preencha todos os campos obrigatórios.')
                return render(request, 'Produtos/cadastrar_produto.html')
            
            # Criar produto com dados básicos
            produto = Produto(
                nome=nome,
                preco=float(preco),
                unidade=unidade,
                quantidade=int(quantidade)
            )
            
            # Dados opcionais
            codigo_barras = request.POST.get('codigo_barras', '').strip()
            if codigo_barras:
                produto.codigo_barras = codigo_barras
                
            preco_compra = request.POST.get('preco_compra', '').strip()
            if preco_compra:
                produto.preco_compra = float(preco_compra)
            else:
                produto.preco_compra = 0
                
            descricao = request.POST.get('descricao', '').strip()
            if descricao:
                produto.descricao = descricao
                
            observacao = request.POST.get('observacao', '').strip()
            if observacao:
                produto.observacao = observacao
                
            validade = request.POST.get('validade', '').strip()
            if validade:
                from datetime import datetime
                produto.validade = datetime.strptime(validade, '%Y-%m-%d').date()
            
            fornecedor_id = request.POST.get('fornecedor', '').strip()
            if fornecedor_id and fornecedor_id.isdigit():
                try:
                    fornecedor = Fornecedor.objects.get(id=int(fornecedor_id))
                    produto.fornecedor = fornecedor
                except Fornecedor.DoesNotExist:
                    pass
                
            produto.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('cadastrar_produto')
            
        except ValueError as e:
            messages.error(request, 'Erro nos dados informados. Verifique os valores numéricos.')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar produto: {str(e)}')
    
    return render(request, 'Produtos/cadastrar_produto.html', {
        'titulo_pagina': 'Cadastro de Produto' 
    })

    

@login_required_custom
def lista_produtos(request):
    filtro = request.GET.get('filtro')
    periodo = request.GET.get('periodo')
    
    produtos = Produto.objects.all()
    
    # Filtro por busca
    if filtro:
        filtro = filtro.strip()
        
        if filtro.isdigit() and len(filtro) <= 6:  # IDs normalmente são menores
            produtos = produtos.filter(id=filtro)
        else:
            produtos = produtos.filter(
                models.Q(nome__icontains=filtro) |
                models.Q(fornecedor__nome__icontains=filtro) |
                models.Q(codigo_barras__icontains=filtro)
            )
    
    # Filtro por período
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    produtos = produtos.order_by('-data_hora')

    return render(request, 'Produtos/lista_produtos.html', {
        'produtos': produtos,
        'filtro': filtro
    })

def salvar_produto(request):
    # Redirecionar para a view cadastrar que já funciona
    return redirect('cadastrar_produto')


# ----- SERVIÇOS -----
@login_required_custom
def cadastrar_servico(request):
    if request.method == "POST":
        form = ServicoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Serviço cadastrado com sucesso.')
                return redirect('cadastrar_servico')
            except Exception as e:
                messages.error(request, f'Erro ao cadastrar serviço: {str(e)}')
    else:
        form = ServicoForm()
    
    return render(request, 'Produtos/cadastrar_servico.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Serviço' 
    })

@login_required_custom
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

    return render(request, 'Produtos/lista_servicos.html', {
        'servicos': servicos,
        'filtro': filtro
    })

@login_required_custom
def editar_servico(request, servico_id):
    try:
        servico = Servico.objects.get(id=servico_id)
    except Servico.DoesNotExist:
        messages.error(request, 'Serviço não encontrado')
        return redirect('lista_servicos')
    
    if request.method == "POST":
        form = ServicoForm(request.POST, instance=servico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Serviço atualizado com sucesso!')
            return redirect('lista_servicos')
    else:
        form = ServicoForm(instance=servico)
    
    return render(request, 'Produtos/editar_servico.html', {
        'form': form,
        'servico': servico,
        'titulo_pagina': 'Editar Serviço'
    })

@login_required_custom
def excluir_servico(request, servico_id):
    try:
        servico = Servico.objects.get(id=servico_id)
        servico.delete()
        messages.success(request, 'Serviço excluído com sucesso!')
    except Servico.DoesNotExist:
        messages.error(request, 'Serviço não encontrado')
    return redirect('lista_servicos')


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
    filtro = request.GET.get('filtro')
    
    if filtro:
        clientes = Cliente.objects.filter(nome__icontains=filtro).order_by('nome')
    else:
        clientes = Cliente.objects.all().order_by('nome')
    
    return render(request, 'lista_cliente.html', {
        'clientes': clientes,
        'filtro': filtro
    })


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
        uf = request.POST.get('uf', '').strip()
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

        # Obter usuário logado
        usuario_logado = None
        if 'usuario_logado' in request.session:
            try:
                usuario_id = request.session['usuario_logado']
                usuario_logado = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                pass
        
        orcamento = Orcamento(
            cliente=cliente,
            cnpj=cnpj,
            endereco=endereco,
            cidade=cidade,
            uf=uf,
            telefone=telefone,
            email=email,
            itens_unidades=unidades_agregadas,
            descricao=descricao_agregada,
            itens_quantidades=quantidades_agregadas,
            itens_valores=valores_agregados,
            observacao=observacao,
            desconto=desconto_decimal,
            data=data_obj,
            usuario=usuario_logado
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
            # Buscar APENAS por ID exato
            orcamentos = orcamentos.filter(id=int(filtro))
        else:
            # Tentar filtrar por data no formato dd/mm/yyyy
            try:
                from datetime import datetime
                if '/' in filtro:
                    data_filtro = datetime.strptime(filtro, '%d/%m/%Y').date()
                    orcamentos = orcamentos.filter(data=data_filtro)
                else:
                    # Buscar apenas por nome do cliente
                    orcamentos = orcamentos.filter(cliente__icontains=filtro)
            except ValueError:
                # Se não conseguir converter data, buscar por cliente
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
        orc.subtotal = formatar_valor_brasileiro(subtotal)
        orc.valor_desconto = formatar_valor_brasileiro(valor_desconto)
        orc.valor_total = formatar_valor_brasileiro(valor_total)
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
    
    # Adicionar valores calculados ao orçamento com separador de milhares
    orc.subtotal_calculado = formatar_valor_brasileiro(subtotal)
    orc.valor_desconto_calculado = formatar_valor_brasileiro(valor_desconto)
    orc.valor_total_calculado = formatar_valor_brasileiro(valor_total)

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
    periodo = request.GET.get('periodo')
    
    produtos = Produto.objects.all()
    
    # Filtro por busca
    if busca:
        produtos = produtos.filter(
            models.Q(nome__icontains=busca) |
            models.Q(fornecedor__nome__icontains=busca) |
            models.Q(descricao__icontains=busca) |
            models.Q(codigo_barras__icontains=busca)
        )
    
    # Filtro por período (em dias)
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    # Adicionar informações de movimentação para cada produto
    produtos_com_movimentacao = []
    for produto in produtos:
        ultima_entrada = MovimentacaoEstoque.objects.filter(
            produto=produto, tipo='ENTRADA'
        ).order_by('-data_hora').first()
        
        ultima_saida = MovimentacaoEstoque.objects.filter(
            produto=produto, tipo='SAIDA'
        ).order_by('-data_hora').first()
        
        produto.ultima_entrada = ultima_entrada
        produto.ultima_saida = ultima_saida
        produtos_com_movimentacao.append(produto)
    # Obter usuário logado
    usuario_logado = None
    if 'usuario_logado' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
        except Usuario.DoesNotExist:
            pass
    
    return render(request, 'relatorio_estoque.html', {
        'produtos': produtos_com_movimentacao,
        'usuario_logado': usuario_logado,
        'data_hora_relatorio': timezone.now()
    })

def relatorio_entrada(request):
    periodo = request.GET.get('periodo')
    produtos = Produto.objects.all()
    
    # Filtro por período
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    # Adicionar informações de última entrada
    produtos_com_entrada = []
    for produto in produtos:
        ultima_entrada = MovimentacaoEstoque.objects.filter(
            produto=produto, tipo='ENTRADA'
        ).order_by('-data_hora').first()
        
        produto.ultima_entrada = ultima_entrada
        produtos_com_entrada.append(produto)

    if request.method == "POST":
        produtos = produtos_com_entrada  # Usar a lista com informações de entrada
        for produto in produtos:
            qtd_recebida = request.POST.get(f"quantidade_{produto.id}")
            if qtd_recebida and qtd_recebida.isdigit() and int(qtd_recebida) > 0:
                qtd = int(qtd_recebida)
                produto.quantidade += qtd
                produto.data_hora = timezone.now()
                produto.save()
                
                # Obter usuário logado
                usuario_logado = None
                if 'usuario_logado' in request.session:
                    try:
                        usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
                    except Usuario.DoesNotExist:
                        pass
                
                # Registrar movimentação
                mov = MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='ENTRADA',
                    quantidade=qtd,
                    usuario=usuario_logado
                )
        return redirect('relatorio_entrada')

    return render(request, 'relatorio_entrada.html', {'produtos': produtos_com_entrada})


def relatorio_saida(request):
    if request.method == 'POST':
        usuario_logado = request.session.get('usuario_logado')
        if not usuario_logado:
            messages.error(request, 'Usuário não está logado.')
            return redirect('login')
        
        try:
            usuario = Usuario.objects.get(id=usuario_logado)
        except Usuario.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
            return redirect('login')
        
        produtos_com_saida = []
        
        for key, value in request.POST.items():
            if key.startswith('quantidade_') and value and int(value) > 0:
                produto_id = key.replace('quantidade_', '')
                quantidade = int(value)
                
                try:
                    produto = Produto.objects.get(id=produto_id)
                    
                    if produto.quantidade >= quantidade:
                        produto.quantidade -= quantidade
                        produto.save()
                        
                        # Registrar movimentação
                        MovimentacaoEstoque.objects.create(
                            produto=produto,
                            tipo='saida',
                            quantidade=quantidade,
                            usuario=usuario
                        )
                        
                        produtos_com_saida.append(f"{produto.nome} ({quantidade} {produto.unidade})")
                    else:
                        messages.error(request, f'Estoque insuficiente para {produto.nome}. Disponível: {produto.quantidade}')
                        
                except Produto.DoesNotExist:
                    messages.error(request, f'Produto com ID {produto_id} não encontrado.')
        

        
        return redirect('relatorio_saida')
    
    # Filtro por período
    periodo = request.GET.get('periodo')
    produtos = Produto.objects.all().order_by('nome')
    
    if periodo:
        try:
            dias = int(periodo)
            data_limite = timezone.now() - timedelta(days=dias)
            produtos = produtos.filter(data_cadastro__gte=data_limite)
        except ValueError:
            pass
    
    # Adicionar última saída para cada produto
    for produto in produtos:
        produto.ultima_saida = MovimentacaoEstoque.objects.filter(
            produto=produto, 
            tipo='saida'
        ).order_by('-data_hora').first()
    
    return render(request, 'relatorio_saida.html', {'produtos': produtos})

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
                    settings.EMAIL_HOST_USER,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, f'Solicitação salva, mas erro no email: {str(e)}')
            
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
    periodo = request.GET.get('periodo')
    
    demandas = Suporte.objects.all()
    
    if filtro:
        filtro = filtro.strip()
        if filtro.isdigit():
            demandas = demandas.filter(
                models.Q(id=filtro) |
                models.Q(telefone__icontains=filtro)
            )
        else:
            demandas = demandas.filter(
                models.Q(nome__icontains=filtro) |
                models.Q(email__icontains=filtro) |
                models.Q(telefone__icontains=filtro) |
                models.Q(descreva__icontains=filtro)
            )
    
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        demandas = demandas.filter(data_criacao__gte=data_limite)
    
    demandas = demandas.order_by('-data_criacao')
    
    return render(request, 'lista_suporte.html', {
        'demandas': demandas,
        'filtro': filtro
    })


# ----- USUÁRIO -----
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuário {usuario.nome} cadastrado com sucesso!')
            return redirect('home')  # redireciona para home depois do cadastro
        else:
            messages.error(request, 'Erro no formulário. Verifique os dados informados.')
    else:
        form = UsuarioForm()
        # Garantir que o campo cidade esteja vazio
        form.fields['cidade'].initial = ''
    return render(request, 'usuarios/cadastrar_usuario.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Usuário'
    })
    



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].strip()
            senha = form.cleaned_data['senha']
            
            # Validação adicional
            if not email or not senha:
                messages.error(request, 'Email e senha são obrigatórios')
                return render(request, 'login.html', {'form': form})
            
            try:
                usuario = Usuario.objects.get(email=email)
                
                # Verificar se o usuário está bloqueado
                if usuario.bloqueado:
                    messages.error(request, 'Usuário bloqueado por excesso de tentativas. Entre em contato com o suporte.')
                    return render(request, 'login.html', {'form': form})
                
                # Verificar se o usuário está ativo
                if not usuario.ativo:
                    messages.error(request, 'Usuário bloqueado. Contate o administrador.')
                    return render(request, 'login.html', {'form': form})
                
                # Verificar senha
                if usuario.senha == senha:
                    # Login correto - resetar tentativas
                    usuario.tentativas_login = 0
                    usuario.save()
                    
                    request.session['usuario_logado'] = usuario.id
                    
                    remember = form.cleaned_data.get('remember', False)
                    if remember:
                        request.session.set_expiry(None)  # Não expira
                    else:
                        request.session.set_expiry(86400)  # 24 horas
                        
                    messages.success(request, f'Bem-vindo, {usuario.nome}!')
                    return redirect('home')
                else:
                    # Senha incorreta - incrementar tentativas
                    usuario.tentativas_login += 1
                    if usuario.tentativas_login >= 5:
                        usuario.bloqueado = True
                        usuario.data_bloqueio = timezone.now()
                        messages.error(request, 'Usuário bloqueado por excesso de tentativas. Entre em contato com o suporte.')
                    else:
                        tentativas_restantes = 5 - usuario.tentativas_login
                        messages.error(request, f'Senha incorreta. Restam {tentativas_restantes} tentativas.')
                    usuario.save()
                    
            except Usuario.DoesNotExist:
                messages.error(request, 'Email não encontrado')
        else:
            messages.error(request, 'Dados inválidos')
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
            messages.success(request, 'Fornecedor atualizado com sucesso!')
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
    if 'usuario_logado' not in request.session:
        return redirect('login')
    
    try:
        fornecedor = Fornecedor.objects.get(id=fornecedor_id)
        fornecedor.ativo = not fornecedor.ativo
        fornecedor.save()
    except:
        pass
    
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
    movimentacoes = MovimentacaoEstoque.objects.filter(tipo='ENTRADA').select_related('produto', 'produto__fornecedor').order_by('-data_hora')
    return render(request, 'relatorio_movimentacao_entrada.html', {'movimentacoes': movimentacoes})

@login_required_custom
def relatorio_movimentacao_saida(request):
    movimentacoes = MovimentacaoEstoque.objects.filter(tipo='SAIDA').select_related('produto', 'produto__fornecedor').order_by('-data_hora')
    return render(request, 'relatorio_movimentacao_saida.html', {'movimentacoes': movimentacoes})
import random
import string
from django.core.mail import send_mail
from .models import RecuperacaoSenha
from .forms import RecuperarSenhaForm, VerificarCodigoForm, NovaSenhaForm

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
                
                # Enviar email
                try:
                    send_mail(
                        'Código de Recuperação - INSUMED',
                        f'Seu código de recuperação é: {codigo}',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, 'Código enviado para seu email!')
                    request.session['email_recuperacao'] = email
                    return redirect('verificar_codigo')
                except Exception as e:
                    messages.error(request, f'Erro ao enviar email: {str(e)}')
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

def usuarios_cadastrados(request):
    # Verificar se é admin
    if 'admin_logado' not in request.session:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    
    # Buscar TODOS os usuários sem limitação
    usuarios = Usuario.objects.all().order_by('-id')
    
    return render(request, 'usuarios_cadastrados.html', {
        'usuarios': usuarios
    })

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
    
    import os
    from django.conf import settings
    
    # Caminho absoluto para a imagem
    static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
    
    context = {
        'orcamento': orcamento,
        'linhas': itens,
        'STATIC_ROOT': static_root
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

@csrf_exempt
def buscar_produto_por_codigo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo_barras = data.get('codigo_barras', '').strip()
            
            if codigo_barras:
                try:
                    # Buscar produto pelo código de barras exato
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
                    # Tentar buscar por código similar (caso tenha espaços ou caracteres extras)
                    produtos_similares = Produto.objects.filter(codigo_barras__icontains=codigo_barras)
                    if produtos_similares.exists():
                        produto = produtos_similares.first()
                        
                        return JsonResponse({
                            'encontrado': True,
                            'nome': produto.nome,
                            'preco': str(produto.preco),
                            'descricao': produto.descricao or '',
                            'fornecedor': produto.fornecedor.id if produto.fornecedor else '',
                            'unidade': produto.unidade,
                            'observacao': produto.observacao or ''
                        })
                    
                    return JsonResponse({'encontrado': False, 'erro': 'Produto não encontrado'})
            
            return JsonResponse({'encontrado': False, 'erro': 'Código vazio'})
        except Exception as e:
            return JsonResponse({'encontrado': False, 'erro': str(e)})
    
    return JsonResponse({'encontrado': False, 'erro': 'Método não permitido'})

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
            
            # Processar itens do orçamento (mesmo código do PDF)
            descricoes = orcamento.descricao.split(' / ') if orcamento.descricao else []
            quantidades = orcamento.itens_quantidades.split(' / ') if orcamento.itens_quantidades else []
            valores = orcamento.itens_valores.split(' / ') if orcamento.itens_valores else []
            unidades = orcamento.itens_unidades.split(' / ') if orcamento.itens_unidades else []
            
            itens = []
            subtotal = 0
            for i in range(max(len(descricoes), len(quantidades), len(valores), len(unidades))):
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
            desconto_percent = float(orcamento.desconto) if orcamento.desconto else 0
            valor_desconto = subtotal * (desconto_percent / 100)
            valor_total = subtotal - valor_desconto
            
            orcamento.subtotal_calculado = f"{subtotal:.2f}".replace('.', ',')
            orcamento.valor_desconto_calculado = f"{valor_desconto:.2f}".replace('.', ',')
            orcamento.valor_total_calculado = f"{valor_total:.2f}".replace('.', ',')
            
            # Usar o mesmo template do PDF
            import os
            static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
            
            context = {
                'orcamento': orcamento,
                'linhas': itens,
                'STATIC_ROOT': static_root
            }
            
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
            try:
                from django.core.mail import EmailMessage
                # Preparar informações do usuário
                info_usuario = ""
                if orcamento.usuario:
                    info_usuario += f"\nCriado por: {orcamento.usuario.nome}"
                if orcamento.data_hora_criacao:
                    info_usuario += f"\nEm: {orcamento.data_hora_criacao.strftime('%d/%m/%Y %H:%M')}"
                
                email = EmailMessage(
                    f'Orçamento #{orcamento.id} - {orcamento.cliente}',
                    f'Segue em anexo o orçamento solicitado.\n\nCliente: {orcamento.cliente}\nData: {orcamento.data.strftime("%d/%m/%Y")}{info_usuario}\n\nAtenciosamente,\nEquipe INSUMED',
                    settings.EMAIL_HOST_USER,
                    [email_destino]
                )
                email.attach(f'orcamento_{orcamento.id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
                email.send()
            except Exception as email_error:
                return JsonResponse({'success': False, 'error': f'Erro no envio: {str(email_error)}'})
            
            return JsonResponse({'success': True})
            
        except Orcamento.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Orçamento não encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

# ----- TESTE NOTIFICAÇÕES -----
def teste_notificacoes(request):
    """View de teste para verificar se as notificações estão funcionando"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Notificações funcionando',
        'notificacoes': [
            {
                'id': 1,
                'titulo': 'Teste',
                'mensagem': 'Esta é uma notificação de teste',
                'icone': '⚠️'
            }
        ],
        'total': 1
    })

def detalhes_notificacao(request, produto_id, tipo):
    """Exibe detalhes de uma notificação específica"""
    # Marcar como lida ao acessar
    try:
        Notificacao.objects.filter(produto_id=produto_id, tipo=tipo, lida=False).update(lida=True)
    except:
        pass
    
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        messages.error(request, 'Produto não encontrado')
        return redirect('lista_produtos')
    
    context = {
        'produto': produto,
        'tipo': tipo,
        'mensagem': ''
    }
    
    hoje = timezone.now().date()
    
    if tipo == 'VENCIDO':
        if hasattr(produto, 'validade') and produto.validade:
            dias_vencidos = (hoje - produto.validade).days
        else:
            dias_vencidos = 5  # Valor padrão para teste
        context['dias_vencidos'] = dias_vencidos
        context['mensagem'] = f'⚠️ PRODUTO VENCIDO - Este produto está vencido há {dias_vencidos} dias e deve ser descartado imediatamente para evitar riscos à saúde. Não comercialize ou utilize este produto.'
        
    elif tipo == 'VALIDADE':
        if hasattr(produto, 'validade') and produto.validade:
            dias_restantes = (produto.validade - hoje).days
        else:
            dias_restantes = 15  # Valor padrão para teste
        context['dias_restantes'] = dias_restantes
        context['mensagem'] = f'Este produto vence em {dias_restantes} dias'
        
    elif tipo == 'ESTOQUE_CRITICO':
        context['mensagem'] = f'Produto com apenas {produto.quantidade} unidades em estoque'
        
    elif tipo == 'BAIXA_SAIDA':
        if hasattr(produto.data_hora, 'date'):
            dias_parado = (hoje - produto.data_hora.date()).days
        else:
            dias_parado = 90  # Valor padrão para teste
        context['dias_parado'] = dias_parado
        context['mensagem'] = f'Produto sem movimentação há {dias_parado} dias'
    
    return render(request, 'detalhes_notificacao.html', context)

# ----- NOTIFICAÇÕES DE ESTOQUE -----

def gerar_notificacoes_estoque():
    """Gera notificações automáticas baseadas nas regras de estoque"""
    try:
        # Limpar notificações antigas (mais de 30 dias)
        Notificacao.objects.filter(data_criacao__lt=timezone.now() - timedelta(days=30)).delete()
        
        hoje = timezone.now().date()
        
        # 1. Produtos próximos da validade (60 dias)
        produtos_validade = Produto.objects.filter(
            validade__isnull=False,
            validade__lte=hoje + timedelta(days=60)
        )
        
        for produto in produtos_validade:
            dias_restantes = (produto.validade - hoje).days
            if not Notificacao.objects.filter(produto=produto, tipo='VALIDADE', lida=False).exists():
                Notificacao.objects.create(
                    produto=produto,
                    tipo='VALIDADE',
                    titulo='Produto próximo da validade',
                    mensagem=f'O produto {produto.nome} vence em {dias_restantes} dias ({produto.validade.strftime("%d/%m/%Y")})'
                )
        
        # 2. Produtos com baixa saída (90 dias sem movimentação)
        data_limite = timezone.now() - timedelta(days=90)
        produtos_sem_saida = Produto.objects.filter(data_hora__lt=data_limite)
        
        for produto in produtos_sem_saida:
            # Verificar se teve saída recente
            teve_saida = MovimentacaoEstoque.objects.filter(
                produto=produto,
                tipo='SAIDA',
                data_hora__gte=data_limite
            ).exists()
            
            if not teve_saida and not Notificacao.objects.filter(produto=produto, tipo='BAIXA_SAIDA', lida=False).exists():
                dias_parado = (timezone.now().date() - produto.data_hora.date()).days
                Notificacao.objects.create(
                    produto=produto,
                    tipo='BAIXA_SAIDA',
                    titulo='Produto com baixa saída',
                    mensagem=f'O produto {produto.nome} está há {dias_parado} dias sem movimentação de saída'
                )
        
        # 3. Estoque crítico (quantidade <= 5)
        produtos_criticos = Produto.objects.filter(quantidade__lte=5)
        
        for produto in produtos_criticos:
            if not Notificacao.objects.filter(produto=produto, tipo='ESTOQUE_CRITICO', lida=False).exists():
                Notificacao.objects.create(
                    produto=produto,
                    tipo='ESTOQUE_CRITICO',
                    titulo='Estoque crítico',
                    mensagem=f'O produto {produto.nome} possui apenas {produto.quantidade} unidades em estoque'
                )
    except Exception as e:
        print(f'Erro ao gerar notificações: {e}')

@csrf_exempt
def obter_notificacoes(request):
    """Retorna notificações baseadas em produtos reais do banco"""
    try:
        if request.method == 'GET':
            from datetime import timedelta
            hoje = timezone.now().date()
            
            # 1. Produtos vencidos
            produtos_vencidos = Produto.objects.filter(
                validade__isnull=False,
                validade__lt=hoje
            )[:10]
            
            # 2. Produtos próximos da validade (60 dias, mas não vencidos)
            produtos_validade = Produto.objects.filter(
                validade__isnull=False,
                validade__gte=hoje,
                validade__lte=hoje + timedelta(days=60)
            )[:10]
            
            # 3. Produtos com estoque crítico (≤ 5 unidades)
            produtos_criticos = Produto.objects.filter(quantidade__lte=5)[:10]
            
            # 4. Produtos com baixa saída (90 dias sem movimentação)
            data_limite = timezone.now() - timedelta(days=90)
            produtos_sem_saida = Produto.objects.filter(data_hora__lt=data_limite)[:10]
            
            tipo_filtro = request.GET.get('tipo')
            
            if tipo_filtro == 'VENCIDO':
                notificacoes = []
                for produto in produtos_vencidos:
                    dias_vencidos = (hoje - produto.validade).days
                    notificacoes.append({
                        'id': produto.id,
                        'produto_id': produto.id,
                        'produto_nome': produto.nome,
                        'mensagem': f'Vencido há {dias_vencidos} dias',
                        'tipo': 'VENCIDO'
                    })
                return JsonResponse({'notificacoes': notificacoes, 'total': len(notificacoes)})
            
            elif tipo_filtro == 'VALIDADE':
                notificacoes = []
                for produto in produtos_validade:
                    dias_restantes = (produto.validade - hoje).days
                    notificacoes.append({
                        'id': produto.id,
                        'produto_id': produto.id,
                        'produto_nome': produto.nome,
                        'mensagem': f'Vence em {dias_restantes} dias',
                        'tipo': 'VALIDADE'
                    })
                return JsonResponse({'notificacoes': notificacoes, 'total': len(notificacoes)})
            
            elif tipo_filtro == 'ESTOQUE_CRITICO':
                notificacoes = []
                for produto in produtos_criticos:
                    notificacoes.append({
                        'id': produto.id,
                        'produto_id': produto.id,
                        'produto_nome': produto.nome,
                        'mensagem': f'Apenas {produto.quantidade} unidades',
                        'tipo': 'ESTOQUE_CRITICO'
                    })
                return JsonResponse({'notificacoes': notificacoes, 'total': len(notificacoes)})
            
            elif tipo_filtro == 'BAIXA_SAIDA':
                notificacoes = []
                for produto in produtos_sem_saida:
                    dias_parado = (hoje - produto.data_hora.date()).days
                    notificacoes.append({
                        'id': produto.id,
                        'produto_id': produto.id,
                        'produto_nome': produto.nome,
                        'mensagem': f'Sem saída há {dias_parado} dias',
                        'tipo': 'BAIXA_SAIDA'
                    })
                return JsonResponse({'notificacoes': notificacoes, 'total': len(notificacoes)})
            
            else:
                # Retornar contadores por categoria
                categorias = [
                    {'tipo': 'VENCIDO', 'titulo': 'Produto vencido', 'icone': '❌', 'count': produtos_vencidos.count()},
                    {'tipo': 'VALIDADE', 'titulo': 'Produto próximo da validade', 'icone': '⚠️', 'count': produtos_validade.count()},
                    {'tipo': 'ESTOQUE_CRITICO', 'titulo': 'Estoque crítico', 'icone': '🔴', 'count': produtos_criticos.count()},
                    {'tipo': 'BAIXA_SAIDA', 'titulo': 'Baixa saída', 'icone': '📦', 'count': produtos_sem_saida.count()}
                ]
                
                total = sum(cat['count'] for cat in categorias)
                
                return JsonResponse({
                    'categorias': categorias,
                    'total': total
                })
    except Exception as e:
        return JsonResponse({
            'categorias': [],
            'total': 0,
            'error': str(e)
        })
    
    return JsonResponse({'categorias': [], 'total': 0})

@csrf_exempt
def marcar_notificacao_lida(request):
    """Marca uma notificação como lida"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            produto_id = data.get('produto_id')
            tipo = data.get('tipo')
            
            if produto_id and tipo:
                # Marcar todas as notificações deste produto e tipo como lidas
                Notificacao.objects.filter(produto_id=produto_id, tipo=tipo, lida=False).update(lida=True)
                return JsonResponse({'success': True})
        except:
            pass
    
    return JsonResponse({'success': False})

@csrf_exempt
def marcar_todas_lidas(request):
    """Marca todas as notificações como lidas"""
    if request.method == 'POST':
        Notificacao.objects.filter(lida=False).update(lida=True)
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False})

# ----- EXPORTAR ESTOQUE PDF -----
def exportar_estoque_pdf(request):
    busca = request.GET.get('q')
    periodo = request.GET.get('periodo')
    
    produtos = Produto.objects.all()
    
    if busca:
        produtos = produtos.filter(
            models.Q(nome__icontains=busca) |
            models.Q(fornecedor__nome__icontains=busca) |
            models.Q(descricao__icontains=busca) |
            models.Q(codigo_barras__icontains=busca)
        )
    
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    produtos_com_movimentacao = []
    for produto in produtos:
        ultima_entrada = MovimentacaoEstoque.objects.filter(
            produto=produto, tipo='ENTRADA'
        ).order_by('-data_hora').first()
        
        ultima_saida = MovimentacaoEstoque.objects.filter(
            produto=produto, tipo='SAIDA'
        ).order_by('-data_hora').first()
        
        produto.ultima_entrada = ultima_entrada
        produto.ultima_saida = ultima_saida
        produtos_com_movimentacao.append(produto)
    
    import os
    from datetime import datetime
    static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
    
    # Obter usuário logado
    usuario_logado = None
    if 'usuario_logado' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
        except Usuario.DoesNotExist:
            pass
    
    context = {
        'produtos': produtos_com_movimentacao,
        'busca': busca,
        'data_atual': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'usuario_logado': usuario_logado,
        'STATIC_ROOT': static_root
    }
    
    template = get_template('estoque_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_estoque.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    return response

@csrf_exempt
def enviar_estoque_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_destino = data.get('email')
            
            if not email_destino:
                return JsonResponse({'success': False, 'error': 'Email não informado'})
            produtos = Produto.objects.all()
            
            produtos_com_movimentacao = []
            for produto in produtos:
                ultima_entrada = MovimentacaoEstoque.objects.filter(
                    produto=produto, tipo='ENTRADA'
                ).order_by('-data_hora').first()
                
                ultima_saida = MovimentacaoEstoque.objects.filter(
                    produto=produto, tipo='SAIDA'
                ).order_by('-data_hora').first()
                
                produto.ultima_entrada = ultima_entrada
                produto.ultima_saida = ultima_saida
                produtos_com_movimentacao.append(produto)
            
            import os
            from datetime import datetime
            static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
            
            # Obter usuário logado
            usuario_logado = None
            if 'usuario_logado' in request.session:
                try:
                    usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
                except Usuario.DoesNotExist:
                    pass
            
            context = {
                'produtos': produtos_com_movimentacao,
                'data_atual': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'usuario_logado': usuario_logado,
                'STATIC_ROOT': static_root
            }
            
            template = get_template('estoque_pdf.html')
            html = template.render(context)
            
            from io import BytesIO
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
            
            if pisa_status.err:
                return JsonResponse({'success': False, 'error': 'Erro ao gerar PDF'})
            
            pdf_buffer.seek(0)
            
            from django.core.mail import EmailMessage
            email = EmailMessage(
                'Relatório de Estoque - INSUMED',
                f'Segue em anexo o relatório de estoque.\n\nTotal de produtos: {len(produtos_com_movimentacao)}\n\nAtenciosamente,\nEquipe INSUMED',
                settings.DEFAULT_FROM_EMAIL,
                [email_destino]
            )
            email.attach('relatorio_estoque.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

# ----- TESTE DEBUG -----
def debug_produtos(request):
    """View de debug para verificar produtos"""
    produtos = Produto.objects.all()
    produtos_data = []
    
    for produto in produtos:
        produtos_data.append({
            'id': produto.id,
            'nome': produto.nome,
            'codigo_barras': produto.codigo_barras,
            'fornecedor': produto.fornecedor.nome if produto.fornecedor else 'Sem fornecedor',
            'quantidade': produto.quantidade
        })
    
    return JsonResponse({
        'total': produtos.count(),
        'produtos': produtos_data
    })

@csrf_exempt
def gerar_senha_temporaria(request):
    if request.method == 'POST':
        # Verificar se é admin
        if 'admin_logado' not in request.session:
            return JsonResponse({'success': False, 'error': 'Acesso negado'})
        
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')
            novo_email = data.get('novo_email', '').strip()
            
            if not usuario_id or not novo_email:
                return JsonResponse({'success': False, 'error': 'Dados incompletos'})
            
            # Verificar se usuário existe
            try:
                usuario = Usuario.objects.get(id=usuario_id)
            except Usuario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})
            
            # Gerar senha temporária de 8 caracteres
            import random
            import string
            senha_temp = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            
            # Enviar email com senha temporária
            try:
                from django.core.mail import send_mail
                send_mail(
                    'Senha Temporária - INSUMED',
                    f'Olá {usuario.nome},\n\nSua senha temporária é: {senha_temp}\n\nUse esta senha para acessar o sistema com seu email original ({usuario.email}) e depois altere sua senha e email nas configurações da conta.\n\nAtenciosamente,\nEquipe INSUMED',
                    settings.DEFAULT_FROM_EMAIL,
                    [novo_email],
                    fail_silently=False,
                )
                
                # Atualizar senha do usuário no banco
                usuario.senha = senha_temp
                usuario.save()
                
                return JsonResponse({
                    'success': True, 
                    'message': f'Senha temporária enviada para {novo_email}'
                })
                
            except Exception as e:
                return JsonResponse({'success': False, 'error': f'Erro ao enviar email: {str(e)}'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@csrf_exempt
def deletar_usuario(request):
    if request.method == 'POST':
        # Verificar se é admin
        if 'admin_logado' not in request.session:
            return JsonResponse({'success': False, 'error': 'Acesso negado'})
        
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')
            
            if not usuario_id:
                return JsonResponse({'success': False, 'error': 'ID do usuário não informado'})
            
            # Verificar se usuário existe e deletar
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                nome_usuario = usuario.nome
                usuario.delete()
                
                return JsonResponse({
                    'success': True, 
                    'message': f'Usuário {nome_usuario} deletado com sucesso'
                })
                
            except Usuario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

@csrf_exempt
def verificar_status_usuario(request):
    if request.method == 'POST':
        if 'usuario_logado' in request.session:
            try:
                usuario_id = request.session['usuario_logado']
                usuario = Usuario.objects.get(id=usuario_id)
                print(f"DEBUG: Verificando usuário {usuario.nome} - Status: {usuario.ativo}")
                return JsonResponse({'ativo': usuario.ativo})
            except Usuario.DoesNotExist:
                return JsonResponse({'ativo': False})
        return JsonResponse({'ativo': False})
    return JsonResponse({'ativo': False})

@csrf_exempt
def alternar_status_usuario(request):
    if request.method == 'POST':
        if 'admin_logado' not in request.session:
            return JsonResponse({'success': False, 'error': 'Acesso negado'})
        
        try:
            data = json.loads(request.body)
            usuario_id = data.get('usuario_id')
            ativo = data.get('ativo')
            
            if usuario_id is None or ativo is None:
                return JsonResponse({'success': False, 'error': 'Dados incompletos'})
            
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                print(f"DEBUG ANTES: {usuario.nome} - Ativo: {usuario.ativo}")
                usuario.ativo = bool(ativo)
                usuario.save()
                usuario.refresh_from_db()
                print(f"DEBUG DEPOIS: {usuario.nome} - Ativo: {usuario.ativo}")
                
                # Se usuário foi desativado, deslogar todas as sessões dele
                if not ativo:
                    # Buscar e deletar todas as sessões do usuário
                    for session in Session.objects.all():
                        session_data = session.get_decoded()
                        if session_data.get('usuario_logado') == usuario_id:
                            session.delete()
                
                status_texto = 'ativado' if ativo else 'desativado'
                
                return JsonResponse({
                    'success': True, 
                    'message': f'Usuário {usuario.nome} {status_texto} com sucesso'
                })
                
            except Usuario.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Usuário não encontrado'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

# ----- RELATÓRIO FINANCEIRO -----
@login_required_custom
def relatorio_financeiro(request):
    periodo = request.GET.get('periodo', 'mes')
    
    from datetime import datetime, timedelta
    hoje = timezone.now().date()
    
    # Definir período de filtro
    if periodo == 'dia':
        data_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        titulo_periodo = f"Hoje ({hoje.strftime('%d/%m/%Y')})"
    elif periodo == 'mes':
        data_inicio = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        data_fim = None
        titulo_periodo = f"Este Mês ({hoje.strftime('%m/%Y')})"
    elif periodo == 'ano':
        data_inicio = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        data_fim = None
        titulo_periodo = f"Este Ano ({hoje.year})"
    else:
        data_inicio = None
        data_fim = None
        titulo_periodo = "Todo o Período"
    
    # Filtrar movimentações de entrada e saída
    if data_inicio:
        if data_fim:  # Para filtro de dia
            entradas_mov = MovimentacaoEstoque.objects.filter(
                tipo='ENTRADA',
                data_hora__range=[data_inicio, data_fim]
            ).select_related('produto')
            saidas_mov = MovimentacaoEstoque.objects.filter(
                tipo='SAIDA',
                data_hora__range=[data_inicio, data_fim]
            ).select_related('produto')
            # Para produtos cadastrados no período
            produtos_periodo = Produto.objects.filter(
                data_hora__range=[data_inicio, data_fim]
            )
        else:  # Para filtros de mês e ano
            entradas_mov = MovimentacaoEstoque.objects.filter(
                tipo='ENTRADA',
                data_hora__gte=data_inicio
            ).select_related('produto')
            saidas_mov = MovimentacaoEstoque.objects.filter(
                tipo='SAIDA',
                data_hora__gte=data_inicio
            ).select_related('produto')
            # Para produtos cadastrados no período
            produtos_periodo = Produto.objects.filter(
                data_hora__gte=data_inicio
            )
    else:
        entradas_mov = MovimentacaoEstoque.objects.filter(tipo='ENTRADA').select_related('produto')
        saidas_mov = MovimentacaoEstoque.objects.filter(tipo='SAIDA').select_related('produto')
        # Todos os produtos para "Todo o Período"
        produtos_periodo = Produto.objects.all()
    
    # Calcular valores das movimentações
    valor_entradas_mov = sum(mov.quantidade * mov.produto.preco for mov in entradas_mov)
    valor_saidas_mov = sum(mov.quantidade * mov.produto.preco for mov in saidas_mov)
    
    # Calcular valor do estoque inicial dos produtos cadastrados no período
    valor_estoque_inicial = sum(produto.quantidade * produto.preco for produto in produtos_periodo)
    
    # Somar entradas: movimentações + estoque inicial dos produtos cadastrados
    valor_entradas_total = valor_entradas_mov + valor_estoque_inicial
    valor_saidas_total = valor_saidas_mov
    
    # Calcular produtos vencidos (prejuízo)
    hoje = timezone.now().date()
    produtos_vencidos = Produto.objects.filter(
        validade__isnull=False,
        validade__lt=hoje
    )
    valor_prejuizo = sum(produto.quantidade * produto.preco for produto in produtos_vencidos)
    
    # Calcular lucro
    lucro = valor_saidas_total - valor_entradas_total
    
    # Estatísticas de quantidade
    total_entradas_mov = sum(mov.quantidade for mov in entradas_mov)
    total_saidas_mov = sum(mov.quantidade for mov in saidas_mov)
    total_estoque_inicial = sum(produto.quantidade for produto in produtos_periodo)
    
    # Total de entradas = movimentações + estoque inicial
    total_entradas = total_entradas_mov + total_estoque_inicial
    total_saidas = total_saidas_mov
    
    print(f"Período: {periodo}")
    print(f"Entradas mov: {valor_entradas_mov:.2f} ({total_entradas_mov} itens)")
    print(f"Estoque inicial: {valor_estoque_inicial:.2f} ({total_estoque_inicial} itens)")
    print(f"Total entradas: {valor_entradas_total:.2f} ({total_entradas} itens)")
    print(f"Saídas: {valor_saidas_total:.2f} ({total_saidas} itens)")
    
    # Obter usuário logado
    usuario_logado = None
    if 'usuario_logado' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
        except Usuario.DoesNotExist:
            pass
    
    context = {
        'periodo': periodo,
        'titulo_periodo': titulo_periodo,
        'valor_entradas': valor_entradas_total,
        'valor_saidas': valor_saidas_total,
        'lucro': lucro,
        'valor_prejuizo': valor_prejuizo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'data_atual': timezone.now().strftime('%d/%m/%Y %H:%M'),
        'usuario_logado': usuario_logado,
        'data_hora_relatorio': timezone.now()
    }
    
    return render(request, 'balancete.html', context)

# ----- RELATÓRIO FINANCEIRO -----
@login_required_custom
def relatorio_financeiro(request):
    periodo = request.GET.get('periodo')
    
    produtos = Produto.objects.all()
    
    # Filtro por período
    if periodo and periodo.isdigit():
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    # Agrupar produtos por nome, fornecedor e preço (case-insensitive)
    produtos_agrupados = {}
    
    for produto in produtos:
        fornecedor_nome = produto.fornecedor.nome if produto.fornecedor else "Sem fornecedor"
        preco_venda = produto.preco or 0
        # Usar nome, fornecedor e preço para agrupamento
        chave = f"{produto.nome.lower().strip()}_{fornecedor_nome.lower().strip()}_{preco_venda}"
        
        if chave in produtos_agrupados:
            # Somar quantidades
            produtos_agrupados[chave]['quantidade'] += produto.quantidade or 0
        else:
            # Criar novo item agrupado
            produtos_agrupados[chave] = {
                'nome': produto.nome,
                'fornecedor': produto.fornecedor,
                'quantidade': produto.quantidade or 0,
                'unidade': produto.unidade,
                'preco_compra': produto.preco_compra or 0,
                'preco': produto.preco or 0
            }
    
    # Calcular valores financeiros para produtos agrupados
    produtos_financeiros = []
    total_compra = 0
    total_venda = 0
    
    for item in produtos_agrupados.values():
        preco_compra = item['preco_compra']
        preco_venda = item['preco']
        quantidade = item['quantidade']
        
        valor_total_compra = preco_compra * quantidade
        valor_total_venda = preco_venda * quantidade
        lucro_unitario = preco_venda - preco_compra
        lucro_total = lucro_unitario * quantidade
        
        # Criar objeto similar ao produto para o template
        produto_agrupado = type('obj', (object,), {
            'nome': item['nome'],
            'fornecedor': item['fornecedor'],
            'quantidade': quantidade,
            'unidade': item['unidade'],
            'preco_compra': f"{preco_compra:.2f}".replace('.', ','),
            'preco': f"{preco_venda:.2f}".replace('.', ','),
            'valor_total_compra': f"{valor_total_compra:.2f}".replace('.', ','),
            'valor_total_venda': f"{valor_total_venda:.2f}".replace('.', ','),
            'lucro_unitario': f"{lucro_unitario:.2f}".replace('.', ','),
            'lucro_total': f"{lucro_total:.2f}".replace('.', ',')
        })
        
        total_compra += valor_total_compra
        total_venda += valor_total_venda
        
        produtos_financeiros.append(produto_agrupado)
    
    lucro_geral = total_venda - total_compra
    
    # Obter usuário logado
    usuario_logado = None
    if 'usuario_logado' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
        except Usuario.DoesNotExist:
            pass
    
    return render(request, 'relatorio_financeiro.html', {
        'produtos': produtos_financeiros,
        'total_compra': f"{total_compra:.2f}".replace('.', ','),
        'total_venda': f"{total_venda:.2f}".replace('.', ','),
        'lucro_geral': f"{lucro_geral:.2f}".replace('.', ','),
        'periodo': periodo,
        'usuario_logado': usuario_logado,
        'data_hora_relatorio': timezone.now()
    })

# ----- BALANCETE PDF/EMAIL -----
def exportar_balancete_pdf(request):
    periodo = request.GET.get('periodo', 'mes')
    
    from datetime import datetime, timedelta
    hoje = timezone.now().date()
    
    # Definir período de filtro (mesma lógica da view principal)
    if periodo == 'dia':
        data_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        data_fim = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        titulo_periodo = f"Hoje ({hoje.strftime('%d/%m/%Y')})"
    elif periodo == 'mes':
        data_inicio = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        data_fim = None
        titulo_periodo = f"Este Mês ({hoje.strftime('%m/%Y')})"
    elif periodo == 'ano':
        data_inicio = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        data_fim = None
        titulo_periodo = f"Este Ano ({hoje.year})"
    else:
        data_inicio = None
        data_fim = None
        titulo_periodo = "Todo o Período"
    
    # Filtrar movimentações e produtos (mesma lógica da view principal)
    if data_inicio:
        if data_fim:
            entradas_mov = MovimentacaoEstoque.objects.filter(
                tipo='ENTRADA', data_hora__range=[data_inicio, data_fim]
            ).select_related('produto')
            saidas_mov = MovimentacaoEstoque.objects.filter(
                tipo='SAIDA', data_hora__range=[data_inicio, data_fim]
            ).select_related('produto')
            produtos_periodo = Produto.objects.filter(
                data_hora__range=[data_inicio, data_fim]
            )
        else:
            entradas_mov = MovimentacaoEstoque.objects.filter(
                tipo='ENTRADA', data_hora__gte=data_inicio
            ).select_related('produto')
            saidas_mov = MovimentacaoEstoque.objects.filter(
                tipo='SAIDA', data_hora__gte=data_inicio
            ).select_related('produto')
            produtos_periodo = Produto.objects.filter(
                data_hora__gte=data_inicio
            )
    else:
        entradas_mov = MovimentacaoEstoque.objects.filter(tipo='ENTRADA').select_related('produto')
        saidas_mov = MovimentacaoEstoque.objects.filter(tipo='SAIDA').select_related('produto')
        produtos_periodo = Produto.objects.all()
    
    # Calcular valores
    valor_entradas_mov = sum(mov.quantidade * mov.produto.preco for mov in entradas_mov)
    valor_saidas_mov = sum(mov.quantidade * mov.produto.preco for mov in saidas_mov)
    valor_estoque_inicial = sum(produto.quantidade * produto.preco for produto in produtos_periodo)
    
    # Calcular produtos vencidos (prejuízo)
    hoje = timezone.now().date()
    produtos_vencidos = Produto.objects.filter(
        validade__isnull=False,
        validade__lt=hoje
    )
    valor_prejuizo = sum(produto.quantidade * produto.preco for produto in produtos_vencidos)
    
    valor_entradas = valor_entradas_mov + valor_estoque_inicial
    valor_saidas = valor_saidas_mov
    lucro = valor_saidas - valor_entradas
    
    total_entradas_mov = sum(mov.quantidade for mov in entradas_mov)
    total_saidas_mov = sum(mov.quantidade for mov in saidas_mov)
    total_estoque_inicial = sum(produto.quantidade for produto in produtos_periodo)
    
    total_entradas = total_entradas_mov + total_estoque_inicial
    total_saidas = total_saidas_mov
    
    import os
    static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
    
    context = {
        'titulo_periodo': titulo_periodo,
        'valor_entradas': valor_entradas,
        'valor_saidas': valor_saidas,
        'lucro': lucro,
        'valor_prejuizo': valor_prejuizo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'data_atual': timezone.now().strftime('%d/%m/%Y %H:%M'),
        'STATIC_ROOT': static_root
    }
    
    template = get_template('balancete_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="balancete.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    return response

@csrf_exempt
def enviar_balancete_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_destino = data.get('email')
            periodo = data.get('periodo', 'mes')
            
            if not email_destino:
                return JsonResponse({'success': False, 'error': 'Email não informado'})
            
            # Mesma lógica de cálculo do PDF
            hoje = timezone.now().date()
            
            if periodo == 'dia':
                data_inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
                data_fim = timezone.now().replace(hour=23, minute=59, second=59, microsecond=999999)
                titulo_periodo = f"Hoje ({hoje.strftime('%d/%m/%Y')})"
            elif periodo == 'mes':
                data_inicio = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                data_fim = None
                titulo_periodo = f"Este Mês ({hoje.strftime('%m/%Y')})"
            elif periodo == 'ano':
                data_inicio = timezone.now().replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
                data_fim = None
                titulo_periodo = f"Este Ano ({hoje.year})"
            else:
                data_inicio = None
                data_fim = None
                titulo_periodo = "Todo o Período"
            
            if data_inicio:
                if data_fim:
                    entradas_mov = MovimentacaoEstoque.objects.filter(
                        tipo='ENTRADA', data_hora__range=[data_inicio, data_fim]
                    ).select_related('produto')
                    saidas_mov = MovimentacaoEstoque.objects.filter(
                        tipo='SAIDA', data_hora__range=[data_inicio, data_fim]
                    ).select_related('produto')
                    produtos_periodo = Produto.objects.filter(
                        data_hora__range=[data_inicio, data_fim]
                    )
                else:
                    entradas_mov = MovimentacaoEstoque.objects.filter(
                        tipo='ENTRADA', data_hora__gte=data_inicio
                    ).select_related('produto')
                    saidas_mov = MovimentacaoEstoque.objects.filter(
                        tipo='SAIDA', data_hora__gte=data_inicio
                    ).select_related('produto')
                    produtos_periodo = Produto.objects.filter(
                        data_hora__gte=data_inicio
                    )
            else:
                entradas_mov = MovimentacaoEstoque.objects.filter(tipo='ENTRADA').select_related('produto')
                saidas_mov = MovimentacaoEstoque.objects.filter(tipo='SAIDA').select_related('produto')
                produtos_periodo = Produto.objects.all()
            
            valor_entradas_mov = sum(mov.quantidade * mov.produto.preco for mov in entradas_mov)
            valor_saidas_mov = sum(mov.quantidade * mov.produto.preco for mov in saidas_mov)
            valor_estoque_inicial = sum(produto.quantidade * produto.preco for produto in produtos_periodo)
            
            # Calcular produtos vencidos (prejuízo)
            hoje = timezone.now().date()
            produtos_vencidos = Produto.objects.filter(
                validade__isnull=False,
                validade__lt=hoje
            )
            valor_prejuizo = sum(produto.quantidade * produto.preco for produto in produtos_vencidos)
            
            valor_entradas = valor_entradas_mov + valor_estoque_inicial
            valor_saidas = valor_saidas_mov
            lucro = valor_saidas - valor_entradas
            
            total_entradas_mov = sum(mov.quantidade for mov in entradas_mov)
            total_saidas_mov = sum(mov.quantidade for mov in saidas_mov)
            total_estoque_inicial = sum(produto.quantidade for produto in produtos_periodo)
            
            total_entradas = total_entradas_mov + total_estoque_inicial
            total_saidas = total_saidas_mov
            
            import os
            static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
            
            context = {
                'titulo_periodo': titulo_periodo,
                'valor_entradas': valor_entradas,
                'valor_saidas': valor_saidas,
                'lucro': lucro,
                'valor_prejuizo': valor_prejuizo,
                'total_entradas': total_entradas,
                'total_saidas': total_saidas,
                'data_atual': timezone.now().strftime('%d/%m/%Y %H:%M'),
                'STATIC_ROOT': static_root
            }
            
            template = get_template('balancete_pdf.html')
            html = template.render(context)
            
            from io import BytesIO
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
            
            if pisa_status.err:
                return JsonResponse({'success': False, 'error': 'Erro ao gerar PDF'})
            
            pdf_buffer.seek(0)
            
            from django.core.mail import EmailMessage
            email = EmailMessage(
                f'Balancete Financeiro - {titulo_periodo}',
                f'Segue em anexo o balancete financeiro.\n\nResumo:\n- Entradas: R$ {valor_entradas:.2f}\n- Saídas: R$ {valor_saidas:.2f}\n- Lucro: R$ {lucro:.2f}\n\nAtenciosamente,\nEquipe INSUMED',
                settings.DEFAULT_FROM_EMAIL,
                [email_destino]
            )
            email.attach('balancete.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})

def usuarios_cadastrados(request):
    # Verificar se é admin
    if 'admin_logado' not in request.session:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    
    # Buscar TODOS os usuários - sem filtros
    usuarios = Usuario.objects.all().order_by('-id')
    
    return render(request, 'usuarios_cadastrados.html', {
        'usuarios': usuarios
    })

def debug_usuarios_view(request):
    usuarios = Usuario.objects.all().order_by('-id')
    return render(request, 'debug_usuarios.html', {
        'usuarios': usuarios
    })

def exportar_financeiro_pdf(request):
    periodo = request.GET.get('periodo')
    
    produtos = Produto.objects.all()
    
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    # Agrupar produtos por nome, fornecedor e preço
    produtos_agrupados = {}
    
    for produto in produtos:
        fornecedor_nome = produto.fornecedor.nome if produto.fornecedor else "Sem fornecedor"
        preco_venda = produto.preco or 0
        chave = f"{produto.nome.lower().strip()}_{fornecedor_nome.lower().strip()}_{preco_venda}"
        
        if chave in produtos_agrupados:
            produtos_agrupados[chave]['quantidade'] += produto.quantidade or 0
        else:
            produtos_agrupados[chave] = {
                'nome': produto.nome,
                'fornecedor': produto.fornecedor,
                'quantidade': produto.quantidade or 0,
                'unidade': produto.unidade,
                'preco_compra': produto.preco_compra or 0,
                'preco': produto.preco or 0
            }
    
    produtos_financeiros = []
    total_compra = 0
    total_venda = 0
    
    for item in produtos_agrupados.values():
        preco_compra = item['preco_compra']
        preco_venda = item['preco']
        quantidade = item['quantidade']
        
        valor_total_compra = preco_compra * quantidade
        valor_total_venda = preco_venda * quantidade
        lucro_unitario = preco_venda - preco_compra
        lucro_total = lucro_unitario * quantidade
        
        produto_agrupado = type('obj', (object,), {
            'nome': item['nome'],
            'fornecedor': item['fornecedor'],
            'quantidade': quantidade,
            'unidade': item['unidade'],
            'preco_compra': f"{preco_compra:.2f}".replace('.', ','),
            'preco': f"{preco_venda:.2f}".replace('.', ','),
            'valor_total_compra': f"{valor_total_compra:.2f}".replace('.', ','),
            'valor_total_venda': f"{valor_total_venda:.2f}".replace('.', ','),
            'lucro_unitario': f"{lucro_unitario:.2f}".replace('.', ','),
            'lucro_total': f"{lucro_total:.2f}".replace('.', ',')
        })
        
        total_compra += valor_total_compra
        total_venda += valor_total_venda
        
        produtos_financeiros.append(produto_agrupado)
    
    lucro_geral = total_venda - total_compra
    
    import os
    from datetime import datetime
    static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
    
    # Obter usuário logado
    usuario_logado = None
    if 'usuario_logado' in request.session:
        try:
            usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
        except Usuario.DoesNotExist:
            pass
    
    context = {
        'produtos': produtos_financeiros,
        'total_compra': f"{total_compra:.2f}".replace('.', ','),
        'total_venda': f"{total_venda:.2f}".replace('.', ','),
        'lucro_geral': f"{lucro_geral:.2f}".replace('.', ','),
        'periodo': periodo,
        'data_atual': datetime.now().strftime('%d/%m/%Y %H:%M'),
        'usuario_logado': usuario_logado,
        'STATIC_ROOT': static_root
    }
    
    template = get_template('financeiro_pdf.html')
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_financeiro.pdf"'
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    
    return response

@csrf_exempt
def enviar_financeiro_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email_destino = data.get('email')
            periodo = data.get('periodo', '')
            
            if not email_destino:
                return JsonResponse({'success': False, 'error': 'Email não informado'})
            
            produtos = Produto.objects.all()
            
            if periodo and periodo.isdigit():
                from datetime import timedelta
                dias = int(periodo)
                data_limite = timezone.now() - timedelta(days=dias)
                produtos = produtos.filter(data_hora__gte=data_limite)
            
            produtos_financeiros = []
            total_compra = 0
            total_venda = 0
            
            for produto in produtos:
                preco_compra = produto.preco_compra or 0
                preco_venda = produto.preco or 0
                quantidade = produto.quantidade or 0
                
                valor_total_compra = preco_compra * quantidade
                valor_total_venda = preco_venda * quantidade
                lucro_unitario = preco_venda - preco_compra
                lucro_total = lucro_unitario * quantidade
                
                produto.valor_total_compra = f"{valor_total_compra:.2f}".replace('.', ',')
                produto.valor_total_venda = f"{valor_total_venda:.2f}".replace('.', ',')
                produto.lucro_unitario = f"{lucro_unitario:.2f}".replace('.', ',')
                produto.lucro_total = f"{lucro_total:.2f}".replace('.', ',')
                
                total_compra += valor_total_compra
                total_venda += valor_total_venda
                
                produtos_financeiros.append(produto)
            
            lucro_geral = total_venda - total_compra
            
            import os
            from datetime import datetime
            static_root = getattr(settings, 'STATIC_ROOT', None) or os.path.join(settings.BASE_DIR, 'static')
            
            # Obter usuário logado
            usuario_logado = None
            if 'usuario_logado' in request.session:
                try:
                    usuario_logado = Usuario.objects.get(id=request.session['usuario_logado'])
                except Usuario.DoesNotExist:
                    pass
            
            context = {
                'produtos': produtos_financeiros,
                'total_compra': f"{total_compra:.2f}".replace('.', ','),
                'total_venda': f"{total_venda:.2f}".replace('.', ','),
                'lucro_geral': f"{lucro_geral:.2f}".replace('.', ','),
                'periodo': periodo,
                'data_atual': datetime.now().strftime('%d/%m/%Y %H:%M'),
                'usuario_logado': usuario_logado,
                'STATIC_ROOT': static_root
            }
            
            template = get_template('financeiro_pdf.html')
            html = template.render(context)
            
            from io import BytesIO
            pdf_buffer = BytesIO()
            pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)
            
            if pisa_status.err:
                return JsonResponse({'success': False, 'error': 'Erro ao gerar PDF'})
            
            pdf_buffer.seek(0)
            
            from django.core.mail import EmailMessage
            email = EmailMessage(
                'Relatório Financeiro - INSUMED',
                f'Segue em anexo o relatório financeiro.\n\nResumo:\n- Total Compra: R$ {total_compra:.2f}\n- Total Venda: R$ {total_venda:.2f}\n- Lucro Geral: R$ {lucro_geral:.2f}\n\nAtenciosamente,\nEquipe INSUMED',
                settings.DEFAULT_FROM_EMAIL,
                [email_destino]
            )
            email.attach('relatorio_financeiro.pdf', pdf_buffer.getvalue(), 'application/pdf')
            email.send()
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})
# ----- CRIAR PRODUTOS VENCIDOS PARA TESTE -----
def criar_produtos_teste_notificacoes(request):
    from datetime import date
    
    # Buscar ou criar fornecedor
    fornecedor, created = Fornecedor.objects.get_or_create(
        nome="Farmácia Teste",
        defaults={
            'cnpj': '12345678000199',
            'endereco': 'Rua Teste, 123',
            'cidade': 'Cidade Teste',
            'telefone': '(35) 99999-9999',
            'email': 'teste@farmacia.com'
        }
    )
    
    # Produtos vencidos
    produtos_vencidos = [
        {
            'nome': 'Aspirina 500mg VENCIDA',
            'quantidade': 15,
            'unidade': 'Comprimido',
            'preco': 12.50,
            'preco_compra': 8.00,
            'validade': date.today() - timedelta(days=30),
            'descricao': 'Aspirina para dor de cabeça - PRODUTO VENCIDO'
        },
        {
            'nome': 'Dipirona 500mg VENCIDA',
            'quantidade': 8,
            'unidade': 'Comprimido',
            'preco': 15.00,
            'preco_compra': 10.00,
            'validade': date.today() - timedelta(days=15),
            'descricao': 'Dipirona para febre - PRODUTO VENCIDO'
        },
        {
            'nome': 'Xarope Infantil VENCIDO',
            'quantidade': 3,
            'unidade': 'Frasco',
            'preco': 25.00,
            'preco_compra': 18.00,
            'validade': date.today() - timedelta(days=60),
            'descricao': 'Xarope para tosse infantil - PRODUTO VENCIDO'
        },
        {
            'nome': 'Vitamina C VENCIDA',
            'quantidade': 20,
            'unidade': 'Comprimido',
            'preco': 18.00,
            'preco_compra': 12.00,
            'validade': date.today() - timedelta(days=5),
            'descricao': 'Vitamina C 1000mg - PRODUTO VENCIDO'
        }
    ]
    
    produtos_criados = []
    for produto_data in produtos_vencidos:
        produto, created = Produto.objects.get_or_create(
            nome=produto_data['nome'],
            defaults={
                'quantidade': produto_data['quantidade'],
                'unidade': produto_data['unidade'],
                'preco': produto_data['preco'],
                'preco_compra': produto_data['preco_compra'],
                'validade': produto_data['validade'],
                'descricao': produto_data['descricao'],
                'fornecedor': fornecedor
            }
        )
        
        if created:
            produtos_criados.append(produto.nome)
    
    if produtos_criados:
        messages.success(request, f'Produtos vencidos criados: {", ".join(produtos_criados)}')
    else:
        messages.info(request, 'Produtos vencidos já existem no sistema')
    
    return redirect('home')
# ----- DEBUG PRODUTOS VENCIDOS -----
def debug_produtos_vencidos(request):
    from datetime import date
    hoje = date.today()
    
    # Buscar todos os produtos com validade
    produtos_com_validade = Produto.objects.filter(validade__isnull=False).order_by('validade')
    
    debug_info = []
    for produto in produtos_com_validade:
        dias_diff = (hoje - produto.validade).days if produto.validade else 0
        status = "VENCIDO" if produto.validade < hoje else "VÁLIDO"
        
        debug_info.append({
            'nome': produto.nome,
            'validade': produto.validade,
            'dias_diff': dias_diff,
            'status': status
        })
    
    return JsonResponse({
        'hoje': str(hoje),
        'total_produtos_com_validade': len(debug_info),
        'produtos': debug_info
    })