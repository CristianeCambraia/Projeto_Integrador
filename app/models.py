from django.db import models

# Create your models here.
class Fornecedor(models.Model):
    nome = models.CharField(max_length=200)
    cnpj = models.IntegerField()
    endereco = models.CharField(max_length=200)
    bairro = models.CharField(max_length=200)
    complemento = models.CharField(max_length=200)
    data_nascimento = models.IntegerField()
    cidade = models.CharField(max_length=200)
    uf = models.CharField(max_length=2)
    cep = models.IntegerField()
    email = models.CharField(max_length=200)
    telefone = models.IntegerField()
