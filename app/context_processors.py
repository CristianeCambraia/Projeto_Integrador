def usuario_logado(request):
    return {
        'usuario_logado': 'usuario_logado' in request.session,
        'admin_logado': 'admin_logado' in request.session
    }