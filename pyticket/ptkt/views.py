from django.shortcuts import render, redirect
from ptkt.models import Tickets, Interacoes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404
from django.http import JsonResponse

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
    ticket = Tickets.objects.filter(usuario=username)
    dados = {'tickets': ticket}
    return render(request, 'tickets.html', dados)

@login_required(login_url='/login/')
def ticket(request):
    id_ticket = request.GET.get('id')
    dados = {}
    if id_ticket:
        dados['ticket'] = Tickets.objects.get(id=id_ticket)
    return render(request, 'ticket.html', dados)
