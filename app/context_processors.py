def usuario_logado(request):
    try:
        from .models import Usuario
        context = {
            'admin_logado': 'admin_logado' in request.session,
            'notificacoes_count': 0
        }
        
        if 'usuario_logado' in request.session:
            try:
                usuario = Usuario.objects.get(id=request.session['usuario_logado'])
                context['usuario_logado'] = usuario
            except Usuario.DoesNotExist:
                context['usuario_logado'] = None
        else:
            context['usuario_logado'] = None
            
        return context
    except Exception:
        return {
            'usuario_logado': None,
            'admin_logado': False,
            'notificacoes_count': 0
        }