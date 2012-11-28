# -*- coding: utf-8 -*-

from models import *
import datetime
from django.http import HttpResponse, HttpRequest
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def custom_render(request, template, context={}):
    context['request'] = request
    return render_to_response(template, context, context_instance=RequestContext(request))

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("dashboard")
    else:
        return custom_render(request, "index.html")

def ulogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("dashboard")
            else:
                message = " A tua conte foi desactivada"
        else:
            message = "User ou password inválidos"

        return custom_render(request, "index.html", {"message": message})
    else: 
        return HttpResponseRedirect("")

@login_required
def contacto(request, voluntario_id=None):
    # Ver contacto do voluntário
    if voluntario_id:
        contacto = Voluntario.objects.get(id=voluntario_id)
        user = request.user
        return custom_render(request, "contacto.html", {"contacto": contacto, "user": user})
        
    # Ver lista de voluntários
    else:
        contactos = Voluntario.objects.order_by('-date_joined')[:5]
        return custom_render(request, "contactos.html", {"contactos": contactos})

@login_required
def editar_contacto(request, voluntario_id=None):
    voluntario = Voluntario.objects.get(pk=voluntario_id)

    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contactos/"+str(voluntario_id))
    else:
        form = VoluntarioForm(instance=voluntario)
    return custom_render(request, "editar_contacto.html", {"form": form})

@login_required
def dashboard(request):
    avisos = Aviso.objects.all().reverse()[:5]
    turnos = Escala.objects.filter(Q(condutor=request.user) | Q(preto=request.user) | Q(outro=request.user))
    turnos = turnos.filter(data__gte=datetime.date.today()).order_by("data")[:5]
    buracos = Escala.objects.filter(Q(condutor=None) | Q(preto=None) | Q(outro=None))
    buracos = buracos.order_by("data")[:5]
    return custom_render(request, "home.html", {'avisos':avisos, 'turnos':turnos, 'buracos':buracos})

@login_required
def quit(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def AdicionarAviso(request):
    if request.method == "POST":
        titulo = request.POST['titulo']
        mensagem = request.POST['mensagem']
        AdicionarNovoAviso(titulo, mensagem)
 
        custom_render(request, "algures na web", {'titulo':titulo, 'mensagem':mensagem})

    else:
        return HttpResponseRedirect("")

@login_required
def listaAvisos(request, desde):
    return HttpResponse("")


#Funções Auxiliares
def AdicionarNovoAviso(titl, conteudo):
    Now = datetime.date

    NovoAviso = Aviso(titulo = titl, date = Now, mensagem = conteudo)
    NovoAviso.save()