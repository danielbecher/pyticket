from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Interacoes(models.Model):
    id_usuario = models.CharField(max_length=50, null=False)
    interacao = models.TextField(blank=False, null=False)
    data_criacao = models.DateTimeField(auto_now=True)
    anexo = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.id_usuario

class Tickets(models.Model):
    #Definindo as escolhas de prioridades
    prioridadesChoices = (
        ('1', 'Baixa'),
        ('2', 'Média'),
        ('3', 'Alta'),
    )

    assunto = models.CharField(max_length=300, blank=False, null=False)
    descricao = models.TextField(blank=False, null=False)
    interacao = models.ForeignKey(Interacoes, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_abertura = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
    prioridade = models.CharField(max_length=1, choices=prioridadesChoices) #prioridades setadas na tupla prioridadesChoices
    anexo = models.FileField(upload_to ='uploads/')

    def __str__(self):
        return self.assunto