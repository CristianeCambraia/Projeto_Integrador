from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'usuario_logado' not in request.session:
            return redirect('login')
        
        # Verificar se o usuário ainda está ativo
        try:
            from .models import Usuario
            usuario_id = request.session['usuario_logado']
            usuario = Usuario.objects.get(id=usuario_id)
            
            if not usuario.ativo:
                # Limpar sessão e redirecionar para login
                del request.session['usuario_logado']
                messages.error(request, 'Usuário bloqueado. Entre em contato com o administrador.')
                return redirect('login')
        except Usuario.DoesNotExist:
            # Usuário não existe mais, limpar sessão
            del request.session['usuario_logado']
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    return wrapper