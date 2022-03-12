from django.contrib import admin
from ptkt.models import Tickets

class ticketsAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'assunto', 'status', 'prioridade', 'data_abertura')

admin.site.register(Tickets, ticketsAdmin)
