from django.shortcuts import render, redirect
from .models import Fornecedor, Produto, Servico, Cliente, Usuario, Orcamento, MovimentacaoEstoque, RecuperacaoSenha, Suporte, Admin, Notificacao
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

            return redirect('cadastrar_produto')
    else:
        form = ProdutoForm()
    return render(request, 'produtos/cadastrar_produto.html', {
        'form': form,
        'titulo_pagina': 'Cadastro de Produto' 
    })

    

def lista_produtos(request):
    filtro = request.GET.get('filtro')
    periodo = request.GET.get('periodo')
    
    produtos = Produto.objects.all()
    
    # Filtro por busca
    if filtro:
        filtro = filtro.strip()
        print(f"Filtro aplicado: '{filtro}'")  # Debug
        
        if filtro.isdigit() and len(filtro) <= 6:  # IDs normalmente são menores
            produtos = produtos.filter(id=filtro)
            print(f"Busca por ID: {produtos.count()} produtos encontrados")  # Debug
        else:
            produtos = produtos.filter(
                models.Q(nome__icontains=filtro) |
                models.Q(fornecedor__nome__icontains=filtro) |
                models.Q(codigo_barras__icontains=filtro)
            )
            print(f"Busca por texto: {produtos.count()} produtos encontrados")  # Debug
    
    # Filtro por período
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
        print(f"Filtro últimos {dias} dias: {produtos.count()} produtos")  # Debug
    
    produtos = produtos.order_by('nome')
    print(f"Total final: {produtos.count()} produtos")  # Debug

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
            # Tentar filtrar por data no formato dd/mm/yyyy
            try:
                from datetime import datetime
                if '/' in filtro:
                    data_filtro = datetime.strptime(filtro, '%d/%m/%Y').date()
                    orcamentos = orcamentos.filter(data=data_filtro)
                else:
                    orcamentos = orcamentos.filter(cliente__icontains=filtro)
            except ValueError:
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
        print(f"Filtro últimos {dias} dias (desde {data_limite}): {produtos.count()} produtos")  # Debug
    
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
    
    print(f"Total produtos final: {len(produtos_com_movimentacao)}")  # Debug
    return render(request, 'relatorio_estoque.html', {'produtos': produtos_com_movimentacao})

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
                
                # Registrar movimentação
                mov = MovimentacaoEstoque.objects.create(
                    produto=produto,
                    tipo='ENTRADA',
                    quantidade=qtd
                )
                print(f"Movimentação criada: {mov.produto.nome} - ENTRADA - {mov.quantidade} - {mov.data_hora}")
        return redirect('relatorio_entrada')

    return render(request, 'relatorio_entrada.html', {'produtos': produtos_com_entrada})


def relatorio_saida(request):
    periodo = request.GET.get('periodo')
    produtos = Produto.objects.all()
    
    # Filtro por período
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        produtos = produtos.filter(data_hora__gte=data_limite)
    
    # Adicionar informações de última saída
    produtos_com_saida = []
    for produto in produtos:
        ultima_saida = MovimentacaoEstoque.objects.filter(
            produto=produto, tipo='SAIDA'
        ).order_by('-data_hora').first()
        
        produto.ultima_saida = ultima_saida
        produtos_com_saida.append(produto)

    if request.method == "POST":
        produtos = produtos_com_saida  # Usar a lista com informações de saída
        for produto in produtos:
            qtd_retirada = request.POST.get(f"quantidade_{produto.id}")
            if qtd_retirada and int(qtd_retirada) > 0:
                qtd_retirada = int(qtd_retirada)

                if produto.quantidade - qtd_retirada >= 0:
                    produto.quantidade -= qtd_retirada
                    produto.save()
                    
                    # Registrar movimentação
                    mov = MovimentacaoEstoque.objects.create(
                        produto=produto,
                        tipo='SAIDA',
                        quantidade=qtd_retirada
                    )
                    print(f"Movimentação criada: {mov.produto.nome} - SAIDA - {mov.quantidade} - {mov.data_hora}")
                else:
                    messages.error(request, f"O produto {produto.nome} não pode sofrer de retirada por falta de estoque!")

        return redirect("relatorio_saida")

    return render(request, "relatorio_saida.html", {"produtos": produtos_com_saida})

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
            email = form.cleaned_data['email'].strip()
            senha = form.cleaned_data['senha']
            
            # Validação adicional
            if not email or not senha:
                messages.error(request, 'Email e senha são obrigatórios')
                return render(request, 'login.html', {'form': form})
            
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
    print(f"Total de movimentações de entrada: {movimentacoes.count()}")
    for mov in movimentacoes[:5]:  # Mostrar apenas as 5 primeiras
        print(f"Entrada: {mov.produto.nome} - {mov.quantidade} - {mov.data_hora}")
    return render(request, 'relatorio_movimentacao_entrada.html', {'movimentacoes': movimentacoes})

