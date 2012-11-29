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
    # Ver contacto do voluntário
    if voluntario_id:
        contacto = Voluntario.objects.get(id=voluntario_id)
        user = request.user
        return render_to_response("contacto.html", {"contacto": contacto, "user": user})
        
    # Ver lista de voluntários
    else:
        contactos = Voluntario.objects.order_by('-date_joined')[:5]
        return render_to_response("contactos.html", {"contactos": contactos})

@login_required
def editar_contacto(request, voluntario_id=None):
    voluntario = Voluntario.objects.get(pk=voluntario_id)
    user = request.user
    if voluntario.id != user.id:
        return HttpResponseRedirect("/contactos/"+str(voluntario_id))

    if request.method == 'POST':
        form = VoluntarioForm(request.POST, instance=voluntario)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/contactos/"+str(voluntario_id))
    else:
        form = VoluntarioForm(instance=voluntario)
    return render_to_response("editar_contacto.html", {"form": form}, context_instance=RequestContext(request))

@login_required
def editar_disponibilidade(request, voluntario_id=None):
    voluntario = Voluntario.objects.get(pk=voluntario_id)
    user = request.user
    if voluntario.id != user.id:
        return HttpResponseRedirect("/contactos/"+str(voluntario_id))

    if request.method == 'POST':
        form = DisponibilidadeForm(request.POST)
        if form.is_valid():
            i = -1
            for dia in ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']:
                i += 1
                for turno in [1, 2, 3]:
                    disponibilidade = form.cleaned_data[dia + str(turno)]
                    registo = Disponibilidade.objects.filter(voluntario_id=voluntario_id, turno=turno, dia=i)
                    if registo and not disponibilidade: # se exisita mas deixou de existir
                        registo.delete()
                    elif not registo and disponibilidade: # se não exisita mas passou a existir
                        novo = Disponibilidade(voluntario_id=voluntario_id, turno=turno, dia=i)
                        novo.save()

            return HttpResponseRedirect("/contactos/"+str(voluntario_id))
        else:
            return HttpResponseRedirect("/contactos/")
    # GET
    else:
        #form = DisponibilidadeForm()
        resp = {}
        i = -1
        for dia in ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']:
            i += 1
            for turno in [1, 2, 3]:
                if Disponibilidade.objects.filter(voluntario_id=voluntario_id, turno=turno, dia=i):
                    resp[dia + str(turno)] = True
        form = DisponibilidadeForm(initial=resp)
    return render_to_response("editar_disponibilidade.html", {"form": form}, context_instance=RequestContext(request))


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