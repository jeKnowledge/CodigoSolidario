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
			return HttpResponse(str(voluntario_id))

		# Ver lista de voluntários
		else:
			contacto = Voluntario.objects.order_by('-pub_date')[:5]
		    context = {'contacto': contacto}
    		return render(request, 'RecHumanos/contactos.html', context)
    		
	elif request.method == 'POST':
		return HttpResponse("POST")
	else:
		return HttpResponse(request.method)
