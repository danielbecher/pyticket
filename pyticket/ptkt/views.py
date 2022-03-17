from django.shortcuts import render, redirect
from ptkt.models import Tickets, Interacoes, User, Notificacoes
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime
from django.http.response import Http404
from threading import Thread

#seta url
urlAdmin = "http://pyticket.becher.com.br"
emailAssuntosUsuarios = ["Alerta de novo ticket criado", "Você criou um novo ticket e em breve ele será analisado por alguém do suporte. Para acompanhar, acesse http://pyticket.becher.com.br", "Seu ticket recebeu uma resposta", "Seu ticket foi respondido, é possível que você precise respondê-lo ou encerrá-lo. Para verificar, acesse http://pyticket.becher.com.br",
                "Ticket encerrado", "Seu ticket foi encerrado. Para visualizar o histórico, acesse http://pyticket.becher.com.br"]

emailAssuntosStaffs = ["Alerta de novo ticket criado", "Um usuário abriu um ticket. Acesse o painel de administração e verifique", "Um ticket foi respondido", "Um usuário respondeu um ticket. Acesse o painel de administração e verifique", "Ticket encerrado", "Um ticket foi encerrado. Para visualizar o histórico, acesse o painel de administração"]

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

#Aqui não usaremos decorador por motivos óbvios, é a criação de usuários
def criar_usuario(request):        
    return render(request, 'criarusuario.html')

def criar_usuario_submit(request):
    if request.POST:
        criausername = request.POST.get('usuario')
        criapassword = request.POST.get('senha')
        criaemail = request.POST.get('email')
        criafirstname = request.POST.get('primeironome')
        crialastname = request.POST.get('ultimonome')
        novoUsuario = User.objects.create_user(username=criausername,
                            password=criapassword,
                            email=criaemail,
                            first_name=criafirstname,
                            last_name=crialastname)
        novoUsuario.save()

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
    pegaEmailStaffs()
    usuario = request.user
    if usuario.is_staff:
        ticket = Tickets.objects.all().order_by('-data_abertura').order_by('prioridade')
        ticketf = Tickets.objects.filter(status="Fechado").order_by('-data_abertura')[:5]
        dados = {'tickets': ticket,
                'ticketsf': ticketf}
        return render(request, 'tickets.html', dados)
    else:
        ticket = Tickets.objects.filter(usuario_id=usuario)
        ticketf = Tickets.objects.filter(status="Fechado").order_by('-data_abertura')[:5]
        dados = {'tickets': ticket,
                'ticketsf': ticketf}
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

@login_required(login_url='/login/')
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
                                  prioridade=prioridade,
                                  status = status)      
    
    staffs = pegaEmailStaffs()
    for staff in staffs:
        tn1 = Thread(target=notificaMail, args=(emailAssuntosStaffs[1],emailAssuntosStaffs[0],staff))
        tn1.start()
    tn2 = Thread(target=notificaMail, args=(emailAssuntosUsuarios[1], emailAssuntosUsuarios[0],usuario.email))
    tn2.start()
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
        ti1 = Thread(target=notificaMail, args=(emailAssuntosUsuarios[3], emailAssuntosUsuarios[2], email))
        ti1.start()
    
    staffs = pegaEmailStaffs()
    for staff in staffs:
        ti2 = Thread(target=notificaMail, args=(emailAssuntosStaffs[3], emailAssuntosStaffs[2],staff))
        ti2.start()
    
    return redirect('/')

@login_required(login_url='/login/')
def ticket_delete(request, id_ticket):
    usuario = request.user
    try:
        ticket = Tickets.objects.get(id=id_ticket)
    except Exception:
        raise Http404()
    if usuario == ticket.usuario or usuario.is_staff:
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
        tf1 = Thread(target=notificaMail, args=(emailAssuntosUsuarios[5], emailAssuntosUsuarios[4],email))
        tf1.start()

    staffs = pegaEmailStaffs()
    for staff in staffs:
        tf2 = Thread(target=notificaMail, args=(emailAssuntosUsuarios[5], emailAssuntosUsuarios[4],staff))
        tf2.start()

    return redirect('/')

@login_required(login_url='/login/')
def ticket_abre(request):
    ticketid = request.GET.get('id')
    ticket = Tickets.objects.get(id=ticketid)
    if ticketid:
        ticket.status = "Aberto"
        ticket.save()
    return redirect('/')

#############################################
### Funções sem rota
#############################################
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
        useradd = usuarios.id_usuario
        if useradd not in usuariosInteracoes:
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

def pegaEmailStaffs():
    staffs = []
    usuarios = User.objects.all().filter(is_staff=True)
    for user in usuarios:
        if user not in staffs:
            staffs.append(user.email)
            
    return staffs
    

def notificaMail(msg,subj,destinatario):
    conexao = Notificacoes.objects.get()
    host = conexao.host
    usuario = conexao.usuario
    senha = conexao.senha
    porta = conexao.porta
    server = smtplib.SMTP(host,porta)
    server.ehlo()
    server.starttls()
    server.login(usuario, senha)
    message = msg
    subject = subj
    email_msg = MIMEMultipart()
    email_msg['From'] = usuario
    email_msg['To'] = destinatario
    email_msg['Subject'] = subject
    email_msg.attach(MIMEText(message, 'plain'))
    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())
    server.quit()