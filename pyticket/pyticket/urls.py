"""pyticket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ptkt import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/tickets')),
    path('admin/', admin.site.urls),
    path('login/', views.login_user ),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('tickets/', views.tickets_list),
    path('tickets/ticket/', views.ticket),
    path('tickets/ticket/submit', views.ticket_submit),
    path('tickets/ticket/submit2', views.ticket_submit2),
    path('tickets/ticket/delete/<int:id_ticket>/', views.ticket_delete),
    path('tickets/fecha/', views.ticket_fecha),
    path('tickets/abre/', views.ticket_abre)
]
