from django import forms
from .models import Fornecedor, Produto, Servico, Cliente, Usuario, Suporte, Admin
from django.contrib.auth.forms import AuthenticationForm
from .models import Usuario  # ou de onde vier seu modelo de usuário
class SuporteForm(forms.ModelForm):
    class Meta:
        model = Suporte
        fields = ["nome", "telefone", "email", "descreva"]
        widgets = {
            'telefone': forms.TextInput(attrs={'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'}),
        }

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
            'telefone': forms.TextInput(attrs={'placeholder': 'Telefone', 'pattern': '[0-9]*', 'inputmode': 'numeric', 'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
        
        # Preencher data de nascimento ao editar
        if self.instance and hasattr(self.instance, 'data_nascimento') and self.instance.data_nascimento:
            self.initial['data_nascimento'] = self.instance.data_nascimento


# Formulário de Produto
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'codigo_barras', 'preco', 'preco_compra', 'descricao', 'fornecedor', 'unidade', 'quantidade', 'validade', 'observacao']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do Produto'}),
            'codigo_barras': forms.TextInput(attrs={'placeholder': 'Escaneie ou digite o código de barras...', 'id': 'codigo_barras'}),
            'preco': forms.NumberInput(attrs={'placeholder': 'Preço de Venda'}),
            'preco_compra': forms.NumberInput(attrs={'placeholder': 'Preço de Compra'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição', 'rows': 4}),
            'fornecedor': forms.Select(),
            'unidade': forms.Select(),
            'quantidade': forms.NumberInput(attrs={'placeholder': 'Quantidade', 'min': '0'}),
            'validade': forms.DateInput(attrs={'type': 'date'}),
            'observacao': forms.Textarea(attrs={'placeholder': 'Observações', 'rows': 4})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar apenas fornecedores ativos
        try:
            self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)
            self.fields['fornecedor'].empty_label = 'Selecione o Fornecedor'
        except:
            pass


# Formulário de Serviço
class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'preco', 'descricao', 'fornecedor', 'unidade', 'quantidade', 'observacao']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do Serviço'}),
            'preco': forms.NumberInput(attrs={'placeholder': 'Preço'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição', 'rows': 4, 'style': 'width: 100%; grid-column: 1 / -1;'}),
            'fornecedor': forms.Select(attrs={'placeholder': 'Selecione o Fornecedor'}),
            'unidade': forms.Select(attrs={'placeholder': 'Selecione a Cobrança'}),
            'quantidade': forms.NumberInput(attrs={'placeholder': 'Quantidade', 'min': '0'}),
            'observacao': forms.Textarea(attrs={'placeholder': 'Observações', 'rows': 4, 'style': 'width: 100%; grid-column: 1 / -1;'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
        
        # Definir campos obrigatórios
        self.fields['nome'].required = True
        self.fields['preco'].required = True
        self.fields['unidade'].required = True
        self.fields['descricao'].required = False
        self.fields['quantidade'].required = False
        self.fields['observacao'].required = False
        
        # Mostrar apenas fornecedores ativos
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)
        self.fields['fornecedor'].required = False
        if not Fornecedor.objects.filter(ativo=True).exists():
            self.fields['fornecedor'].empty_label = 'Nenhum fornecedor ativo'
        else:
            self.fields['fornecedor'].empty_label = 'Fornecedor'


# Formulário de Cliente
class ClienteForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],  # aceita formato ISO e BR
        widget=forms.DateInput(attrs={'placeholder': 'Data de Nascimento', 'type': 'date'}, format='%Y-%m-%d')
    )

    class Meta:
        model = Cliente
        fields = [
            'nome', 'cpf', 'endereco', 'bairro', 'complemento',
            'data_nascimento', 'cidade', 'uf', 'cep', 'email', 'telefone'
        ]

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'CPF'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço'}),
            'bairro': forms.TextInput(attrs={'placeholder': 'Bairro'}),
            'complemento': forms.TextInput(attrs={'placeholder': 'Complemento'}),
            # 'data_nascimento': já declarado acima
            'cidade': forms.TextInput(attrs={'placeholder': 'Cidade'}),
            'uf': forms.TextInput(attrs={'placeholder': 'UF'}),
            'cep': forms.TextInput(attrs={'placeholder': 'CEP'}),
            'email': forms.EmailInput(attrs={'placeholder': 'E-mail'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Telefone', 'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
        
        # Preservar valor da data de nascimento ao editar
        if self.instance and self.instance.pk and self.instance.data_nascimento:
            self.fields['data_nascimento'].widget.attrs['value'] = self.instance.data_nascimento.strftime('%Y-%m-%d')


# Formulário de Usuário
class UsuarioForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        widget=forms.DateInput(attrs={'placeholder': 'Data de Nascimento', 'type': 'date'}),
        label='Data de Nascimento'
    )

    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Senha'})
    )

    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'cpf', 'endereco', 'telefone', 'data_nascimento', 'senha']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'cpf': forms.TextInput(attrs={'placeholder': 'CPF', 'maxlength': '14', 'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57', 'oninput': r'this.value = this.value.replace(/\D/g, "").replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4").substring(0, 14)'}),
            'endereco': forms.TextInput(attrs={'placeholder': 'Endereço'}),
            'telefone': forms.TextInput(attrs={'placeholder': 'Telefone', 'onkeypress': 'return event.charCode >= 48 && event.charCode <= 57', 'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'}),
            # 'data_nascimento' e 'senha' já declarados acima
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'data_nascimento':
                field.label = ''



class LoginForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'E‑mail',
            'class': 'form-control',
            'required': True
        })
    )
    senha = forms.CharField(
        required=True,
        min_length=1,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha',
            'class': 'form-control',
            'required': True
        })
    )
    remember = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Email é obrigatório')
        return email.strip()
    
    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if not senha:
            raise forms.ValidationError('Senha é obrigatória')
        return senha
 
# Formulário para editar produto (sem preço, quantidade e unidade)
class EditarProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'fornecedor']

        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome do Produto'}),
            'descricao': forms.Textarea(attrs={'placeholder': 'Descrição', 'rows': 3}),
            'fornecedor': forms.Select(attrs={'placeholder': 'Selecione o Fornecedor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label = ''
        # Mostrar apenas fornecedores ativos
        self.fields['fornecedor'].queryset = Fornecedor.objects.filter(ativo=True)

class RecuperarSenhaForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Digite seu e-mail',
            'class': 'form-control'
        })
    )

class VerificarCodigoForm(forms.Form):
    codigo = forms.CharField(
        max_length=6,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite o código de 6 dígitos',
            'class': 'form-control'
        })
    )

class NovaSenhaForm(forms.Form):
    nova_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Nova senha',
            'class': 'form-control'
        })
    )
    confirmar_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a nova senha',
            'class': 'form-control'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        nova_senha = cleaned_data.get('nova_senha')
        confirmar_senha = cleaned_data.get('confirmar_senha')
        
        if nova_senha and confirmar_senha and nova_senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem')
        
        return cleaned_data

class AdminLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'E‑mail Admin',
            'class': 'form-control'
        })
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha Admin',
            'class': 'form-control'
        })
    )