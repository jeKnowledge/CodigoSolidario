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

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("dashboard")
    else:
        return render_to_response("index.html", {}, context_instance=RequestContext(request))

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

        return render_to_response("index.html", {"message": message})
    else: 
        return HttpResponseRedirect("")

@login_required
def contacto(request, voluntario_id=None):
    if request.method == 'GET':

        # Ver contacto do voluntário
        if voluntario_id:
            contacto = Voluntario.objects.get(id=voluntario_id)
            return render_to_response("contacto.html", {"contacto": contacto})
            
        # Ver lista de voluntários
        else:
            contactos = Voluntario.objects.order_by('-date_joined')[:5]
            return render_to_response("contactos.html", {"contactos": contactos})
            
    elif request.method == 'POST':
        return HttpResponse("POST")
    else:
        return HttpResponse(request.method)


@login_required
def dashboard(request):
    avisos = Aviso.objects.all().reverse()[:5]
    turnos = Escala.objects.filter(Q(condutor=request.user) | Q(preto=request.user) | Q(outro=request.user))
    turnos = turnos.filter(data__gte=datetime.date.today()).order_by("data")[:5]
    return HttpResponse(turnos)


@login_required
def quit(request):
    logout(request)
    return HttpResponseRedirect('/')