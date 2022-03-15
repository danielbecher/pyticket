from django.contrib import admin
from ptkt.models import Tickets, Interacoes
from pyticket.ptkt.models import Notificacoes

class ticketsAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'assunto', 'status', 'prioridade', 'data_abertura')

class interacoesAdmin(admin.ModelAdmin):
    list_display = ('id_usuario','data_criacao', 'interacao', 'chamado_id')

class notificacoesAdmin(admin.ModelAdmin):
    list_display = ('host','porta','usuario','senha')

admin.site.register(Tickets, ticketsAdmin)
admin.site.register(Interacoes, interacoesAdmin)
admin.site.register(Notificacoes, notificacoesAdmin)
