from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from RecHumanos.models import *
from RecHumanos.forms import *

class VoluntarioAdmin(auth_admin.UserAdmin):
	fieldsets = auth_admin.UserAdmin.fieldsets + (
		('Dados pessoais', {'fields': ('telefone', 'telefone2', 'formacao', 'categoria')}),
	)
	form = VoluntarioChangeForm

admin.site.unregister(User)
admin.site.register(Voluntario, VoluntarioAdmin)
admin.site.register(Escala)
admin.site.register(Disponibilidade)
admin.site.register(Aviso)
admin.site.register(Apoio)
admin.site.register(Turno)
admin.site.register(Inscricao)
admin.site.register(Troca)