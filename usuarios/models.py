from django.db import models
from django.utils import timezone

class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    senha = models.CharField(max_length=64)

    def __str__(self):
        return self.nome
    