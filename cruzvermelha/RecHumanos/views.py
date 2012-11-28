# -*- coding: utf-8 -*-

from models import *
from django.http import HttpResponse, HttpRequest

from django.contrib.auth import authenticate, login, logout

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def home(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("dashboard")
    else:
        return render_to_response("index.html", {})

def login(requet):
    if request.method == "POST":
        if request.method == 'POST':
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
