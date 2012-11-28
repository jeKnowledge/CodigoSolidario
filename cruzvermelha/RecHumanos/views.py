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
    # Ver contacto do voluntário
    if voluntario_id:
        contacto = Voluntario.objects.get(id=voluntario_id)
        return render_to_response("contacto.html", {"contacto": contacto})
        
    # Ver lista de voluntários
    else:
        contactos = Voluntario.objects.order_by('-date_joined')[:5]
        return render_to_response("contactos.html", {"contactos": contactos})

def editar_contacto(request, voluntario_id=None):
    voluntario = Voluntario.objects.get(pk=voluntario_id)

    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contactos/"+str(voluntario_id))
    else:
        form = VoluntarioForm(instance=voluntario)
    return render_to_response("editar_contacto.html", {"form": form}, context_instance=RequestContext(request))