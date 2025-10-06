from django.shortcuts import redirect
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'usuario_logado' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper