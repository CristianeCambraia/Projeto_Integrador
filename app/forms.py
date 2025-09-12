from django import forms
from .models import Fornecedor, Produto

# Formulário de Fornecedor
class FornecedorForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],  # aceita formato ISO e BR
        widget=forms.DateInput(attrs={'placeholder': 'Data de Nascimento', 'type': 'date'})
    )

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
            # 'data_nascimento': já declarado acima
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


# Formulário de Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'preco', 'descricao', 'fornecedor']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do Produto'}),
            'preco': forms.NumberInput(attrs={'placeholder': 'Preço'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição', 'rows': 3}),
            'fornecedor': forms.Select(attrs={'placeholder': 'Selecione o Fornecedor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''

            