@login_required_custom
def relatorio_movimentacao_saida(request):
    movimentacoes = MovimentacaoEstoque.objects.filter(tipo='SAIDA').select_related('produto', 'produto__fornecedor').order_by('-data_hora')
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

def usuarios_cadastrados(request):
    # Verificar se é admin
    if 'admin_logado' not in request.session:
        messages.error(request, 'Acesso negado. Apenas administradores podem acessar esta página.')
        return redirect('home')
    
    filtro = request.GET.get('filtro')
    periodo = request.GET.get('periodo')
    usuarios = Usuario.objects.all()
    
    # Filtro por busca
    if filtro:
        filtro = filtro.strip()
        if filtro.isdigit():
            usuarios = usuarios.filter(id=filtro)
        else:
            usuarios = usuarios.filter(
                models.Q(nome__icontains=filtro) |
                models.Q(email__icontains=filtro) |
                models.Q(cpf__icontains=filtro) |
                models.Q(telefone__icontains=filtro)
            )
    
    if periodo and periodo.isdigit():
        from datetime import timedelta
        dias = int(periodo)
        data_limite = timezone.now() - timedelta(days=dias)
        # Como não temos campo de data de cadastro, vamos usar o ID como aproximação
        # IDs maiores = cadastros mais recentes
        usuarios_recentes = usuarios.order_by('-id')[:50]  # Pegar os 50 mais recentes
        if dias <= 7:
            usuarios = usuarios_recentes[:10]
        elif dias <= 30:
            usuarios = usuarios_recentes[:25]
        else:
            usuarios = usuarios_recentes
    else:
        usuarios = usuarios.order_by('nome')
    
    return render(request, 'usuarios_cadastrados.html', {
        'usuarios': usuarios,
        'filtro': filtro
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
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def buscar_produto_por_codigo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo_barras = data.get('codigo_barras', '').strip()
            
            print(f"Buscando produto com código: '{codigo_barras}'")  # Debug
            
            if codigo_barras:
                try:
                    # Buscar produto pelo código de barras exato
                    produto = Produto.objects.get(codigo_barras=codigo_barras)
                    print(f"Produto encontrado: {produto.nome}")  # Debug
                    
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
                    print(f"Produto não encontrado com código: '{codigo_barras}'")  # Debug
                    
                    # Tentar buscar por código similar (caso tenha espaços ou caracteres extras)
                    produtos_similares = Produto.objects.filter(codigo_barras__icontains=codigo_barras)
                    if produtos_similares.exists():
                        produto = produtos_similares.first()
                        print(f"Produto similar encontrado: {produto.nome}")  # Debug
                        
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
            print(f"Erro na busca: {str(e)}")  # Debug
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
            from django.core.mail import EmailMessage
            email = EmailMessage(
                f'Orçamento #{orcamento.id} - {orcamento.cliente}',
                f'Segue em anexo o orçamento solicitado.\n\nCliente: {orcamento.cliente}\nData: {orcamento.data.strftime("%d/%m/%Y")}\n\nAtenciosamente,\nEquipe INSUMED',
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
    Notificacao.objects.filter(produto_id=produto_id, tipo=tipo, lida=False).update(lida=True)
    
    try:
        produto = Produto.objects.get(id=produto_id)
    except Produto.DoesNotExist:
        # Criar produto de teste se não existir
        produtos_teste = {
            1: {'nome': 'Medicamento A', 'descricao': 'Medicamento para teste', 'preco': 25.50, 'quantidade': 10},
            2: {'nome': 'Medicamento B', 'descricao': 'Medicamento para teste', 'preco': 35.00, 'quantidade': 15},
            3: {'nome': 'Produto C', 'descricao': 'Produto com estoque crítico', 'preco': 45.00, 'quantidade': 2},
            4: {'nome': 'Produto D', 'descricao': 'Produto com baixa saída', 'preco': 55.00, 'quantidade': 50},
            5: {'nome': 'Insulina Regular', 'descricao': 'Insulina para diabetes', 'preco': 85.00, 'quantidade': 8},
            6: {'nome': 'Soro Fisiológico', 'descricao': 'Soro para hidratação', 'preco': 12.50, 'quantidade': 20},
            7: {'nome': 'Máscara N95', 'descricao': 'Máscara de proteção', 'preco': 8.90, 'quantidade': 1},
            8: {'nome': 'Luvas Cirúrgicas', 'descricao': 'Luvas descartáveis', 'preco': 15.00, 'quantidade': 3},
            9: {'nome': 'Termômetro Digital', 'descricao': 'Termômetro infravermelho', 'preco': 120.00, 'quantidade': 25},
            10: {'nome': 'Estetoscópio', 'descricao': 'Estetoscópio clínico', 'preco': 180.00, 'quantidade': 15}
        }
        
        if produto_id in produtos_teste:
            dados = produtos_teste[produto_id]
            # Criar objeto temporário para o template
            class ProdutoTeste:
                def __init__(self, id, nome, descricao, preco, quantidade):
                    self.id = id
                    self.nome = nome
                    self.descricao = descricao
                    self.preco = preco
                    self.quantidade = quantidade
                    self.data_hora = timezone.now()
                    self.validade = timezone.now().date() + timedelta(days=30 if id <= 2 else 365)
                    self.fornecedor = None
            
            produto = ProdutoTeste(produto_id, dados['nome'], dados['descricao'], dados['preco'], dados['quantidade'])
        else:
            messages.error(request, 'Produto não encontrado')
            return redirect('lista_produtos')
    
    context = {
        'produto': produto,
        'tipo': tipo,
        'mensagem': ''
    }
    
    hoje = timezone.now().date()
    
    if tipo == 'VALIDADE':
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
from datetime import datetime, timedelta

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
            
            # 1. Produtos próximos da validade (60 dias)
            produtos_validade = Produto.objects.filter(
                validade__isnull=False,
                validade__lte=hoje + timedelta(days=60)
            )[:10]
            
            # 2. Produtos com estoque crítico (≤ 5 unidades)
            produtos_criticos = Produto.objects.filter(quantidade__lte=5)[:10]
            
            # 3. Produtos com baixa saída (90 dias sem movimentação)
            data_limite = timezone.now() - timedelta(days=90)
            produtos_sem_saida = Produto.objects.filter(data_hora__lt=data_limite)[:10]
            
            tipo_filtro = request.GET.get('tipo')
            
            if tipo_filtro == 'VALIDADE':
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
    
    context = {
        'produtos': produtos_com_movimentacao,
        'busca': busca,
        'data_atual': datetime.now().strftime('%d/%m/%Y %H:%M'),
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
            busca = data.get('busca', '')
            periodo = data.get('periodo', '')
            
            if not email_destino:
                return JsonResponse({'success': False, 'error': 'Email não informado'})
            
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
            
            context = {
                'produtos': produtos_com_movimentacao,
                'busca': busca,
                'data_atual': datetime.now().strftime('%d/%m/%Y %H:%M'),
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

# ----- BALANCETE -----
@login_required_custom
def balancete(request):
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
    
    context = {
        'periodo': periodo,
        'titulo_periodo': titulo_periodo,
        'valor_entradas': valor_entradas_total,
        'valor_saidas': valor_saidas_total,
        'lucro': lucro,
        'valor_prejuizo': valor_prejuizo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'data_atual': timezone.now().strftime('%d/%m/%Y %H:%M')
    }
    
    return render(request, 'balancete.html', context)

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
    
    usuarios = Usuario.objects.all().order_by('nome')
    
    return render(request, 'usuarios_cadastrados.html', {
        'usuarios': usuarios
    })