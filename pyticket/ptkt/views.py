from re import I
from django.shortcuts import render, redirect
from ptkt.models import Tickets, Interacoes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        username = request.POST.get('usuario')
        password = request.POST.get('senha')
        loga = authenticate(username=username, password=password)
        if loga is not None:
            login(request, loga)
            return redirect('/tickets/')
        else:
            messages.error(request, "Usuário ou senha inválidos!")
    return redirect('/')

@login_required(login_url='/login/')
def tickets(request):
    id_tickets = request.GET.get('id')
    dados = {}
    dados2 = {}
    if id_tickets:
        dados['tickets'] = Tickets.objects.get(id=id_tickets)
    return render(request, 'ticket.html', dados)

def logout_user(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login/')
def tickets_list(request):
    username = request.user
    data_atual = datetime.now()
    ticket = Tickets.objects.all()
    dados = {'tickets': ticket}
    return render(request, 'tickets.html', dados)

@login_required(login_url='/login/')
def ticket(request):
    id_ticket = request.GET.get('id')
    dados = {}
    if id_ticket:
        dados = {'ticket': Tickets.objects.get(id=id_ticket), 'interacoes': Interacoes.objects.filter(chamado_id=id_ticket)}
        
    return render(request, 'ticket.html', dados)

@login_required(login_url='/login/')
def ticket_submit(request):
    if request.POST:
        usuario = request.user
        assunto = request.POST.get('assunto')
        descricao = request.POST.get('descricao')
        status = request.POST.get('status')
        data_abertura = datetime.now()
        prioridade = request.POST.get('prioridade')
        id_ticket = request.POST.get('id_ticket')
        if id_ticket:
            ticket = Tickets.objects.get(id=id_ticket)
            if ticket.usuario == usuario:
                ticket.assunto = assunto
                ticket.descricao = descricao
                ticket.status = status
                ticket.prioridade = prioridade
                ticket.save()
        else:
            Tickets.objects.create(assunto=assunto,
                                  data_abertura=data_abertura,
                                  descricao=descricao,
                                  usuario=usuario,
                                  prioridade = prioridade,
                                  status = status)        
    return redirect('/')

def ticket_criar(request):        
    return render(request, 'criarticket.html')

@login_required(login_url='/login/')
def ticket_criar_submit(request):
    usuario = request.user
    assunto = request.POST.get('assunto')
    descricao = request.POST.get('descricao')
    status = "Aberto"
    data_abertura = datetime.now()
    prioridade = request.POST.get('prioridade')
    Tickets.objects.create(assunto=assunto,
                                  data_abertura=data_abertura,
                                  descricao=descricao,
                                  usuario=usuario,
                                  prioridade = prioridade,
                                  status = status)      
    return redirect('/')

@login_required(login_url='/login/')
def interacao_submit(request):
    usuario = request.user
    id_ticket = request.POST.get('id_ticket')
    resposta = request.POST.get('resposta')
    Interacoes.objects.create(id_usuario=usuario,
                                chamado_id=id_ticket,
                                interacao=resposta)
    ticket_aguarda(id_ticket)
    return redirect('/')

@login_required(login_url='/login/')
def ticket_delete(request, id_ticket):
    usuario = request.user
    try:
        ticket = Tickets.objects.get(id=id_ticket)
    except Exception:
        raise Http404()
    if usuario == ticket.usuario:
        ticket.delete()
    else:
        raise Http404()
    return redirect('/')

@login_required(login_url='/login/')
def ticket_fecha(request):
    ticketid = request.GET.get('id')
    ticket = Tickets.objects.get(id=ticketid)
    if ticketid:
        ticket.status = "Fechado"
        ticket.save()
    return redirect('/')

@login_required(login_url='/login/')
def ticket_abre(request):
    ticketid = request.GET.get('id')
    ticket = Tickets.objects.get(id=ticketid)
    if ticketid:
        ticket.status = "Aberto"
        ticket.save()
    return redirect('/')


#Funções sem rota
def ticket_aguarda(id):
    ticket = Tickets.objects.get(id=id)
    if id:
        ticket.status = "Aguardando"
        ticket.save()
