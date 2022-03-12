from django.contrib import admin
from ptkt.models import Tickets, Interacoes

class ticketsAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'assunto', 'status', 'prioridade', 'data_abertura')

class interacoesAdmin(admin.ModelAdmin):
    list_display = ('id_usuario','data_criacao', 'interacao', 'chamado_id')

admin.site.register(Tickets, ticketsAdmin)
admin.site.register(Interacoes, interacoesAdmin)
