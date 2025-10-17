from datetime import date
from django.utils import timezone

# Ajuste o email/senha abaixo conforme desejar
EMAIL = 'admin@insumed.local'
SENHA = 'admin123'

try:
    from app.models import Usuario

    usuario, created = Usuario.objects.get_or_create(
        email=EMAIL,
        defaults={
            'nome': 'Administrador',
            'cpf': '00000000000',
            'endereco': 'Sede',
            'telefone': '0000000000',
            'data_nascimento': date(1990, 1, 1),
            'senha': SENHA,
            'is_admin': True,
        }
    )

    if not created:
        usuario.is_admin = True
        usuario.senha = SENHA
        usuario.save()
        print(f'Usuário existente atualizado como admin: {usuario.email} (id={usuario.id})')
    else:
        print(f'Usuário admin criado: {usuario.email} (id={usuario.id})')

except Exception as e:
    print('Erro ao criar/atualizar usuário admin:', e)
