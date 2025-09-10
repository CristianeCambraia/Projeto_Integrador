from django import forms
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = [
            'nome', 'cnpj', 'endereco', 'bairro', 'complemento',
            'data_nascimento', 'cidade', 'uf', 'cep', 'email', 'telefone'
        ]

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'cnpj': forms.TextInput(attrs={'placeholder': 'CNPJ'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço'}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Bairro'}),
            'complemento': forms.TextInput(attrs={'placeholder': 'Complemento'}),
            'data_nascimento': forms.DateInput(attrs={'placeholder': 'Data de Nascimento', 'type': 'date'}),
            'cidade': forms.TextInput(attrs={'placeholder': 'Cidade'}),
            'uf': forms.TextInput(attrs={'placeholder': 'UF'}),
            'cep': forms.TextInput(attrs={'placeholder': 'CEP'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Telefone'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
