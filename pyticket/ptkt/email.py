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