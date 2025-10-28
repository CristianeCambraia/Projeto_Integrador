# ----- MINHA CONTA -----
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usuario
from .decorators import login_required_custom

@login_required_custom
def minha_conta(request):
    usuario_id = request.session.get('usuario_logado')
    usuario = Usuario.objects.get(id=usuario_id)
    return render(request, 'minha_conta.html', {'usuario': usuario})

@login_required_custom
def editar_conta(request):
    usuario_id = request.session.get('usuario_logado')
    usuario = Usuario.objects.get(id=usuario_id)
    
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        email = request.POST.get('email', '').strip()
        telefone = request.POST.get('telefone', '').strip()
        endereco = request.POST.get('endereco', '').strip()
        cidade = request.POST.get('cidade', '').strip()
        nova_senha = request.POST.get('nova_senha', '').strip()
        confirmar_senha = request.POST.get('confirmar_senha', '').strip()
        
        # Validações básicas
        if not nome or not email:
            messages.error(request, 'Nome e email são obrigatórios')
            return render(request, 'editar_conta.html', {'usuario': usuario})
        
        # Verificar se email já existe (exceto o próprio usuário)
        if Usuario.objects.filter(email=email).exclude(id=usuario.id).exists():
            messages.error(request, 'Este email já está sendo usado por outro usuário')
            return render(request, 'editar_conta.html', {'usuario': usuario})
        
        # Validar senha se fornecida
        if nova_senha:
            if nova_senha != confirmar_senha:
                messages.error(request, 'As senhas não coincidem')
                return render(request, 'editar_conta.html', {'usuario': usuario})
            if len(nova_senha) < 6:
                messages.error(request, 'A senha deve ter pelo menos 6 caracteres')
                return render(request, 'editar_conta.html', {'usuario': usuario})
        
        # Atualizar dados
        usuario.nome = nome
        usuario.email = email
        usuario.telefone = telefone
        usuario.endereco = endereco
        usuario.cidade = cidade
        
        if nova_senha:
            usuario.senha = nova_senha
        
        usuario.save()
        messages.success(request, 'Dados atualizados com sucesso!')
        return redirect('editar_conta')
    
    return render(request, 'editar_conta.html', {'usuario': usuario})