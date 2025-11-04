def usuario_logado(request):
    try:
        context = {
            'usuario_logado': 'usuario_logado' in request.session,
            'admin_logado': 'admin_logado' in request.session,
            'notificacoes_count': 0
        }
        return context
    except Exception:
        return {
            'usuario_logado': False,
            'admin_logado': False,
            'notificacoes_count': 0
        }