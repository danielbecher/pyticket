from django.shortcuts import render, redirect
from ptkt.models import Tickets, Interacoes, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404

urlAdmin = "http://localhost:8000"
emailAssuntoCriacao = "Alerta de novo ticket criado"

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
    usuario = request.user
    data_atual = datetime.now()
    ticket = Tickets.objects.filter(usuario_id=usuario)
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
    
    notificaMail("O usuário {} criou um ticket com a prioridade {}. Veja aqui mesmo este ticket: {}".format(usuario, prioridade, urlAdmin), emailAssuntoCriacao, "daniel@becher.com.br")
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
    emailsnotify = pegaEmails(id_ticket)
    for email in emailsnotify:
        notificaMail("Olá! Tem uma nova interação para o seu ticket número {}. Para ler e responder, acesse: {}".format(id_ticket, "https://localhost:8000/"), "Aviso de movimentação de ticket", email)
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
    
    emailsnotify = pegaEmails(ticketid)
    for email in emailsnotify:
        notificaMail("Olá! O seu ticket foi fechado! Caso precise de algo mais é só abrir um novo ticket. Para acompanhar o histórico deste ticket ou abrir um novo, acesse: {}".format(urlAdmin), "Aviso de movimentação de ticket", email)

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



#Notificações por e-mail
#Faz a notificação de que um link foi gerado, ou um erro aconteceu.
import smtplib
from django.shortcuts import render
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def view_a(request):
    return render(request, 'view_a.html')

def pegaEmails(idticket):
    ticket = Tickets.objects.get(id=idticket)
    interacoes = Interacoes.objects.filter(chamado_id=idticket)
    usuariosInteracoes = []
    emailsinteracoes = []

    for usuarios in interacoes:
        if usuarios not in usuariosInteracoes:
            usuariosInteracoes.append(usuarios.id_usuario)
    
    for usr in usuariosInteracoes:
        if usr not in emailsinteracoes:
            emailsinteracoes.append(pegaUsuario(usr))
    
    if pegaUsuario(ticket.usuario) not in emailsinteracoes:
        emailsinteracoes.append(pegaUsuario(ticket.usuario))

    return emailsinteracoes
    
def pegaUsuario(user):
    usuario = User.objects.get(username=user)
    email = usuario.email
    return email
    

def notificaMail(msg,subj,destinatario):
    senha = conectMail()
    host = 'smtp.gmail.com'
    port = 587
    user = 'ti@sotepa.com.br'
    server = smtplib.SMTP(host,port)

    server.ehlo()
    server.starttls()
    server.login(user, senha)

    message = msg
    subject = subj
    email_msg = MIMEMultipart()
    email_msg['From'] = user
    email_msg['To'] = destinatario
    email_msg['Subject'] = subject

    email_msg.attach(MIMEText(message, 'plain'))

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()

def conectMail():
    mailPass = ''
    return mailPass