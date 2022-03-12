from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Tickets(models.Model):
    #Definindo as escolhas de prioridades
    prioridadesChoices = (
        ('1', 'Baixa'),
        ('2', 'Média'),
        ('3', 'Alta'),
    )

    assunto = models.CharField(max_length=300, blank=False, null=False)
    descricao = models.TextField(blank=False, null=False)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_abertura = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20)
    prioridade = models.CharField(max_length=1, choices=prioridadesChoices) #prioridades setadas na tupla prioridadesChoices
    anexo = models.FileField(upload_to ='uploads/', blank=True, null=True)

    def __str__(self):
        return self.assunto

    def get_data_ticket(self):
        return self.data_abertura.strftime('%d/%m/%Y')

    def get_hora_ticket(self):
        return self.data_abertura.strftime('%H:%M')

    def get_data_hora_ticket(self):
        return self.data_abertura.strftime('%Y-%m-%d %H:%M')


class Interacoes(models.Model):
    id_usuario = models.CharField(max_length=50, null=False)
    interacao = models.TextField(blank=False, null=False)
    data_criacao = models.DateTimeField(auto_now=True)
    chamado = models.ForeignKey(Tickets, on_delete=models.CASCADE)
    anexo = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return self.chamado