from django.db import models

class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=20)  # Usar CharField pois pode conter caracteres especiais
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200, blank=True, null=True)  # Pode ser opcional
    data_nascimento = models.DateField()
    cidade = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=10)  # Também CharField por conta do formato
    email = models.EmailField(max_length=200)  # Melhor usar EmailField para validação
    telefone = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    descricao = models.TextField(blank=True, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, related_name="produtos")

    def __str__(self):
        return f"{self.nome} - R${self.preco}"
