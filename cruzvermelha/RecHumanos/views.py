# Create your views here.
from models import *
from django.http import HttpResponse, HttpRequest

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