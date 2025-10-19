def usuario_logado(request):
    from .models import Notificacao
    
    context = {
        'usuario_logado': 'usuario_logado' in request.session,
        'admin_logado': 'admin_logado' in request.session
    }
    
    # Adicionar contador de notificações se usuário estiver logado
    if 'usuario_logado' in request.session:
        try:
            notificacoes_count = Notificacao.objects.filter(lida=False).count()
            context['notificacoes_count'] = notificacoes_count
        except:
            context['notificacoes_count'] = 0
    
    return context